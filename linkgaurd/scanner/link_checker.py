import asyncio
import aiohttp
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class LinkResult:
    """Result of checking a single link."""
    url: str
    status_code: int | None
    is_broken: bool
    error: str | None
    response_time: float
    file_path: str
    line_number: int | None
    
class LinkChecker:
    """Asynchronously checks URLs for validity."""
    
    def __init__(self, timeout: int = 10, max_concurrent: int = 50):
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        
    async def check_links(self, url_data: List[tuple]) -> List[LinkResult]:
        """
        Check a list of URLs concurrently.
        
        Args:
            url_data (List[tuple]): List of tuples containing (url, file_path, line_number).
            
        Returns:
            List[LinkResult]: List of results for each URL checked.
        """
        
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        ) as session:
            tasks = [
                self._check_one_link(session, semaphore, file_path, url_info)
                for file_path, url_info in url_data
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [r for r in results if isinstance(r, LinkResult)]
            
    async def _check_one_link(
        self, 
        session: aiohttp.ClientSession, 
        semaaphore: asyncio.Semaphore,
        file_path: str,
        url_info: Dict[str, Any]
    ) -> LinkResult:
        """Check a single URL and return Results

        Args:
            session (aiohttp.ClientSession): Session Client
            semaaphore (asyncio.Semaphore): Semaphore
            file_path (str): File path to check
            url_info (Dict[str, Any]): URL info

        Returns:
            LinkResult: Result of the single URL search
        """
        
        url = url_info['url']
        
        async with semaaphore:
            start_time = asyncio.get_event_loop().time()
            
            try:
                async with session.get(url, allow_redirects=True, ssl=False) as response:
                    response_time = asyncio.get_event_loop().time() - start_time
                    
                    return LinkResult(
                        url=url,
                        status_code=response.status,
                        is_broken=response.status >= 400,
                        error=None,
                        response_time=response_time,
                        file_path=file_path,
                        line_number=url_info.get('line_number')
                    )
                    
            except asyncio.TimeoutError:
                response_time = asyncio.get_event_loop().time() - start_time
                return LinkResult(
                    url=url,
                    status_code=None,
                    is_broken=True,
                    error="Timeout",
                    response_time=response_time,
                    file_path=file_path,
                    line_number=url_info.get('line_number')
                )
                
            except aiohttp.ClientError as e:
                response_time = asyncio.get_event_loop().time() - start_time
                return LinkResult(
                    url=url,
                    status_code=None,
                    is_broken=True,
                    error=f"Connection error: {str(e)[:50]}",
                    response_time=response_time,
                    file_path=file_path,
                    line_number=url_info.get('line_number')
                )
            
            except Exception as e:
                response_time = asyncio.get_event_loop().time() - start_time
                return LinkResult(
                    url=url,
                    status_code=None,
                    is_broken=True,
                    error=f"Unexpected error: {str(e)[:50]}",
                    response_time=response_time,
                    file_path=file_path,
                    line_number=url_info.get('line_number')
                )