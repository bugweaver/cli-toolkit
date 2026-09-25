import typer

from .calculator import evaluate
from .converter import convert_units
from .errors import ToolkitError

app = typer.Typer(
    help="Calculate expressions and convert units.",
    add_completion=False,
)


@app.command()
def calc(
    expression: str = typer.Argument(
        help="""Arithmetic expression, for example 2 + 2 * 3."""
    ),
) -> None:
    """Evaluate an arithmetic expression.
    \b
    Example:
        python -m toolkit calc "2 + 2 * 3"
    \u200b"""
    try:
        result = evaluate(expression)
    except ToolkitError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=2)
    typer.echo(result)


@app.command()
def convert(
    value: float = typer.Argument(help="Numeric value to convert."),
    from_unit: str = typer.Option(
        ..., "--from", help="Source unit: mm, cm, m, km, g, kg, c, f, k."
    ),
    to_unit: str = typer.Option(..., "--to", help="Target unit from the same group."),
) -> None:
    """Convert a value between units.
    \b
    Example:
        python -m toolkit convert 1500 --from m --to km
    """
    try:
        result = convert_units(value, from_unit, to_unit)
    except ToolkitError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=2)
    typer.echo(result)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
