"""
mazegen/generator.py: Logic for carving the maze using iterative DFS.
"""
import random
from .validator import would_create_forbidden_3x3
def get_unvisited_neighbors(maze, x: int, y: int) -> list[tuple[str, int, int]]:
    """
    Exactly your logic: Finds valid neighbors that haven't been visited 
    and are NOT part of the '42' pattern.
    """
    unvisited_neighbors: list[tuple[str, int, int]] = []

    # Calls the neighbors function from your Maze/Geometry logic
    for direction, neighbor_x, neighbor_y in maze.get_neighbors(x, y):
        # Skip cells that are part of the '42' logo
        if maze.is_pattern_cell(neighbor_x, neighbor_y):
            continue

        neighbor = maze.get_cell(neighbor_x, neighbor_y)
        if not neighbor.visited:
            unvisited_neighbors.append((direction, neighbor_x, neighbor_y))

    return unvisited_neighbors


def run_dfs_generation(maze, start_x: int = 0, start_y: int = 0) -> None:
    """
    Exactly your logic: Generate the maze using a stack (Iterative DFS).
    This prevents recursion depth issues.
    """
    # 1. Bounds check (graceful error handling for 42 subject)
    if not maze.is_in_bounds(start_x, start_y):
        raise ValueError("Starting cell is outside maze bounds")

    # 2. Setup starting point
    start_cell = maze.get_cell(start_x, start_y)
    start_cell.visited = True
    
    # 3. Your Stack-based loop
    stack: list[tuple[int, int]] = [(start_x, start_y)]

    while stack:
        current_x, current_y = stack[-1]
        unvisited = get_unvisited_neighbors(maze, current_x, current_y)

        if unvisited:
            # Pick a random unvisited neighbor
            direction, next_x, next_y = random.choice(unvisited)

            # Carve the passage (removes walls in both cells)
            maze.remove_wall(current_x, current_y, direction)
             # Move into the neighbor
            next_cell = maze.get_cell(next_x, next_y)
            next_cell.visited = True
            stack.append((next_x, next_y))
        else:
            # No neighbors left: pop from stack to backtrack
            stack.pop()

def make_imperfect(maze) -> None:
    """
    Randomly removes extra walls to create loops, 
    with a safety counter to prevent infinite loops.
    """
    # Target number of walls to remove (e.g., 5% of total cells)
    extra_walls = (maze.width * maze.height) // 20
    count = 0
    
    # SAFETY COUNTER (The part you added)
    attempts = 0
    max_attempts = extra_walls * 20 if extra_walls > 0 else 20

    # The loop now checks BOTH: 
    # 1. Did we reach our goal (count)? 
    # 2. Are we trying too hard (attempts)?
    while count < extra_walls and attempts < max_attempts:
        attempts += 1 # Every loop costs one attempt
        
        rx = random.randint(0, maze.width - 2)
        ry = random.randint(0, maze.height - 2)
        direction = random.choice(["E", "S"])

        if direction == "E":
            nx, ny = rx + 1, ry
        else:
            nx, ny = rx, ry + 1

        # 1. Skip if it's the logo
        if maze.is_pattern_cell(rx, ry) or maze.is_pattern_cell(nx, ny):
            continue
            
        # 2. Skip if it would create a 3x3 open area (from validator.py)
        if would_create_forbidden_3x3(maze, rx, ry, direction):
            continue

        # 3. Skip if the wall is already open (no point in "removing" it again)
        # We only count it if we actually changed something.
        current_cell = maze.get_cell(rx, ry)
        is_already_open = (direction == "E" and not current_cell.east) or \
                          (direction == "S" and not current_cell.south)
        
        if is_already_open:
            continue

        # If we passed all checks, remove the wall!
        maze.remove_wall(rx, ry, direction)
        count += 1 # We successfully removed a wall