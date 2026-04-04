"""
mazegen/solver.py: Logic for finding the shortest path using BFS.
"""
from collections import deque

def run_bfs_solver(maze, entry: tuple[int, int], exit_: tuple[int, int]) -> list[tuple[int, int]]:
    # Safety: If entry or exit are logo cells, no path is possible
    if maze.is_pattern_cell(*entry) or maze.is_pattern_cell(*exit_):
        print("[DEBUG] Entry or Exit is inside the 42 logo!")
        return []

    queue = deque([entry])
    visited = {entry}
    came_from = {entry: None}

    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) == exit_:
            break

        current_cell = maze.get_cell(cx, cy)
        # N, E, S, W checks
        moves = [
            (cx, cy - 1, current_cell.north),
            (cx + 1, cy, current_cell.east),
            (cx, cy + 1, current_cell.south),
            (cx - 1, cy, current_cell.west),
        ]

        for nx, ny, wall_exists in moves:
            if not wall_exists and maze.is_in_bounds(nx, ny) and (nx, ny) not in visited:
                if not maze.is_pattern_cell(nx, ny):
                    visited.add((nx, ny))
                    came_from[(nx, ny)] = (cx, cy)
                    queue.append((nx, ny))

    if exit_ not in came_from:
        print(f"[DEBUG] Solver failed: No path from {entry} to {exit_}")
        return []

    path = []
    curr = exit_
    while curr is not None:
        path.append(curr)
        curr = came_from[curr]
    return path[::-1]


def path_to_directions(path: list[tuple[int, int]]) -> str:
    """
    Exactly your logic: Converts [(0,0), (1,0)] to 'E'.
    """
    if len(path) < 2:
        return ""
    
    result = []
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        
        if y2 < y1: result.append("N")
        elif x2 > x1: result.append("E")
        elif y2 > y1: result.append("S")
        elif x2 < x1: result.append("W")
        
    return "".join(result)