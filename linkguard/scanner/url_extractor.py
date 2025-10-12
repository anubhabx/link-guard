import re
from pathlib import Path
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import json


class URLExtractor:
    """Extract URLs from different file formats."""

    # URL regex pattern - matches http:// or https:// URLs
    # Modified to exclude trailing punctuation
    URL_PATTERN = re.compile(
        r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\."
        r"[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)"
    )

    # Markdown link pattern [text](url)
    MD_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def extract_from_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Extract URLs from a file based on its extension.

        Returns:
            List of dicts with 'url', 'line_number', and 'context' keys
        """
        suffix = file_path.suffix.lower()

        if suffix in {".md", ".txt"}:
            return self._extract_from_text(file_path)
        elif suffix in {".html", ".htm"}:
            return self._extract_from_html(file_path)
        elif suffix == ".json":
            return self._extract_from_json(file_path)
        elif suffix in {".js", ".jsx", ".tsx", ".ts"}:
            return self._extract_from_text(file_path)

        return []

    def _extract_from_text(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extract URLs from plain text/markdown files."""
        urls = []
        seen_urls = set()  # Track URLs we've already found to avoid duplicates

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, start=1):
                # Find markdown-style links [text](url) FIRST
                md_matches = self.MD_LINK_PATTERN.findall(line)

                for text, url in md_matches:
                    # Only include URLs starting with http:// or https://
                    if url.startswith(("http://", "https://")):
                        # Clean URL and create unique key
                        clean_url = self._clean_url(url)
                        url_key = (clean_url, line_num)

                        if url_key not in seen_urls:
                            seen_urls.add(url_key)
                            urls.append(
                                {
                                    "url": clean_url,
                                    "line_number": line_num,
                                    "context": line.strip()[:60],
                                }
                            )

                # Find bare URLs (http:// or https://)
                # But skip them if they're part of markdown links
                url_matches = self.URL_PATTERN.findall(line)
                for url in url_matches:
                    clean_url = self._clean_url(url)
                    url_key = (clean_url, line_num)

                    # Only add if we haven't seen this URL on this line (avoids markdown duplicates)
                    if url_key not in seen_urls:
                        seen_urls.add(url_key)
                        urls.append(
                            {
                                "url": clean_url,
                                "line_number": line_num,
                                "context": line.strip()[:60],
                            }
                        )

        return urls

    def _clean_url(self, url: str) -> str:
        """Remove trailing punctuation from URLs."""
        # Remove trailing ), ., ,, ;, etc.
        return url.rstrip(".,;:)")

    def _extract_from_html(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extract URLs from HTML files."""
        urls = []

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        # Extract from <a href="">
        for tag in soup.find_all("a", href=True):
            url = tag.get("href")
            if isinstance(url, str) and url.startswith(("http://", "https://")):
                urls.append(
                    {
                        "url": url,
                        "line_number": None,
                        "context": f'<a href="{url}">',
                    }
                )

        # Extract from <img src="">, <link href="">, <script src="">
        for tag in soup.find_all(["img", "link", "script"]):
            url = tag.get("src") or tag.get("href")

            if isinstance(url, str) and url.startswith(("http://", "https://")):
                urls.append(
                    {
                        "url": url,
                        "line_number": None,
                        "context": f'<{tag.name} src="{url}">',
                    }
                )

        return urls

    def _extract_from_json(self, file_path: Path) -> List[Dict[str, Any]]:
        """Extract URLs from JSON files."""
        urls: List[Dict[str, Any]] = []

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)

            self._search_json_for_urls(data, urls)
        except json.JSONDecodeError:
            pass

        return urls

    def _search_json_for_urls(self, obj, urls: List[Dict[str, Any]], path: str = ""):
        """Recursively search JSON object for URL strings."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                self._search_json_for_urls(value, urls, f"{path}.{key}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                self._search_json_for_urls(item, urls, f"{path}[{i}]")
        elif isinstance(obj, str):
            # Only match strings that start with http:// or https://
            if obj.startswith(("http://", "https://")):
                urls.append(
                    {
                        "url": obj,
                        "line_number": None,
                        "context": f"JSON path: {path}",
                    }
                )
