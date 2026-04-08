"""
mazegen/generator.py: Logic for carving the maze using iterative DFS.
"""
import random
from typing import TYPE_CHECKING

from .validator import would_create_forbidden_3x3

if TYPE_CHECKING:
    from .maze import Maze


def get_unvisited_neighbors(
    maze: "Maze",
    x: int,
    y: int,
) -> list[tuple[str, int, int]]:
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


def run_dfs_generation(
    maze: "Maze",
    start_x: int = 0,
    start_y: int = 0,
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """Returns a history of moves as (from_cell, to_cell) pairs."""
    start_cell = maze.get_cell(start_x, start_y)
    start_cell.visited = True
    stack: list[tuple[int, int]] = [(start_x, start_y)]
    history: list[tuple[tuple[int, int], tuple[int, int]]] = []

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


def make_imperfect(maze: "Maze") -> list[tuple[int, int]]:
    """
    Randomly removes extra internal walls to create loops (imperfect maze).
    Uses a safety counter and 3x3 validation to remain compliant.

    Returns:
        A list of visual-grid (row, col) positions of the corridor cells
        that were opened, so the animation can reveal them correctly.
    """
    # Target: remove roughly 5% of total potential walls
    extra_walls = (maze.width * maze.height) // 20
    count = 0
    broken_visual: list[tuple[int, int]] = []

    # SAFETY: Prevent infinite loops if the maze is too crowded
    attempts = 0
    max_attempts = extra_walls * 20 if extra_walls > 0 else 20

    while count < extra_walls and attempts < max_attempts:
        attempts += 1

        rx = random.randint(0, maze.width - 2)
        ry = random.randint(0, maze.height - 2)
        direction = random.choice(["E", "S"])

        # 1. Identify the neighbor based on direction
        if direction == "E":
            nx, ny = rx + 1, ry
        else:
            nx, ny = rx, ry + 1

        # 2. RULE: Don't break walls inside or touching the '42' logo
        if maze.is_pattern_cell(rx, ry) or maze.is_pattern_cell(nx, ny):
            continue

        # 3. RULE: Don't break a wall if it's already open
        cell = maze.get_cell(rx, ry)
        is_already_open = (
            (direction == "E" and not cell.east)
            or (direction == "S" and not cell.south)
        )
        if is_already_open:
            continue

        # 4. RULE: Don't break if it creates a forbidden 3x3 open area
        if would_create_forbidden_3x3(maze, rx, ry, direction):
            continue

        # If all checks pass, smash the wall!
        maze.remove_wall(rx, ry, direction)
        count += 1

        # Record the visual corridor cell that was opened
        if direction == "E":
            v_row = ry * 2 + 1
            v_col = rx * 2 + 2
        else:
            v_row = ry * 2 + 2
            v_col = rx * 2 + 1
        broken_visual.append((v_row, v_col))

    return broken_visual
