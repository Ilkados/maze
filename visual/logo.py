"""Logo pattern module for embedding the '42' pattern into the maze."""

_DIGIT_4: list[list[int]] = [
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 1],
    [0, 0, 1],
    [0, 0, 1],
]

_DIGIT_2: list[list[int]] = [
    [1, 1, 1],
    [0, 0, 1],
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 1],
]

_LOGO_H: int = 5
_LOGO_W4: int = 3
_LOGO_W2: int = 3
_LOGO_GAP: int = 1
_LOGO_S: int = 2


def logo_fits(rows: int, cols: int) -> bool:
    """Check whether the '42' logo fits within the given maze dimensions.

    Args:
        rows: Number of rows in the maze grid.
        cols: Number of columns in the maze grid.

    Returns:
        True if the logo can be drawn, False if the maze is too small.
    """
    return (
        rows >= _LOGO_H * _LOGO_S + 2
        and cols >= (_LOGO_W4 + _LOGO_GAP + _LOGO_W2) * _LOGO_S + 2
    )


from mazegen.constants import PATTERN_42, LOGO_WIDTH, LOGO_HEIGHT

def get_logo_cells(rows: int, cols: int) -> set[tuple[int, int]]:
    """
    This version maps your LOGICAL PATTERN_42 to the VISUAL grid.
    It uses Scale 1 to ensure the DFS can move around it.
    """
    # 1. Calculate logic size
    logic_w = cols // 2
    logic_h = rows // 2
    
    if logic_w < LOGO_WIDTH or logic_h < LOGO_HEIGHT:
        return set()

    # 2. Calculate the same centering offset used in your Maze.py
    start_x = (logic_w - LOGO_WIDTH) // 2
    start_y = (logic_h - LOGO_HEIGHT) // 2

    visual_logo: set[tuple[int, int]] = set()

    # 3. Map your PATTERN_42 (logical) to Visual Coordinates (row, col)
    for lx, ly in PATTERN_42:
        real_x = start_x + lx
        real_y = start_y + ly
        
        # Convert Logical (x, y) to Visual (row, col)
        # Visual = logic * 2 + 1
        v_row = real_y * 2 + 1
        v_col = real_x * 2 + 1
        visual_logo.add((v_row, v_col))
        
    return visual_logo