import random
from mazegen.logic.maze import Maze

# Global variable to store the Maze object
_active_maze = None

def generate_maze(rows, cols, entry, exit_, perfect, seed, logo_cells):
    global _active_maze
    if seed is not None:
        random.seed(seed)

    # 1. Calculate Logical Dimensions (e.g., Visual 31x31 -> Logical 15x15)
    logic_w = cols // 2
    logic_h = rows // 2
    maze = Maze(logic_w, logic_h)
    _active_maze = maze
    
    # 2. Map Visual Entry/Exit (row, col) to Logical (x, y)
    # Important: logical X is col//2, logical Y is row//2
    start_xy = (entry[1] // 2, entry[0] // 2)
    end_xy = (exit_[1] // 2, exit_[0] // 2)

    # 3. Clamp coordinates so they are never outside the logical grid
    start_xy = (max(0, min(start_xy[0], logic_w - 1)), max(0, min(start_xy[1], logic_h - 1)))
    end_xy = (max(0, min(end_xy[0], logic_w - 1)), max(0, min(end_xy[1], logic_h - 1)))

    # 4. Align Logo Cells into our logic
    for r, c in logo_cells:
        lx, ly = (c - 1) // 2, (r - 1) // 2
        if maze.is_in_bounds(lx, ly):
            maze.pattern_cells.add((lx, ly))

    # 5. Generate and solve
    # Make sure your generator returns the history of moves
    logical_history = maze.generate(start_xy[0], start_xy[1])
    
    if not perfect:
        maze.make_imperfect()

    # 6. Convert Move History to Visual coordinates for the Animation
    visual_steps = [(start_xy[1] * 2 + 1, start_xy[0] * 2 + 1)]
    # logical_history is a list of ((old_x, old_y), (new_x, new_y))
    for (old_x, old_y), (new_x, new_y) in logical_history:
        # Step into the wall
        visual_steps.append((old_y + new_y + 1, old_x + new_x + 1))
        # Step into the new room
        visual_steps.append((new_y * 2 + 1, new_x * 2 + 1))

    # 7. Create the character grid ('W', ' ', 'E', 'X')
    # We pass the SAME clamped coordinates
    char_grid = maze.get_visual_grid(start_xy, end_xy, None)
    
    return char_grid, visual_steps

def find_path(grid, entry, exit_):
    if _active_maze is None: return []
    
    # 1. Convert friend's visual (row, col) to our logical (x, y)
    # We use // 2 to find the room index. 
    # Example: Visual Col 1 -> 1//2 = 0. Visual Col 3 -> 3//2 = 1.
    start_xy = (entry[1] // 2, entry[0] // 2)
    end_xy = (exit_[1] // 2, exit_[0] // 2)
    
    # 2. Safety Clamp
    start_xy = (max(0, min(start_xy[0], _active_maze.width - 1)), 
                max(0, min(start_xy[1], _active_maze.height - 1)))
    end_xy = (max(0, min(end_xy[0], _active_maze.width - 1)), 
              max(0, min(end_xy[1], _active_maze.height - 1)))
    
    # 3. Solve
    path_coords = _active_maze.solve(start_xy, end_xy)[0] # Get just the list
    
    if not path_coords:
        return []

    # 4. Convert back to VISUAL coordinates (Including the corridors)
    visual_path = []
    for i in range(len(path_coords)):
        x, y = path_coords[i]
        # Current Cell Center (Always odd indices)
        r, c = y * 2 + 1, x * 2 + 1
        visual_path.append((r, c))
        
        # Add the corridor between this cell and the next
        if i < len(path_coords) - 1:
            nx, ny = path_coords[i + 1]
            vr, vc = (y + ny + 1), (x + nx + 1)
            visual_path.append((vr, vc))
            
    return visual_path

def write_maze_file(grid, path, entry, exit_, filename):
    if _active_maze is None: return
    start_xy = (entry[1] // 2, entry[0] // 2)
    end_xy = (exit_[1] // 2, exit_[0] // 2)
    _, path_str = _active_maze.solve(start_xy, end_xy)
    _active_maze.write_output(filename, start_xy, end_xy, path_str)