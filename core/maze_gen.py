import random
from mazegen.maze import Maze

# Global to store the maze object so solver/writer can access it
_current_maze = None

def generate_maze(rows, cols, entry, exit_, perfect, seed, logo_cells):
    global _current_maze
    
    # 1. Map Visual Size (rows/cols) to Logical Size (w/h)
    # Visual (2N+1) -> Logical (N)
    logic_w = cols // 2
    logic_h = rows // 2
    
    # 2. Setup Seed
    if seed is not None:
        random.seed(seed)
    
    # 3. Create Maze
    maze = Maze(logic_w, logic_h)
    _current_maze = maze
    
    # 4. Handle Logo
    maze.place_42_pattern()
    
    # 5. Map Friend's (row, col) to our (x, y)
    # We use // 2 to make sure a border entry at 0 maps to logical 0
    start_x = entry[1] // 2
    start_y = entry[0] // 2
    
    # Safety clamp: ensure start is within bounds
    start_x = max(0, min(start_x, logic_w - 1))
    start_y = max(0, min(start_y, logic_h - 1))
    
    # 6. Generate and capture steps for animation
    # Note: We need to modify your generator.py to return these steps
    carve_steps_logical = maze.generate(start_x, start_y)
    
    if not perfect:
        maze.make_imperfect()
        
    # 7. Convert logical steps to friend's visual (row, col) steps
    visual_carve_steps = []
    if carve_steps_logical:
        for x, y in carve_steps_logical:
            visual_carve_steps.append((y * 2 + 1, x * 2 + 1))
            
    # 8. Get the character grid for display
    char_grid = maze.get_visual_grid((start_x, start_y), (exit_[1]//2, exit_[0]//2), None)
    
    return char_grid, visual_carve_steps

def find_path(grid, entry, exit_):
    if _current_maze is None: return []
    
    # Map friend's visual (row, col) to our logical (x, y)
    start_xy = (entry[1] // 2, entry[0] // 2)
    end_xy = (exit_[1] // 2, exit_[0] // 2)
    
    path_coords, _ = _current_maze.solve(start_xy, end_xy)
    
    # Convert logical (x, y) path to friend's visual (row, col)
    visual_path = []
    for x, y in path_coords:
        # Add the cell center
        visual_path.append((y * 2 + 1, x * 2 + 1))
    return visual_path

def write_maze_file(grid, path, entry, exit_, filename):
    if _current_maze is None: return
    start_xy = (entry[1] // 2, entry[0] // 2)
    end_xy = (exit_[1] // 2, exit_[0] // 2)
    _, path_str = _current_maze.solve(start_xy, end_xy)
    _current_maze.write_output(filename, start_xy, end_xy, path_str)