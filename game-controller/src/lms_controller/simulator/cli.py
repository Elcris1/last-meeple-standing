"""CLI entrypoint for `uv run lms-sim` (implemented by Dev B in Phase 1)."""

import typer

app = typer.Typer(help="Interactive and scripted MQTT device simulator for Last Meeple Standing.")


@app.command()
def interactive(
    host: str = typer.Option("localhost", help="Mosquitto broker hostname"),
    port: int = typer.Option(1883, help="Mosquitto broker TCP port"),
) -> None:
    """Launch the interactive meeple/base simulator."""
    typer.echo(
        f"lms-sim Phase 0 scaffold (broker={host}:{port}). "
        "Implement interactive MQTT simulator in Phase 1."
    )


if __name__ == "__main__":
    app()
