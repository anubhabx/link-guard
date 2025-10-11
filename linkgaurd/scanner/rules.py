import re
from typing import List
from dataclasses import dataclass


@dataclass
class RuleViolation:
    """Represents a rule violation found in a file."""

    url: str
    rule: str
    severity: str
    message: str
    file_path: str
    line_number: int | None


class EnvironmentRules:
    """Checks URLs against predefined environment rules."""

    # Patterns that indicate development or localhost URLs
    LOCALHOST_PATTERNS = [
        r"localhost",  # Localhost
        r"127\.0\.0\.1",  # Loopback address
        r"0\.0\.0\.0",  # Non-routable meta-address
        r"192\.168\.\d{1,3}\.\d{1,3}",  # Private network
        r"10\.\d{1,3}\.\d{1,3}\.\d{1,3}",  # Private network
        r"::1",  # IPv6 localhost
        r"\.local$",  # Local domain
        r"\.test$",  # Test domain
    ]

    def __init__(self, mode: str = "dev"):
        """Initializes rule checker.

        Args:
            mode (str): Mode of operation, either "dev" or "prod".
        """
        self.mode = mode
        self.localhost_regex = re.compile(
            "|".join(self.LOCALHOST_PATTERNS), re.IGNORECASE
        )

    def check_url(
        self, url: str, file_path: str, line_number: int | None
    ) -> RuleViolation | None:
        """Check a URL against environment rules.

        Args:
            url (str): The URL to check.
            file_path (str): The file path where the URL was found.
            line_number (int | None): The line number where the URL was found.

        Returns:
            RuleViolation if a rule is violated, otherwise None.
        """
        if self.mode == "prod":
            if self.localhost_regex.search(url):
                return RuleViolation(
                    url=url,
                    rule="no-localhost-in-prod",
                    severity="error",
                    message="Localhost/development URL found in "
                    "production mode",
                    file_path=file_path,
                    line_number=line_number,
                )
        return None

    def check_urls(self, urls_data: List[tuple]) -> List[RuleViolation]:
        """Check multiple URLs against rules.

        Args:
            urls_data (List[tuple]): List of (file_path, url_info) tuples.

        Returns:
            List[RuleViolation]: List of rule violations
        """
        violations = []

        for file_path, url_info in urls_data:
            violation = self.check_url(
                url_info["url"], str(file_path), url_info.get("line_number")
            )

            if violation:
                violations.append(violation)

        return violations
