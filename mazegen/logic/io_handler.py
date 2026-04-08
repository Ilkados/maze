from typing import TYPE_CHECKING

from .cell import Cell
from .constants import WALL_BITS

if TYPE_CHECKING:
    from .maze import Maze


def cell_to_hex(cell: Cell) -> str:
    value = 0
    if cell.north:
        value |= WALL_BITS["N"]
    if cell.east:
        value |= WALL_BITS["E"]
    if cell.south:
        value |= WALL_BITS["S"]
    if cell.west:
        value |= WALL_BITS["W"]
    return format(value, "X")


def write_hex_file(
    maze: "Maze",
    filename: str,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path_str: str,
) -> None:
    lines: list[str] = []
    for row in maze.grid:
        lines.append("".join(cell_to_hex(cell) for cell in row))

    lines.append("")
    lines.append(f"ENTRY={entry[0]},{entry[1]}")
    lines.append(f"EXIT={exit_[0]},{exit_[1]}")
    lines.append(f"PATH={path_str}")

    with open(filename, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")


def to_visual_grid(
    maze: "Maze",
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: list[tuple[int, int]] | None = None,
) -> list[list[str]]:
    v_height = maze.height * 2 + 1
    v_width = maze.width * 2 + 1
    grid = [["W" for _ in range(v_width)] for _ in range(v_height)]

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            vx, vy = x * 2 + 1, y * 2 + 1

            if maze.is_pattern_cell(x, y):
                grid[vy][vx] = "#"
            elif (x, y) == entry:
                grid[vy][vx] = "E"
            elif (x, y) == exit_:
                grid[vy][vx] = "X"
            elif maze.get_cell(x, y).visited:
                grid[vy][vx] = " "
            else:
                grid[vy][vx] = "W"

            if not cell.north:
                grid[vy - 1][vx] = " "
            if not cell.east:
                grid[vy][vx + 1] = " "
            if not cell.south:
                grid[vy + 1][vx] = " "
            if not cell.west:
                grid[vy][vx - 1] = " "

    return grid
