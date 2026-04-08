"""Logo pattern module for embedding the '42' pattern into the maze."""

from mazegen.logic.constants import PATTERN_42, LOGO_WIDTH, LOGO_HEIGHT

_LOGO_H: int = 5


def logo_fits(rows: int, cols: int) -> bool:
    """Check whether the '42' logo fits within the given maze dimensions.

    Args:
        rows: Number of rows in the maze grid.
        cols: Number of columns in the maze grid.

    Returns:
        True if the logo can be drawn, False if the maze is too small.
    """
    logic_w = cols//2
    logic_h = rows//2
    return logic_w >= LOGO_HEIGHT and logic_h >= LOGO_HEIGHT


def get_logo_cells(rows: int, cols: int) -> set[tuple[int, int]]:
    """
    Returns the visual grid positions of the '42' logo cells.
    """
    # logical grid size
    logic_w = cols // 2
    logic_h = rows // 2

    if logic_w < LOGO_WIDTH or logic_h < LOGO_HEIGHT:
        return set()

    # center the logo
    start_x = (logic_w - LOGO_WIDTH) // 2
    start_y = (logic_h - LOGO_HEIGHT) // 2

    visual_logo: set[tuple[int, int]] = set()

    # convert each pattern cell to visual coords
    for lx, ly in PATTERN_42:
        real_x = start_x + lx
        real_y = start_y + ly

        v_row = real_y * 2 + 1
        v_col = real_x * 2 + 1
        visual_logo.add((v_row, v_col))

    return visual_logo
