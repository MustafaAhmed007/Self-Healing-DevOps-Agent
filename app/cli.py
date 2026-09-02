from __future__ import annotations

import typer
from rich.console import Console

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def demo() -> None:
    console.print("[bold]Self-Healing DevOps Agent[/bold]")
    console.print("Vertical-slice foundation is installed.")
    console.print("Safety defaults: network=disabled, bounded execution, policy-gated diffs.")


@app.command()
def doctor() -> None:
    import shutil
    checks = {"python": shutil.which("python"), "docker": shutil.which("docker"), "git": shutil.which("git")}
    for name, value in checks.items():
        console.print(f"{'✓' if value else '✗'} {name}")


if __name__ == "__main__":
    app()
