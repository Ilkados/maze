import random
from mazegen.maze import Maze
from mazegen.solver import path_to_directions

# We use this global to keep track of the last maze object created
_current_maze_obj = None

def generate_maze(rows, cols, entry, exit_, perfect, seed, logo_cells):
    global _current_maze_obj
    if seed is not None:
        random.seed(seed)
    
    # 1. Logic dimensions: friend uses visual size, we need maze size
    # Visual grid is 2N+1. To get N: (Size - 1) // 2
    logic_w = (cols - 1) // 2
    logic_h = (rows - 1) // 2
    
    # 2. Create the Maze Object
    # Friend passes coordinates as (row, col), we use (x, y)
    maze = Maze(logic_w, logic_h)
    _current_maze_obj = maze
    
    # 3. Handle Logo
    maze.place_42_pattern()
    
    # 4. Generate
    # Convert friend's (row, col) entry to our (x, y)
    start_x, start_y = (entry[1] - 1) // 2, (entry[0] - 1) // 2
    maze.generate(start_x, start_y)
    
    if not perfect:
        maze.make_imperfect()
        
    # 5. Return the character grid and a dummy carve_history for now
    char_grid = maze.get_visual_grid((start_x, start_y), None, None)
    return char_grid, [] 

def find_path(grid, entry, exit_):
    global _current_maze_obj
    if _current_maze_obj is None:
        return []
    
    # Convert friend's coordinates to our (x, y)
    start_xy = ((entry[1] - 1) // 2, (entry[0] - 1) // 2)
    end_xy = ((exit_[1] - 1) // 2, (exit_[0] - 1) // 2)
    
    path_coords, _ = _current_maze_obj.solve(start_xy, end_xy)
    
    # Convert our path back to friend's visual (row, col) coordinates
    visual_path = []
    for x, y in path_coords:
        visual_path.append((y * 2 + 1, x * 2 + 1))
    return visual_path

def write_maze_file(grid, path, entry, exit_, filename):
    global _current_maze_obj
    if _current_maze_obj is None:
        return
    
    # Solve to get the directions string (N, E, S, W)
    start_xy = ((entry[1] - 1) // 2, (entry[0] - 1) // 2)
    end_xy = ((exit_[1] - 1) // 2, (exit_[0] - 1) // 2)
    path_coords, path_str = _current_maze_obj.solve(start_xy, end_xy)
    
    # Write the Hex file using your logic
    _current_maze_obj.write_output(filename, start_xy, end_xy, path_str)