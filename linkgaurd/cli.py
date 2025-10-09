import typer
from rich.console import Console
from pathlib import Path

from linkgaurd.scanner.file_scanner import FileScanner

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
    
    for file in files[:5]:
        console.print(f" :black_circle: {file.relative_to(directory)}")
    if len(files) > 5:
        console.print(f" ... and {len(files) - 5} more")
    
def main():
    app()
    
if __name__ == "__main__":
    main()