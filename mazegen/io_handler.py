from .constants import WALL_BITS

def cell_to_hex(cell) -> str:
    value = 0
    if cell.north: value |= WALL_BITS["N"]
    if cell.east:  value |= WALL_BITS["E"]
    if cell.south: value |= WALL_BITS["S"]
    if cell.west:  value |= WALL_BITS["W"]
    return format(value, "X")

def write_hex_file(maze, filename: str, entry: tuple[int, int], exit_: tuple[int, int], path_str: str) -> None:
    lines = []
    for row in maze.grid:
        lines.append("".join(cell_to_hex(cell) for cell in row))
    lines.append("")
    lines.append(f"ENTRY={entry[0]},{entry[1]}")
    lines.append(f"EXIT={exit_[0]},{exit_[1]}")
    lines.append(f"PATH={path_str}")
    with open(filename, "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")
def to_visual_grid(maze, entry, exit_, path=None) -> list[list[str]]:
    v_height = maze.height * 2 + 1
    v_width = maze.width * 2 + 1
    grid = [["W" for _ in range(v_width)] for _ in range(v_height)]
    
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            vx, vy = x * 2 + 1, y * 2 + 1

            # Inside to_visual_grid in io_handler.py
            if maze.is_pattern_cell(x, y):
                grid[vy][vx] = "#"  # Logo is a wall
            elif (x, y) == entry:
                grid[vy][vx] = 'E'
            elif (x, y) == exit_:
                grid[vy][vx] = 'X'
            elif maze.get_cell(x, y).visited:
                grid[vy][vx] = ' ' # Path
            else:
                grid[vy][vx] = 'W' # <--- IMPORTANT: If not visited, it is a WALL!

            # Open visual walls based on logic booleans
            if not cell.north: grid[vy - 1][vx] = ' '
            if not cell.east:  grid[vy][vx + 1] = ' '
            if not cell.south: grid[vy + 1][vx] = ' '
            if not cell.west:  grid[vy][vx - 1] = ' '
    return grid