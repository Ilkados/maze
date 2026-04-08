import random
from mazegen.logic.maze import Maze


_active_maze: Maze | None = None


def generate_maze(
    rows: int,
    cols: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    perfect: bool,
    seed: int | None,
    logo_cells: list[tuple[int, int]],
) -> tuple[list[list[str]], list[tuple[int, int]]]:
    global _active_maze

    if seed is not None:
        random.seed(seed)

    logic_w = cols // 2
    logic_h = rows // 2
    maze = Maze(logic_w, logic_h)
    _active_maze = maze

    start_xy = (entry[1] // 2, entry[0] // 2)
    end_xy = (exit_[1] // 2, exit_[0] // 2)

    start_xy = (
        max(0, min(start_xy[0], logic_w - 1)),
        max(0, min(start_xy[1], logic_h - 1)),
    )
    end_xy = (
        max(0, min(end_xy[0], logic_w - 1)),
        max(0, min(end_xy[1], logic_h - 1)),
    )

    for r, c in logo_cells:
        lx, ly = (c - 1) // 2, (r - 1) // 2
        if maze.is_in_bounds(lx, ly):
            maze.pattern_cells.add((lx, ly))

    logical_history = maze.generate(start_xy[0], start_xy[1])

    imperfect_visual_steps: list[tuple[int, int]] = []
    if not perfect:
        imperfect_visual_steps = maze.make_imperfect()

    visual_steps: list[tuple[int, int]] = [
        (start_xy[1] * 2 + 1, start_xy[0] * 2 + 1)
    ]

    for (old_x, old_y), (new_x, new_y) in logical_history:
        visual_steps.append((old_y + new_y + 1, old_x + new_x + 1))
        visual_steps.append((new_y * 2 + 1, new_x * 2 + 1))

    visual_steps.extend(imperfect_visual_steps)

    char_grid = maze.get_visual_grid(start_xy, end_xy, None)

    return char_grid, visual_steps


def find_path(
    grid: list[list[str]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
) -> list[tuple[int, int]]:
    if _active_maze is None:
        return []

    start_xy = (entry[1] // 2, entry[0] // 2)
    end_xy = (exit_[1] // 2, exit_[0] // 2)

    start_xy = (
        max(0, min(start_xy[0], _active_maze.width - 1)),
        max(0, min(start_xy[1], _active_maze.height - 1)),
    )
    end_xy = (
        max(0, min(end_xy[0], _active_maze.width - 1)),
        max(0, min(end_xy[1], _active_maze.height - 1)),
    )

    path_coords = _active_maze.solve(start_xy, end_xy)[0]

    if not path_coords:
        return []

    visual_path: list[tuple[int, int]] = []
    for i in range(len(path_coords)):
        x, y = path_coords[i]
        r, c = y * 2 + 1, x * 2 + 1
        visual_path.append((r, c))

        if i < len(path_coords) - 1:
            nx, ny = path_coords[i + 1]
            vr, vc = (y + ny + 1), (x + nx + 1)
            visual_path.append((vr, vc))

    return visual_path


def write_maze_file(
    grid: list[list[str]],
    path: list[tuple[int, int]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
    filename: str,
) -> None:
    if _active_maze is None:
        return

    start_xy = (entry[1] // 2, entry[0] // 2)
    end_xy = (exit_[1] // 2, exit_[0] // 2)

    start_xy_t = (entry[1], entry[0])
    end_xy_t = (exit_[1], exit_[0])

    _, path_str = _active_maze.solve(start_xy, end_xy)
    _active_maze.write_output(filename, start_xy_t, end_xy_t, path_str)
