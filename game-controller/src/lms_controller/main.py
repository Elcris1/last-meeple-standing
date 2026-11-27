"""CLI entrypoint for `uv run lms-controller` (wired in Phase 2)."""

import typer

app = typer.Typer(help="Last Meeple Standing central MQTT game controller.")


@app.command()
def run(
    host: str = typer.Option("localhost", help="Mosquitto broker hostname"),
    port: int = typer.Option(1883, help="Mosquitto broker TCP port"),
) -> None:
    """Start the Last Meeple Standing game controller."""
    typer.echo(
        f"lms-controller Phase 0 scaffold (broker={host}:{port}). "
        "Wire GameEngine + infra/ in Phase 2."
    )


if __name__ == "__main__":
    app()
