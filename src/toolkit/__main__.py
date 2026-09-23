import typer

from .calculator import evaluate

app = typer.Typer()

@app.command()
def calc(expression: str) -> None:
    try:
        result = evaluate(expression)
    except (ValueError, ZeroDivisionError) as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=2)
    typer.echo(result)

def main() -> None:
    app()

if __name__ == "__main__":
    main()
