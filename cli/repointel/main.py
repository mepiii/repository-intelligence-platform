import click
import os
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from repointel.client import RepointelClient

console = Console()
client = RepointelClient()

@click.group()
def cli():
    """Repository Intelligence Platform CLI"""
    pass

@cli.command()
@click.argument("path", default=".")
def scan(path):
    """Scan a local git repository."""
    abs_path = os.path.abspath(path)
    console.print(f"[bold blue]Scanning repository at:[/bold blue] {abs_path}")
    try:
        res = client.scan(abs_path)
        console.print(f"[bold green]Scan complete![/bold green] Scanned {res.get('files_scanned')} files and {res.get('commits')} commits.")
    except Exception as e:
        console.print(f"[bold red]Scan failed:[/bold red] {e}")

@cli.command()
def index():
    """Index vectors for repository."""
    console.print("[bold blue]Generating semantic vector embeddings...[/bold blue]")
    try:
        res = client.index(1)
        console.print(f"[bold green]Indexing complete![/bold green] Vectorized {res.get('total_vectors')} documents.")
    except Exception as e:
        console.print(f"[bold red]Indexing failed:[/bold red] {e}")

@cli.command()
@click.argument("query")
def search(query):
    """Search codebase semantically and keyword."""
    console.print(f"[bold blue]Searching for:[/bold blue] {query}")
    try:
        results = client.search(query)
        table = Table(title="Search Results")
        table.add_column("File Path", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Score", style="green")
        table.add_column("Snippet Preview", style="white")

        for r in results:
            table.add_row(r["file_path"], r["entity_type"], str(r["score"]), r["content_snippet"][:80].replace("\n", " "))
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Search failed:[/bold red] {e}")

@cli.command()
def graph():
    """Inspect Repository Knowledge Graph."""
    try:
        data = client.get_graph()
        console.print(f"[bold green]Knowledge Graph Summary:[/bold green] {len(data['nodes'])} Nodes, {len(data['edges'])} Edges.")
    except Exception as e:
        console.print(f"[bold red]Failed to get graph:[/bold red] {e}")

@cli.command()
def timeline():
    """Display Repository Timeline."""
    try:
        events = client.get_timeline()
        table = Table(title="Repository Timeline")
        table.add_column("Event Type", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Timestamp", style="yellow")

        for e in events:
            table.add_row(e["event_type"], e["description"], str(e["timestamp"]))
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Failed to fetch timeline:[/bold red] {e}")

@cli.command()
def debt():
    """Analyze Technical Debt."""
    try:
        d = client.get_debt()
        console.print(Panel(f"[bold red]Overall Technical Debt Score:[/bold red] {d['overall_debt_score']}/100\n"
                            f"[bold green]Maintainability Score:[/bold green] {d['overall_maintainability_score']}/100"))
        
        console.print("[bold yellow]Key Refactoring Suggestions:[/bold yellow]")
        for sug in d.get("suggestions", []):
            console.print(f" - {sug}")
    except Exception as e:
        console.print(f"[bold red]Debt analysis failed:[/bold red] {e}")

@cli.command()
@click.argument("prompt")
def ask(prompt):
    """Ask AI assistant about repository."""
    console.print(f"[bold blue]Querying AI Repository Assistant...[/bold blue]\n")
    try:
        res = client.ask(prompt)
        console.print(Panel(res["answer"], title="AI Assistant Answer", border_style="cyan"))
        
        if res.get("citations"):
            console.print("[bold yellow]Source Citations:[/bold yellow]")
            for c in res["citations"]:
                console.print(f" • [cyan]{c['file_path']}[/cyan] (Relevance: {c['score']})")
    except Exception as e:
        console.print(f"[bold red]AI query failed:[/bold red] {e}")

@cli.command()
def serve():
    """Start local backend server."""
    console.print("[bold green]Starting backend server on http://localhost:8000 ...[/bold green]")
    subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"], cwd="backend")

if __name__ == "__main__":
    cli()
