"""Static maze display module for terminal rendering."""

from typing import Optional

from visual.colors import (
    BORDER,
    C_ENTRY,
    C_EXIT,
    C_PATH,
    C_LOGO,
    C_VOID,
    get_wall,
)
from visual.terminal import check_terminal_size


def display_maze(
    maze: list[list[str]],
    show_path: bool = False,
    path: Optional[list[tuple[int, int]]] = None,
    logo_cells: Optional[set[tuple[int, int]]] = None,
) -> None:
    """Render the maze as a static image in the terminal."""
    rows = len(maze)
    cols = len(maze[0]) if rows > 0 else 0
    check_terminal_size(rows, cols)

    # Fetch the current wall color from the theme
    wall_color = get_wall()
    
    # Convert path and logo to sets for high-speed checking
    path_set: set[tuple[int, int]] = set(path) if path is not None else set()
    logo_set: set[tuple[int, int]] = logo_cells if logo_cells is not None else set()

    # Draw Top Border
    for r, row in enumerate(maze):
        line = BORDER # Start with the left border
        for c, char in enumerate(row):
            
            # 1. ALWAYS show Entry and Exit colors first (Highest Priority)
            if char == 'E':
                line += C_ENTRY  # Always Green
            elif char == 'X':
                line += C_EXIT   # Always Red
            
            # 2. Show the 42 Logo (Second Priority)
            elif (r, c) in logo_set:
                line += C_LOGO   # Always Yellow
            
            # 3. Show the Path ONLY if show_path is True (Third Priority)
            # This will fill the corridors and cells between E and X
            elif show_path and (r, c) in path_set:
                line += C_PATH   # Always Blue
            
            # 4. Show the Walls
            elif char == 'W':
                line += wall_color
            
            # 5. Everything else is empty space
            else:
                line += C_VOID
                
        line += BORDER # End with the right border
        print(line)