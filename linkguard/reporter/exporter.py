import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from linkguard.scanner.link_checker import LinkResult
from linkguard.scanner.rules import RuleViolation


class Exporter:
    """Exports scan results to JSON or CSV format."""

    @staticmethod
    def export_to_json(
        results: List[LinkResult],
        violations: List[RuleViolation],
        output_path: Path,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Exports results to JSON file.

        Args:
            results (List[LinkResult]): List of link check results
            violations (List[RuleViolation]): List of rule violations
            output_path (Path): Path to save the JSON file
            metadata (Dict[str, Any], optional): Additional Metadata
                (directory, mode, etc.). Defaults to None.
        """
        data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_links": len(results),
                "broken_links": sum(1 for r in results if r.is_broken),
                "working_links": sum(1 for r in results if not r.is_broken),
                "violations": len(violations),
                **(metadata or {}),
            },
            "results": [
                {
                    "url": r.url,
                    "status_code": r.status_code,
                    "is_broken": r.is_broken,
                    "error": r.error,
                    "response_time": r.response_time,
                    "file_path": str(r.file_path),
                    "line_number": r.line_number,
                }
                for r in results
            ],
            "violations": [
                {
                    "url": v.url,
                    "rule": v.rule,
                    "severity": v.severity,
                    "message": v.message,
                    "file_path": str(v.file_path),
                    "line_number": v.line_number,
                }
                for v in violations
            ],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def export_to_csv(
        results: List[LinkResult],
        violations: List[RuleViolation],
        output_path: Path,
    ) -> None:
        """Exports results to CSV file

        Args:
            results (List[LinkResult]): List of link check results.
            violations (List[RuleViolation]): List of violations.
            output_path (Path): Path to save the CSV file.
        """

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow(
                [
                    "URL",
                    "Status Code",
                    "Is Broken",
                    "Error",
                    "Response Time (s)",
                    "File Path",
                    "Line Number",
                    "Rule Violation",
                    "Violation Severity",
                ]
            )

            # Create a map for quick violation lookup
            violation_map = {v.url: v for v in violations}

            # Write to CSV file
            for r in results:
                violation = violation_map.get(r.url)

                writer.writerow(
                    [
                        r.url,
                        r.status_code or "N/A",
                        "Yes" if r.is_broken else "No",
                        r.error or "N/A",
                        f"{r.response_time:.2f}" if r.response_time else None,
                        r.file_path,
                        r.line_number or "N/A",
                        violation.rule if violation else None,
                        violation.severity if violation else None,
                    ]
                )

    @staticmethod
    def export_to_markdown(
        results: List[LinkResult],
        violations: List[RuleViolation],
        output_path: Path,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Export results to Markdown file.

        Args:
            results (List[LinkResult]): List of link check results
            violations (List[RuleViolation]): List of violations
            output_path (Path): Path to save Markdown file
            metadata (Optional[Dict[str, Any]], optional): Additional
                metadata. Defaults to None.
        """

        broken = [r for r in results if r.is_broken]
        working = [r for r in results if not r.is_broken]

        lines = [
            "# Linkguard Scan Report\n",
            "",
            f"**Generated on:** {datetime.now().isoformat()}",
            "",
            "## Summary",
            "",
            f"- Total Links Checked: {len(results)}",
            f"- Working Links: {len(working)}",
            f"- Broken Links: {len(broken)}",
            f"- Rule Violations: {len(violations)}",
            "",
        ]

        if metadata:
            lines.extend(
                [
                    "## Scan Details",
                    "",
                    f"- **Directory:** `{metadata.get('directory', 'N/A')}`",
                    f"- **Mode:** `{metadata.get('mode', 'N/A')}`",
                    f"- **Timeout:** `{metadata.get('timeout', 'N/A')} seconds`",
                    "",
                ]
            )

        if violations:
            lines.extend(
                [
                    "## Rule Violations",
                    "",
                    "| URL | Rule | Severity | Message | File Path | Line Number |",
                    "|-----|------|----------|---------|-----------|-------------|",
                ]
            )

            for v in violations:
                lines.append(
                    f"| {v.url} | {v.rule} | {v.severity} | "
                    f"{v.message} | {v.file_path} | "
                    f"{v.line_number or 'N/A'} |"
                )

            lines.append("")

        if broken:
            lines.extend(
                [
                    "## Broken Links",
                    "",
                    "| URL | Status Code | Error | Response Time (s) | File Path | Line Number |",
                    "|-----|-------------|-------|-------------------|-----------|-------------|",
                ]
            )

            for r in broken:
                time_str = (
                    f"{r.response_time:.2f}" if r.response_time else "N/A"
                )
                lines.append(
                    f"| {r.url} | {r.status_code or 'N/A'} | "
                    f"{r.error or 'N/A'} | {time_str} | "
                    f"{r.file_path} | {r.line_number or 'N/A'} |"
                )

            lines.append("")

        if working:
            lines.extend(
                [
                    "## Working Links",
                    "",
                    "| URL | Status Code | Response Time (s) | File Path | Line Number |",
                    "|-----|-------------|-------------------|-----------|-------------|",
                ]
            )

            for r in working:
                time_str = (
                    f"{r.response_time:.2f}" if r.response_time else "N/A"
                )
                lines.append(
                    f"| {r.url} | {r.status_code or 'N/A'} | "
                    f"{time_str} | {r.file_path} | "
                    f"{r.line_number or 'N/A'} |"
                )

            lines.append("")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
