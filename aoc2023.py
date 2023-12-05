from pathlib import Path

from typer import Option, Typer

import aoc.day1.run
import aoc.day2.run

app = Typer()


@app.command()
def day1(file: Path = Option(...)) -> None:
    aoc.day1.run.run(file)


@app.command()
def day2(file: Path = Option(...)) -> None:
    aoc.day2.run.run(file)


if __name__ == "__main__":
    app()
