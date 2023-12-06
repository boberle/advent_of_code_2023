from pathlib import Path

from typer import Option, Typer

import aoc.day1.run
import aoc.day2.run
import aoc.day3.run
import aoc.day4.run

app = Typer()


@app.command()
def day1(file: Path = Option(...)) -> None:
    aoc.day1.run.run(file)


@app.command()
def day2(file: Path = Option(...)) -> None:
    aoc.day2.run.run(file)


@app.command()
def day3(file: Path = Option(...)) -> None:
    aoc.day3.run.run(file)


@app.command()
def day4(file: Path = Option(...)) -> None:
    aoc.day4.run.run(file)


if __name__ == "__main__":
    app()
