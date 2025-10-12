import asyncio
import aiohttp
from typing import Sequence, Dict, Any, Optional, Callable, Tuple, Union
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LinkResult:
    """Result of checking a single link."""

    url: str
    status_code: Optional[int]
    is_broken: bool
    error: Optional[str]
    response_time: float
    file_path: str
    line_number: Optional[int]


class LinkChecker:
    """Asynchronously checks URLs for validity."""

    # Browser-like headers without Brotli (avoids decode errors)
    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    def __init__(self, timeout: int = 10, max_concurrent: int = 50):
        self.timeout = timeout
        self.max_concurrent = max_concurrent

    async def check_links(
        self,
        url_data: Sequence[Tuple[Union[Path, str], Dict[str, Any]]],
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> list[LinkResult]:
        """
        Check a list of URLs concurrently.

        Args:
            url_data: List of tuples containing (file_path, url_info).
            progress_callback: Callback function to report progress

        Returns:
            list[LinkResult]: List of results for each URL checked.
        """

        semaphore = asyncio.Semaphore(self.max_concurrent)
        results: list[LinkResult] = []
        completed = 0

        # Create TCP connector
        connector = aiohttp.TCPConnector(
            ssl=False,  # Disable SSL verification for dev environments
            limit=self.max_concurrent,
            limit_per_host=10,  # Limit per host to avoid overwhelming servers
            ttl_dns_cache=300,  # Cache DNS for 5 minutes
        )

        async with aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            headers=self.DEFAULT_HEADERS,
        ) as session:
            tasks = [
                self._check_one_link(session, semaphore, file_path, url_info)
                for file_path, url_info in url_data
            ]

            # Process tasks as they complete to provide progress updates
            for coro in asyncio.as_completed(tasks):
                try:
                    result = await coro
                    results.append(result)
                    completed += 1
                    if progress_callback:
                        progress_callback(completed)
                except Exception:
                    # Handle unexpected exceptions
                    completed += 1
                    if progress_callback:
                        progress_callback(completed)

        return results

    async def _check_one_link(
        self,
        session: aiohttp.ClientSession,
        semaphore: asyncio.Semaphore,
        file_path: Union[Path, str],
        url_info: Dict[str, Any],
    ) -> LinkResult:
        """Check a single URL and return Results

        Args:
            session: Session Client
            semaphore: Semaphore for concurrency control
            file_path: File path where URL was found
            url_info: URL info dictionary

        Returns:
            LinkResult: Result of the single URL check
        """

        url = url_info["url"]

        async with semaphore:
            start_time = asyncio.get_event_loop().time()

            try:
                # Use HEAD request first (faster), fall back to GET if needed
                async with session.head(
                    url,
                    allow_redirects=True,
                ) as response:
                    response_time = asyncio.get_event_loop().time() - start_time

                    # Some servers return 403/405 for HEAD but work with GET
                    # If HEAD fails with 4xx, try GET as fallback
                    if response.status in {403, 405, 501}:
                        return await self._check_with_get(
                            session, url, file_path, url_info, start_time
                        )

                    return LinkResult(
                        url=url,
                        status_code=response.status,
                        is_broken=response.status >= 400,
                        error=None,
                        response_time=response_time,
                        file_path=str(file_path),
                        line_number=url_info.get("line_number"),
                    )

            except (aiohttp.ClientError, asyncio.TimeoutError):
                # If HEAD request fails, try GET as fallback
                return await self._check_with_get(session, url, file_path, url_info, start_time)

            except Exception as e:
                response_time = asyncio.get_event_loop().time() - start_time
                return LinkResult(
                    url=url,
                    status_code=None,
                    is_broken=True,
                    error=f"Unexpected error: {str(e)[:50]}",
                    response_time=response_time,
                    file_path=str(file_path),
                    line_number=url_info.get("line_number"),
                )

    async def _check_with_get(
        self,
        session: aiohttp.ClientSession,
        url: str,
        file_path: Union[Path, str],
        url_info: Dict[str, Any],
        start_time: float,
    ) -> LinkResult:
        """Fallback to GET request if HEAD fails."""
        try:
            async with session.get(
                url,
                allow_redirects=True,
            ) as response:
                response_time = asyncio.get_event_loop().time() - start_time

                return LinkResult(
                    url=url,
                    status_code=response.status,
                    is_broken=response.status >= 400,
                    error=None,
                    response_time=response_time,
                    file_path=str(file_path),
                    line_number=url_info.get("line_number"),
                )

        except asyncio.TimeoutError:
            response_time = asyncio.get_event_loop().time() - start_time
            return LinkResult(
                url=url,
                status_code=None,
                is_broken=True,
                error="Timeout",
                response_time=response_time,
                file_path=str(file_path),
                line_number=url_info.get("line_number"),
            )

        except aiohttp.ClientError as e:
            response_time = asyncio.get_event_loop().time() - start_time
            return LinkResult(
                url=url,
                status_code=None,
                is_broken=True,
                error=f"Connection error: {str(e)[:50]}",
                response_time=response_time,
                file_path=str(file_path),
                line_number=url_info.get("line_number"),
            )

        except Exception as e:
            response_time = asyncio.get_event_loop().time() - start_time
            return LinkResult(
                url=url,
                status_code=None,
                is_broken=True,
                error=f"Unexpected error: {str(e)[:50]}",
                response_time=response_time,
                file_path=str(file_path),
                line_number=url_info.get("line_number"),
            )
