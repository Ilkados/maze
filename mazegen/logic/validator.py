"""
mazegen/validator.py: Validation helpers for maze rules.
"""

from .cell import Cell


def cells_connected_horizontally(left: Cell, right: Cell) -> bool:
    """Return True if two side-by-side cells are directly connected."""
    return not left.east and not right.west


def cells_connected_vertically(top: Cell, bottom: Cell) -> bool:
    """Return True if two top/bottom cells are directly connected."""
    return not top.south and not bottom.north


def is_fully_open_3x3_block(maze, start_x: int, start_y: int) -> bool:
    """
    Return True if the 3x3 block starting at (start_x, start_y)
    is a forbidden fully open 3x3 area.
    """
    # First collect the 9 cells
    block = []

    for dy in range(3):
        row = []
        for dx in range(3):
            x = start_x + dx
            y = start_y + dy

            if not maze.is_in_bounds(x, y):
                return False

            if maze.is_pattern_cell(x, y):
                return False

            row.append(maze.get_cell(x, y))
        block.append(row)

    # Check all horizontal inner connections
    for row in range(3):
        for col in range(2):
            if not cells_connected_horizontally(block[row][col], block[row][col + 1]):
                return False

    # Check all vertical inner connections
    for row in range(2):
        for col in range(3):
            if not cells_connected_vertically(block[row][col], block[row + 1][col]):
                return False

    return True


def has_forbidden_3x3_area(maze) -> bool:
    """Return True if the maze contains at least one forbidden 3x3 open area."""
    for y in range(maze.height - 2):
        for x in range(maze.width - 2):
            if is_fully_open_3x3_block(maze, x, y):
                return True
    return False

def would_create_forbidden_3x3(maze, x: int, y: int, direction: str) -> bool:
    """
    Return True if opening the wall at (x, y) in the given direction
    would create a forbidden 3x3 open area.
    """
    current = maze.get_cell(x, y)

    if direction == "N":
        nx, ny = x, y - 1
        neighbor = maze.get_cell(nx, ny)

        old_current_wall = current.north
        old_neighbor_wall = neighbor.south

        current.north = False
        neighbor.south = False

        bad = has_forbidden_3x3_area(maze)

        current.north = old_current_wall
        neighbor.south = old_neighbor_wall
        return bad

    elif direction == "E":
        nx, ny = x + 1, y
        neighbor = maze.get_cell(nx, ny)

        old_current_wall = current.east
        old_neighbor_wall = neighbor.west

        current.east = False
        neighbor.west = False

        bad = has_forbidden_3x3_area(maze)

        current.east = old_current_wall
        neighbor.west = old_neighbor_wall
        return bad

    elif direction == "S":
        nx, ny = x, y + 1
        neighbor = maze.get_cell(nx, ny)

        old_current_wall = current.south
        old_neighbor_wall = neighbor.north

        current.south = False
        neighbor.north = False

        bad = has_forbidden_3x3_area(maze)

        current.south = old_current_wall
        neighbor.north = old_neighbor_wall
        return bad

    elif direction == "W":
        nx, ny = x - 1, y
        neighbor = maze.get_cell(nx, ny)

        old_current_wall = current.west
        old_neighbor_wall = neighbor.east

        current.west = False
        neighbor.east = False

        bad = has_forbidden_3x3_area(maze)

        current.west = old_current_wall
        neighbor.east = old_neighbor_wall
        return bad

    else:
        raise ValueError(f"Invalid direction: {direction}")