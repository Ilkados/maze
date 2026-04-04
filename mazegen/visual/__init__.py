"""Visual package for the A-Maze-ing maze generator.

Exports all public symbols needed by the main program and maze menu:
configuration loading, color management, logo utilities, display and
animation functions, and terminal helpers.
"""

from mazegen.visual.config import load_config
from mazegen.visual.colors import (
    WALL_COLORS,
    get_wall,
    get_trace,
    get_entry,
    get_exit,
    rotate_wall_color,
)
from mazegen.visual.logo import logo_fits, get_logo_cells
from mazegen.visual.display import display_maze
from mazegen.visual.animation import animate_generation, animate_path
from mazegen.visual.terminal import (
    get_terminal_size,
    check_terminal_size,
    clear_maze_display,
    flush_input,
)

__all__ = [
    "load_config",
    "WALL_COLORS",
    "get_wall",
    "get_trace",
    "get_entry",
    "get_exit",
    "rotate_wall_color",
    "logo_fits",
    "get_logo_cells",
    "display_maze",
    "animate_generation",
    "animate_path",
    "get_terminal_size",
    "check_terminal_size",
    "clear_maze_display",
    "flush_input",
]
