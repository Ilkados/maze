"""
mazegen/geometry.py: Your source code logic for grid math.
"""

def is_in_bounds(width: int, height: int, x: int, y: int) -> bool:
    """Check whether a coordinate is inside the maze."""
    return 0 <= x < width and 0 <= y < height


def get_neighbors(maze, x: int, y: int) -> list[tuple[str, int, int]]:
    """Return all valid neighbors of the cell at (x, y)."""
    neighbors = []

    # Your exact candidate list
    candidates = [
        ("N", x, y - 1),
        ("E", x + 1, y),
        ("S", x, y + 1),
        ("W", x - 1, y),
    ]

    for direction, neighbor_x, neighbor_y in candidates:
        if is_in_bounds(maze.width, maze.height, neighbor_x, neighbor_y):
            neighbors.append((direction, neighbor_x, neighbor_y))

    return neighbors


def remove_wall(maze, x: int, y: int, direction: str) -> None:
    """Your exact logic for removing walls with error handling."""
    current = maze.get_cell(x, y)

    if direction == "N":
        neighbor_x, neighbor_y = x, y - 1
        if not is_in_bounds(maze.width, maze.height, neighbor_x, neighbor_y):
            raise ValueError("North neighbor is outside maze bounds")
        neighbor = maze.get_cell(neighbor_x, neighbor_y)
        current.north = False
        neighbor.south = False

    elif direction == "E":
        neighbor_x, neighbor_y = x + 1, y
        if not is_in_bounds(maze.width, maze.height, neighbor_x, neighbor_y):
            raise ValueError("East neighbor is outside maze bounds")
        neighbor = maze.get_cell(neighbor_x, neighbor_y)
        current.east = False
        neighbor.west = False

    elif direction == "S":
        neighbor_x, neighbor_y = x, y + 1
        if not is_in_bounds(maze.width, maze.height, neighbor_x, neighbor_y):
            raise ValueError("South neighbor is outside maze bounds")
        neighbor = maze.get_cell(neighbor_x, neighbor_y)
        current.south = False
        neighbor.north = False

    elif direction == "W":
        neighbor_x, neighbor_y = x - 1, y
        if not is_in_bounds(maze.width, maze.height, neighbor_x, neighbor_y):
            raise ValueError("West neighbor is outside maze bounds")
        neighbor = maze.get_cell(neighbor_x, neighbor_y)
        current.west = False
        neighbor.east = False

    else:
        raise ValueError(f"Invalid direction: {direction}")