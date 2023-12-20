from pathlib import Path

from typer import Option, Typer

import aoc.day1.run
import aoc.day2.run
import aoc.day3.run
import aoc.day4.run
import aoc.day5.run
import aoc.day6.run
import aoc.day7.run
import aoc.day8.run
import aoc.day9.run
import aoc.day11.run
import aoc.day13.run
import aoc.day14.run

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


@app.command()
def day5(file: Path = Option(...)) -> None:
    aoc.day5.run.run(file)


@app.command()
def day6(file: Path = Option(...)) -> None:
    aoc.day6.run.run(file)


@app.command()
def day7(file: Path = Option(...)) -> None:
    aoc.day7.run.run(file)


@app.command()
def day8(file: Path = Option(...)) -> None:
    aoc.day8.run.run(file)


@app.command()
def day9(file: Path = Option(...)) -> None:
    aoc.day9.run.run(file)


@app.command()
def day11(file: Path = Option(...)) -> None:
    aoc.day11.run.run(file)


@app.command()
def day13(file: Path = Option(...)) -> None:
    aoc.day13.run.run(file)


@app.command()
def day14(file: Path = Option(...)) -> None:
    aoc.day14.run.run(file)


if __name__ == "__main__":
    app()
