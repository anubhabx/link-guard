import typer
import asyncio
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path

from linkgaurd.scanner.file_scanner import FileScanner
from linkgaurd.scanner.url_extractor import URLExtractor
from linkgaurd.scanner.link_checker import LinkChecker

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
    
    scanner = FileScanner(directory)
    files = scanner.scan()
    
    console.print(f"[green]:white_check_mark:[/green] Found {len(files)} files to scan")
    
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
        
    console.print()
    broken_links = [r for r in results if r.is_broken]
    working_links = [r for r in results if not r.is_broken]
    
    if broken_links:
        console.print(f"[bold red]:x: Found {len(broken_links)} broken links:[/bold red]")
        for result in broken_links:
            console.print(f" - [red]{result.url}[/red] in {result.file_path}:{result.line_number or '?'} (Error: {result.error or result.status_code})")
            
    if working_links:
        console.print(f"\n[bold green]:white_check_mark: Found {len(working_links)} working links.[/bold green]")
        
    if broken_links:
        raise typer.Exit(code=1)
    else:
        console.print("\n[bold green]:tada: All links are valid![/bold green]")
        raise typer.Exit(code=0)
    
    # for file in files[:5]:
    #     console.print(f" :black_circle: {file.relative_to(directory)}")
    # if len(files) > 5:
    #     console.print(f" ... and {len(files) - 5} more")
    
    # for file, url_info in all_urls[:5]:
    #     console.print(f" :black_circle: {url_info['url']}")
    #     console.print(f"    [dim]in {file.relative_to(directory)}:{url_info['line_number'] or '?'}[/dim]")
    
    # if len(all_urls) > 5:
    #     console.print(f"\n  ... and {len(all_urls) - 5} more URLs")
    
def main():
    app()
    
if __name__ == "__main__":
    main()