# mazegen/maze.py

from .cell import Cell
from .constants import PATTERN_42, LOGO_WIDTH, LOGO_HEIGHT
from . import geometry
from . import generator
from . import io_handler
from . import solver

class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(width)] for _ in range(height)
        ]
        self.pattern_cells: set[tuple[int, int]] = set()

    def get_cell(self, x: int, y: int) -> Cell:
        if not self.is_in_bounds(x, y):
            raise ValueError(f"Cell coordinate ({x}, {y}) is outside the maze bounds")
        return self.grid[y][x]

    def is_in_bounds(self, x: int, y: int) -> bool:
        return geometry.is_in_bounds(self.width, self.height, x, y)

    def is_pattern_cell(self, x: int, y: int) -> bool:
        return (x, y) in self.pattern_cells

    def place_42_pattern(self) -> None:
        self.pattern_cells.clear()
        if self.width < LOGO_WIDTH or self.height < LOGO_HEIGHT:
            return
        start_x = (self.width - LOGO_WIDTH) // 2
        start_y = (self.height - LOGO_HEIGHT) // 2
        for lx, ly in PATTERN_42:
            self.pattern_cells.add((start_x + lx, start_y + ly))

    def get_neighbors(self, x: int, y: int):
        return geometry.get_neighbors(self, x, y)

    def remove_wall(self, x: int, y: int, direction: str):
        geometry.remove_wall(self, x, y, direction)

    def generate(self, start_x: int = 0, start_y: int = 0):
        """Calls your generator logic and returns the animation history."""
        return generator.run_dfs_generation(self, start_x, start_y)
    def make_imperfect(self):
        generator.make_imperfect(self)
        
    def solve(self, entry: tuple[int, int], exit_: tuple[int, int]):
        path = solver.run_bfs_solver(self, entry, exit_)
        path_str = solver.path_to_directions(path)
        return path, path_str

    def write_output(self, filename, entry, exit, path_str):
        io_handler.write_hex_file(self, filename, entry, exit, path_str)
        
    def get_visual_grid(self, entry, exit_, path):
        """Asks io_handler.py for a character map."""
        return io_handler.to_visual_grid(self, entry, exit_, path)