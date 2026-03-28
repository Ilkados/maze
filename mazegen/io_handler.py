"""
mazegen/io_handler.py: Handles file writing and terminal visualization.
"""
from .constants import WALL_BITS

def cell_to_hex(cell) -> str:
    """Converts wall states to a Hex digit (N:1, E:2, S:4, W:8)."""
    value = 0
    if cell.north: value |= WALL_BITS["N"]
    if cell.east:  value |= WALL_BITS["E"]
    if cell.south: value |= WALL_BITS["S"]
    if cell.west:  value |= WALL_BITS["W"]
    return format(value, "X")

def write_hex_file(maze, filename: str, entry: tuple[int, int], exit_: tuple[int, int], path_str: str) -> None:
    """Writes the mandatory hex format to a file."""
    lines = []
    for row in maze.grid:
        lines.append("".join(cell_to_hex(cell) for cell in row))
    
    lines.append("") # Empty line
    lines.append(f"ENTRY={entry[0]},{entry[1]}")
    lines.append(f"EXIT={exit_[0]},{exit_[1]}")
    lines.append(f"PATH={path_str}")

    with open(filename, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")

def to_visual_grid(maze, entry: tuple[int, int], exit_: tuple[int, int], path: list[tuple[int, int]] = None) -> list[list[str]]:
    """Creates a 2D character map (2N+1 size)."""
    v_height = maze.height * 2 + 1
    v_width = maze.width * 2 + 1
    grid = [["W" for _ in range(v_width)] for _ in range(v_height)]
    
    path_set = set(path) if path else set()

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
            elif (x, y) in path_set:
                grid[vy][vx] = "P"
            else:
                grid[vy][vx] = " "

            # Remove visual walls where logic walls are False
            if not cell.north: grid[vy - 1][vx] = " "
            if not cell.east:  grid[vy][vx + 1] = " "
            if not cell.south: grid[vy + 1][vx] = " "
            if not cell.west:  grid[vy][vx - 1] = " "
    return grid