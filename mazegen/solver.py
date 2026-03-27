"""
mazegen/solver.py: Logic for finding the shortest path using BFS.
"""
from collections import deque

def run_bfs_solver(maze, entry: tuple[int, int], exit_: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Finds the shortest path from Entry to Exit.
    Returns a list of coordinates [(x1,y1), (x2,y2)...]
    """
    # 1. Setup the Search
    queue = deque([entry])
    visited = {entry}
    # This dictionary is our 'Breadcrumb' trail
    came_from = {entry: None}

    while queue:
        cx, cy = queue.popleft()

        # If we hit the target, we stop immediately!
        if (cx, cy) == exit_:
            break

        current_cell = maze.get_cell(cx, cy)
        
        # We check all 4 neighbors
        # But we only 'see' them if there is NO WALL (False)
        moves = [
            ("N", cx, cy - 1, current_cell.north),
            ("E", cx + 1, cy, current_cell.east),
            ("S", cx, cy + 1, current_cell.south),
            ("W", cx - 1, cy, current_cell.west),
        ]

        for _, nx, ny, wall_exists in moves:
            # Logic: Can we step here?
            if not wall_exists and maze.is_in_bounds(nx, ny) and (nx, ny) not in visited:
                # Page 9: We can't enter the 42 pattern (it's blocked)
                if not maze.is_pattern_cell(nx, ny):
                    visited.add((nx, ny))
                    came_from[(nx, ny)] = (cx, cy)
                    queue.append((nx, ny))

    # 2. Reconstruct the path from Exit back to Entry
    if exit_ not in came_from:
        return [] # No path exists (impossible in a perfect maze, but good to check)

    path = []
    current = exit_
    while current is not None:
        path.append(current)
        current = came_from[current]
    
    path.reverse() # Start -> Exit
    return path


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