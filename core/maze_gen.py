import random
from mazegen.maze import Maze

# Global to store the maze object so solver/writer can access it
_current_maze = None

def generate_maze(rows, cols, entry, exit_, perfect, seed, logo_cells):
    global _current_maze
    
    # 1. Map Visual Size to Logical Size
    logic_w = cols // 2
    logic_h = rows // 2
    
    if seed is not None:
        random.seed(seed)
    
    maze = Maze(logic_w, logic_h)
    _current_maze = maze
    
    # 2. Add Logo cells to your logic's pattern set
    for r, c in logo_cells:
        lx, ly = (c - 1) // 2, (r - 1) // 2
        if maze.is_in_bounds(lx, ly):
            maze.pattern_cells.add((lx, ly))
    
    # 3. Map friend's visual start to logical start
    start_x = entry[1] // 2
    start_y = entry[0] // 2
    
    # 4. RUN GENERATION
    # This returns the sequence of (row, col) in the character grid
    visual_carve_steps = maze.generate(start_x, start_y)
    
    if not perfect:
        maze.make_imperfect()
            
    # 5. Get the character grid for display
    # We use your logic to build the 'W', ' ', 'E', 'X' grid
    char_grid = maze.get_visual_grid((start_x, start_y), (exit_[1]//2, exit_[0]//2), None)
    
    return char_grid, visual_carve_steps

def find_path(grid, entry, exit_):
    if _current_maze is None: return []
    start_xy = (entry[1] // 2, entry[0] // 2)
    end_xy = (exit_[1] // 2, exit_[0] // 2)
    path_coords, _ = _current_maze.solve(start_xy, end_xy)
    
    # Convert logical path to visual grid coordinates
    visual_path = []
    for x, y in path_coords:
        visual_path.append((y * 2 + 1, x * 2 + 1))
    return visual_path

def write_maze_file(grid, path, entry, exit_, filename):
    if _current_maze is None: return
    start_xy = (entry[1] // 2, entry[0] // 2)
    end_xy = (exit_[1] // 2, exit_[0] // 2)
    _, path_str = _current_maze.solve(start_xy, end_xy)
    _current_maze.write_output(filename, start_xy, end_xy, path_str)