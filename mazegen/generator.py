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
def run_dfs_generation(maze, start_x: int = 0, start_y: int = 0) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """Returns a history of moves as (from_cell, to_cell) pairs."""
    start_cell = maze.get_cell(start_x, start_y)
    start_cell.visited = True
    stack = [(start_x, start_y)]
    history = [] # Stores logical move pairs

    while stack:
        cx, cy = stack[-1]
        unvisited = get_unvisited_neighbors(maze, cx, cy)

        if unvisited:
            direction, nx, ny = random.choice(unvisited)
            
            # Record the move: from (cx, cy) to (nx, ny)
            history.append(((cx, cy), (nx, ny)))
            
            maze.remove_wall(cx, cy, direction)
            next_cell = maze.get_cell(nx, ny)
            next_cell.visited = True
            stack.append((nx, ny))
        else:
            stack.pop()
    return history