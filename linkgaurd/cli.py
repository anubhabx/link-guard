import typer
import asyncio
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from pathlib import Path

from linkgaurd.scanner.file_scanner import FileScanner
from linkgaurd.scanner.url_extractor import URLExtractor
from linkgaurd.scanner.link_checker import LinkChecker
from linkgaurd.scanner.rules import EnvironmentRules

app = typer.Typer(
    name="linkgaurd",
    help="CLI tool for detecting broken links and localhost URLs in project files"
)
console = Console()

@app.command()
def scan(
    directory: Path = typer.Argument(
        ".",
        help="Directory to scan for links",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True
    ),
    mode: str = typer.Option(
        "dev",
        "--mode",
        "-m",
        help="Scanning mode: 'dev' or 'prod' (prod flags localhost URLs)"
    ),
    timeout: int = typer.Option(
        10,
        "--timeout",
        "-t",
        help="Timeout in seconds for HTTP requests"
    ),
    export: str = typer.Option(
        None,
        "--export",
        "-e",
        help="Export results to a JSON file"
    ),
):
    """ 
    Scan a directory for broken links and localhost URLS.
    """
    
    console.print(f"[bold blue]Scanning directory:[/bold blue] {directory}")
    console.print(f"[dim]Mode: {mode} | Timeout: {timeout}s[/dim]")
    
    # Scan for files
    scanner = FileScanner(directory)
    files = scanner.scan()
    
    console.print(f"[green]:white_check_mark:[/green] Found {len(files)} files to scan")
    
    # Extract URLs from files
    extractor = URLExtractor()
    all_urls = []
    
    for file in files:
        urls = extractor.extract_from_file(file)
        if urls:
            all_urls.extend([(file, url) for url in urls])
    
    console.print(f"[green]:white_check_mark:[/green] Extracted {len(all_urls)} URLs.\n")
    
    if not all_urls:
        console.print("[bold yellow]No URLs found to check.[/bold yellow]")
        return
    
    # Check environment rules
    rules = EnvironmentRules(mode=mode)
    violations = rules.check_urls(all_urls)
    
    if violations:
        console.print(f"[bold red]:warning: Found {len(violations)} rule violations:[/bold red]")
        for v in violations:
            console.print(f" - [red]{v.url}[/red] in {v.file_path}:{v.line_number or '?'} (Rule: {v.rule})")
        console.print()
    
    # Check links asynchronously
    console.print(":globe_showing_europe-africa: [bold blue]Checking links...[/bold blue]\n")
    
    checker = LinkChecker(timeout=timeout)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console = console
    ) as progress:
        task = progress.add_task(f"[cyan]Checking {len(all_urls)} links...[/cyan]", total=len(all_urls))
        results = asyncio.run(checker.check_links(all_urls))
        progress.update(task, completed=True)
        
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
        console.print(f"[bold red]:x: Found {len(broken_links)} broken links:[/bold red]")
        for result in broken_links:
            console.print(f" - [red]{result.url}[/red] in {result.file_path}:{result.line_number or '?'} (Error: {result.error or result.status_code})")
            
    if working_links:
        console.print(f"\n[bold green]:white_check_mark: Found {len(working_links)} working links.[/bold green]")
        
    # Exit with code 1 if there are broken links or violations
    if broken_links:
        raise typer.Exit(code=1)
    else:
        console.print("\n[bold green]:tada: All links are valid![/bold green]")
        raise typer.Exit(code=0)
    
def main():
    app()
    
if __name__ == "__main__":
    main()