"""
Maze Generator Module.

This module provides a reusable MazeGenerator class that generates mazes
using the Recursive Backtracker (DFS) algorithm. It supports perfect mazes,
seeded randomness, and embeds a fixed "42" pattern in the center.

Example usage:
    from mazegen import MazeGenerator

    gen = MazeGenerator(width=20, height=15, seed=42, perfect=True)
    gen.generate(entry=(0, 0), exit_=(19, 14))
    print(gen.grid)           # 2D list of wall bitmasks
    print(gen.solution)       # list of 'N','E','S','W' directions
    print(gen.solution_path)  # list of (x, y) coordinates
"""

import random
import collections
from typing import List, Tuple, Optional, Set

WEST: int = 0b1000
SOUTH: int = 0b0100
EAST: int = 0b0010
NORTH: int = 0b0001

DELTA: dict = {
    WEST: (-1, 0),
    SOUTH: (0, 1),
    EAST: (1, 0),
    NORTH: (0, -1)
}

OPPOSIT: dict = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
}

DIR_CHAR: dict = {
    NORTH: 'N',
    EAST: 'E',
    SOUTH: 'S',
    WEST: 'W',
}

# ── Fixed "42" pixel font  (5 rows × 3 cols each digit) ──────────────────────
# 'X' = solid (fully-closed wall cell), '.' = open passage
COORD_42: set[tuple[int, int]] = {
    # The '4'
    (0, 0),
    (0, 1),
    (0, 2), (1, 2), (2, 2),
                    (2, 3),
                    (2, 4),

    # The '2'
    (4, 0), (5, 0), (6, 0),
                    (6, 1),
    (4, 2), (5, 2), (6, 2),
    (4, 3),
    (4, 4), (5, 4), (6, 4)
}


class MazeGenerator:
    """
    Generates a maze using the Recursive Backtracker (DFS) algorithm.

    The maze is represented as a 2D grid where each cell stores a bitmask
    indicating which walls are CLOSED (1 = closed, 0 = open):
        bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West

    A fixed "42" pattern made of fully-closed cells (0xF) is embedded
    in the exact centre of every generated maze.

    Attributes:
        width (int): Number of columns.
        height (int): Number of rows.
        seed (Optional[int]): Random seed for reproducibility.
        perfect (bool): If True, generates a perfect maze (single path).
        grid (List[List[int]]): 2D grid of wall bitmasks after generation.
        solution (List[str]): Shortest path directions ('N','E','S','W').
        solution_path (List[Tuple[int,int]]): Coordinates along the solution.
        entry (Tuple[int,int]): Entry cell (x, y).
        exit (Tuple[int,int]): Exit cell (x, y).
        cells_42 (Set[Tuple[int,int]]): Grid coords occupied by the pattern.
        pattern_fits (bool): False when the maze is too small for the pattern.
    """

    def __init__(
        self,
        width: int = 20,
        height: int = 15,
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        """
        Initialize the MazeGenerator.

        Args:
            width: Number of columns (cells). Must be >= 2.
            height: Number of rows (cells). Must be >= 2.
            seed: Optional random seed for reproducibility.
            perfect: Whether to generate a perfect maze.

        Raises:
            ValueError: If width or height is less than 2.
        """
        if width < 2 or height < 2:
            raise ValueError("Width and height must be at least 2.")
        self.width: int = width
        self.height: int = height
        self.seed: Optional[int] = seed
        self.perfect: bool = perfect
        self.grid: List[List[int]] = []
        self.solution: List[str] = []
        self.solution_path: List[Tuple[int, int]] = []
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (width - 1, height - 1)
        self.cells_42: Set[Tuple[int, int]] = set()
        self.pattern_fits: bool = False
        self._rng: random.Random = random.Random(seed)

    # ── Public API ─────────────────────────────────────────────────────

    def generate(
        self,
        entry: Optional[Tuple[int, int]] = None,
        exit_: Optional[Tuple[int, int]] = None,
    ) -> None:
        """
        Generate the maze.

        The "42" pattern is embedded in the exact centre BEFORE maze carving,
        so the DFS carver naturally routes around it — the pattern is always
        complete and consistent, regardless of the random seed.

        Args:
            entry: Entry cell as (x, y). Defaults to (0, 0).
            exit_: Exit cell as (x, y). Defaults to (width-1, height-1).

        Raises:
            ValueError: If entry/exit are out of bounds or identical.
        """
        if entry is not None:
            self.entry = entry
        if exit_ is not None:
            self.exit = exit_

        self._validate_entry_exit()

        # Reset RNG for reproducibility
        self._rng = random.Random(self.seed)

        # ── Step 1: initialise grid (all walls closed)
        self.grid = [[0xF] * self.width for _ in range(self.height)]

        # ── Step 2: compute and reserve the 42 pattern cells
        self.cells_42 = set()
        self.pattern_fits = False
        self._reserve_42_pattern()

        # Step 3: carve passages (DFS — skips reserved 42 cells)
        self._carve_passages(self.entry[0], self.entry[1])

        # ── Step 4: enforce outer border wall

        # ── Step 5: add loops for non-perfect mazes
        if not self.perfect:
            self._add_loops()

        # ── Step 6: fix wall coherence around 42 cells
        #    Neighbours of 42 cells must have their shared wall CLOSED
        self._seal_42_neighbours()

        # Validate connectivity
        self._validate_full_connectivity()
        # ── Step 7: solve
        self.solution, self.solution_path = self._solve_bfs()
        self._validate_perfect()

    def get_hex_grid(self) -> List[str]:
        """
        Return the maze grid as a list of hex strings (one per row).

        Returns:
            List of strings, each containing hex digits for a row.
        """
        return [
            "".join(format(cell, 'X') for cell in row)
            for row in self.grid
        ]

    # ── Private helpers ───────────────────────────────────────────────
    def _validate_entry_exit(self) -> None:
        """Raise ValueError for invalid entry/exit coordinates."""
        ex, ey = self.entry
        xx, xy = self.exit
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            raise ValueError(f"Entry {self.entry} is out of maze bounds.")
        if not (0 <= xx < self.width and 0 <= xy < self.height):
            raise ValueError(f"Exit {self.exit} is out of maze bounds.")
        if self.entry == self.exit:
            raise ValueError("Entry and exit must be different.")

    def _reserve_42_pattern(self) -> None:
        """
        Mark the centre cells for the '42' pattern as fully closed (0xF).

        The pattern is centred horizontally and vertically.  If the maze is
        too small to fit the pattern with a 3-cell margin, the flag
        `self.pattern_fits` stays False and no cells are reserved.
        """
        if self.width < 9 or self.height < 7:
            print("skip generating the 42 shield")
            return
        center_x: int = self.width // 2
        center_y: int = self.height // 2
        start_x: int = center_x - 3
        start_y: int = center_y - 2
        for (x, y) in COORD_42:
            dynamic_x: int = start_x + x
            dynamic_y: int = start_y + y
            self.cells_42.add((dynamic_x, dynamic_y))
        if self.entry in self.cells_42 or self.exit in self.cells_42:
            self.pattern_fits = False
            return
        self.pattern_fits = True

    def _carve_passages(self, cx: int, cy: int) -> None:
        """
        Recursive backtracker DFS — skips fully-closed (42) cells.

        Args:
            cx: Current x position.
            cy: Current y position.
        """
        directions: list = [WEST, SOUTH, EAST, NORTH]
        random.shuffle(directions)
        for direction in directions:
            dx, dy = DELTA[direction]
            nx = cx + dx
            ny = cy + dy
            if (0 <= nx < self.width and 0 <= ny < self.height and
               self.grid[ny][nx] == 15 and (nx, ny) not in self.cells_42):
                self.grid[cy][cx] &= ~direction
                self.grid[ny][nx] &= ~OPPOSIT[direction]
                self._carve_passages(nx, ny)

    def _seal_42_neighbours(self) -> None:
        """
        For every cell adjacent to a 42-pattern cell, close the shared wall.

        This ensures wall-data coherence: if cell A is 0xF, its neighbour B
        must also have the wall on the shared side closed.
        """
        for cx, cy in self.cells_42:
            for direction, (ddx, ddy) in DELTA.items():
                nx, ny = cx + ddx, cy + ddy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # Close the wall on the neighbour's side facing the 42 cell
                    self.grid[ny][nx] |= OPPOSIT[direction]

    def _add_loops(self) -> None:
        """Remove ~15% of interior walls to create a non-perfect maze."""
        walls_to_remove = int(self.width * self.height * 0.15)
        attempts = 0
        removed = 0
        while removed < walls_to_remove and attempts < walls_to_remove * 10:
            attempts += 1
            x = self._rng.randint(1, self.width - 2)
            y = self._rng.randint(1, self.height - 2)
            direction = self._rng.choice([EAST, SOUTH])
            dx, dy = DELTA[direction]
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (x, y) in self.cells_42 or (nx, ny) in self.cells_42:
                    continue
                if self.grid[y][x] & direction:
                    self.grid[y][x] &= ~direction
                    self.grid[ny][nx] &= ~OPPOSIT[direction]
                    removed += 1

    def _solve_bfs(self) -> Tuple[List[str], List[Tuple[int, int]]]:
        """
        Find shortest path from entry to exit using BFS.

        Returns:
            A tuple (directions, path) where directions is a list of
            'N','E','S','W' characters and path is a list of (x,y) tuples.
        """
        ex, ey = self.entry
        xx, xy = self.exit

        queue: collections.deque = collections.deque()
        queue.append((ex, ey))
        came_from: dict = {(ex, ey): None}
        dir_from: dict = {}

        while queue:
            cx, cy = queue.popleft()
            if (cx, cy) == (xx, xy):
                break
            for direction in [NORTH, EAST, SOUTH, WEST]:
                if self.grid[cy][cx] & direction:
                    continue  # wall is closed
                ddx, ddy = DELTA[direction]
                nx, ny = cx + ddx, cy + ddy
                if (0 <= nx < self.width and 0 <= ny < self.height
                        and (nx, ny) not in came_from):
                    came_from[(nx, ny)] = (cx, cy)
                    dir_from[(nx, ny)] = DIR_CHAR[direction]
                    queue.append((nx, ny))

        if (xx, xy) not in came_from:
            return [], []

        path: List[Tuple[int, int]] = []
        directions: List[str] = []
        current: Optional[Tuple[int, int]] = (xx, xy)
        while current is not None:
            path.append(current)
            prev = came_from[current]
            if prev is not None:
                directions.append(dir_from[current])
            current = prev

        path.reverse()
        directions.reverse()
        return directions, path

    def generate_stepwise(self):
        """
        Generator version of DFS carving.
        Yields (cx, cy) at each carving step for animation.
        """

        self.grid = [[0xF] * self.width for _ in range(self.height)]
        self._rng = random.Random(self.seed)
        self.cells_42 = set()
        self.pattern_fits = False
        self._reserve_42_pattern()

        stack = [self.entry]
        visited = {self.entry}

        while stack:
            cx, cy = stack[-1]
            yield cx, cy  # <-- animation step

            dirs = [NORTH, EAST, SOUTH, WEST]
            self._rng.shuffle(dirs)

            carved = False
            for direction in dirs:
                dx, dy = DELTA[direction]
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) in visited:
                        continue
                    if (nx, ny) in self.cells_42:
                        continue

                    self.grid[cy][cx] &= ~direction
                    self.grid[ny][nx] &= ~OPPOSIT[direction]

                    stack.append((nx, ny))
                    visited.add((nx, ny))
                    carved = True
                    break

            if not carved:
                stack.pop()
        self._seal_42_neighbours()
        self.solution, self.solution_path = self._solve_bfs()

    # ── Legacy compatibility (old attribute names) ──────────────────────

    @property
    def _42_cells(self) -> List[Tuple[int, int]]:
        """Compatibility shim: list of (x,y) for the 42 pattern cells."""
        return list(self.cells_42)

    @property
    def _42_fits(self) -> bool:
        """Compatibility shim."""
        return self.pattern_fits

    def _validate_full_connectivity(self) -> None:
        """Ensure every non-42 cell is reachable from entry."""
        visited = set()
        stack = [self.entry]

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))

            for direction, (dx, dy) in DELTA.items():
                if self.grid[cy][cx] & direction:
                    continue
                nx, ny = cx + dx, cy + dy
                if (0 <= nx < self.width and 0 <= ny < self.height
                        and (nx, ny) not in self.cells_42):
                    stack.append((nx, ny))

        walkable = {
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in self.cells_42
        }

        if visited != walkable:
            raise ValueError("Generated maze is not fully connected.")

    def _validate_perfect(self) -> None:
        """Ensure a unique path exists between entry and exit."""
        if not self.perfect:
            return

        paths = 0
        stack = [(self.entry, set())]

        while stack:
            (cx, cy), visited = stack.pop()

            if (cx, cy) == self.exit:
                paths += 1
                if paths > 1:
                    raise ValueError("Maze is not perfect (multiple paths).")
                continue

            for direction, (dx, dy) in DELTA.items():
                if self.grid[cy][cx] & direction:
                    continue

                nx, ny = cx + dx, cy + dy

                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                if (nx, ny) in visited:
                    continue
                if (nx, ny) in self.cells_42:
                    continue

                stack.append(((nx, ny), visited | {(cx, cy)}))
