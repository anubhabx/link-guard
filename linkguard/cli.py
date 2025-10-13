import typer
import asyncio
from typing import Optional, Dict, Any, List, Tuple
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.table import Table
from pathlib import Path

from linkguard.scanner.file_scanner import FileScanner
from linkguard.scanner.url_extractor import URLExtractor
from linkguard.scanner.link_checker import LinkChecker
from linkguard.scanner.rules import EnvironmentRules
from linkguard.reporter.exporter import Exporter
from linkguard.utils.config import load_config

app = typer.Typer(
    name="linkguard",
    help="CLI tool for detecting broken links and localhost URLs in " "project files",
)
console = Console(force_terminal=True, legacy_windows=False)


@app.command()
def scan(
    directory: Path = typer.Argument(".", help="Directory to scan"),
    mode: str = typer.Option(
        "dev",
        "--mode",
        "-m",
        help="Scanning mode: 'dev' or 'prod' " "(prod flags localhost URLs)",
    ),
    timeout: int = typer.Option(10, "--timeout", "-t", help="Timeout in seconds for HTTP requests"),
    concurrency: int = typer.Option(
        50, "--concurrency", "-c", help="Number of concurrent HTTP requests"
    ),
    export: Optional[str] = typer.Option(
        None, "--export", "-e", help="Export results to a JSON file"
    ),
    ignore: Optional[str] = typer.Option(
        None,
        "--ignore",
        "-i",
        help="Comma-separated list of glob patterns to ignore",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    """Scan directory for broken links and environment violations."""
    
    # Validate directory exists
    if not directory.exists():
        console.print(f"[bold red]Error:[/bold red] Directory does not exist: {directory}")
        raise typer.Exit(code=2)
    
    if not directory.is_dir():
        console.print(f"[bold red]Error:[/bold red] Path is not a directory: {directory}")
        raise typer.Exit(code=2)

    # Load configuration with CLI overrides
    cli_overrides: Dict[str, Any] = {}
    cli_overrides["mode"] = mode
    cli_overrides["timeout"] = timeout
    cli_overrides["concurrency"] = concurrency
    if ignore is not None:
        # Split comma-separated patterns and strip whitespace
        cli_overrides["ignore_patterns"] = [p.strip() for p in ignore.split(",")]

    try:
        config = load_config(directory, cli_overrides)
    except ValueError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        raise typer.Exit(code=2)

    # Get final config values
    final_mode = config.get("mode", "dev")
    final_timeout = config.get("timeout", 10)
    final_concurrency = config.get("concurrency", 10)

    console.print(f"[bold blue]Scanning directory:[/bold blue] {directory}")
    console.print(
        f"[dim]Mode: {final_mode} | Timeout: {final_timeout}s | Concurrency: {final_concurrency}[/dim]\n"
    )

    if verbose and config.get_ignore_patterns():
        console.print(f"[dim]Ignoring patterns: {', '.join(config.get_ignore_patterns())}[/dim]\n")

    # Scan for files
    scanner = FileScanner(directory, ignore_patterns=set(config.get_ignore_patterns()))
    files = scanner.scan()

    console.print(f"[green][/green] Found {len(files)} files to scan")

    # Extract URLs from files
    extractor = URLExtractor()
    all_urls: List[Tuple[Path, Dict[str, Any]]] = []

    for file in files:
        urls = extractor.extract_from_file(file)
        if urls:
            all_urls.extend([(file, url) for url in urls])

    console.print(f"[green][/green] Extracted {len(all_urls)} URLs.\n")

    if not all_urls:
        console.print("[bold yellow]No URLs found to check.[/bold yellow]")
        return

    # Check environment rules
    rules = EnvironmentRules(mode=final_mode)
    violations = rules.check_urls(all_urls)

    if violations:
        console.print(f"[bold red] Found {len(violations)} rule violations:[/bold red]")
        for v in violations:
            console.print(
                f" - [red]{v.url}[/red] in {v.file_path}:{v.line_number or '?'} (Rule: {v.rule})"
            )
        console.print()

    # Check links asynchronously
    console.print("[bold blue]Checking links...[/bold blue]\n")

    checker = LinkChecker(timeout=final_timeout, max_concurrent=final_concurrency)

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="green", finished_style="bold green"),
        TaskProgressColumn(text_format_no_percentage="{task.completed}/{task.total}"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"[cyan]Checking {len(all_urls)} links...[/cyan]",
            total=len(all_urls),
        )

        def update_progress(completed: int):
            progress.update(task, completed=completed)

        results = asyncio.run(checker.check_links(all_urls, update_progress))

    # Display Results
    console.print()
    broken_links = [r for r in results if r.is_broken]
    working_links = [r for r in results if not r.is_broken]

    # Show summary table
    table = Table(title="Scan Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", justify="right", style="green")

    table.add_row("Files Scanned", str(len(files)))
    table.add_row("URLs Found", str(len(all_urls)))
    table.add_row("Working Links", str(len(working_links)))
    table.add_row("Broken Links", str(len(broken_links)))
    table.add_row("Rule Violations", str(len(violations)))

    console.print(table)
    console.print()

    # Show broken links details
    if broken_links:
        console.print(f"[bold red] Found {len(broken_links)} broken links:[/bold red]")
        for result in broken_links:
            console.print(
                f" - [red]{result.url}[/red] in "
                f"{result.file_path}:{result.line_number or '?'} "
                f"(Error: {result.error or result.status_code})"
            )

    if working_links:
        console.print(
            f"\n[bold green] Found "
            f"{len(working_links)} working links.[/bold green]"
        )

    # Export results if requested
    if export:
        export_path = Path(export)
        extension = export_path.suffix.lower()

        metadata: Dict[str, Any] = {
            "directory": str(directory),
            "mode": final_mode,
            "timeout": final_timeout,
            "concurrency": final_concurrency,
            "files_scanned": len(files),
        }

        try:
            if extension == ".json":
                Exporter.export_to_json(results, violations, export_path, metadata)
            elif extension == ".csv":
                Exporter.export_to_csv(results, violations, export_path)
            elif extension in {".md", ".markdown"}:
                Exporter.export_to_markdown(results, violations, export_path, metadata)
            else:
                console.print(
                    f"[yellow]:white_exclamation_mark:[/yellow] "
                    f"Unsupported export format: {extension}"
                )
                console.print("[dim]Supported formats are .json, .csv, .md/.markdown[/dim]")
                return

            console.print(f"[bold green]:tada: Results exported to {export_path}[/bold green]")
        except Exception as e:
            console.print(f"[red] Failed to export results: {e}[/red]")

    # Exit with appropriate code
    if violations and final_mode == "prod":
        console.print("\n[yellow] Environment violations detected in production mode![/yellow]")
        for v in violations[:5]:
            console.print(f"  • {v.url} in {v.file_path}:{v.line_number or '?'} ({v.rule})")
        raise typer.Exit(code=3)

    if broken_links:
        raise typer.Exit(code=1)

    raise typer.Exit(code=0)

def main():
    app()


if __name__ == "__main__":
    main()
