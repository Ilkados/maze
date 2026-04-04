"""
mazegen/constants.py: Fixed values and configuration for the maze logic.
"""

# The '42' pattern coordinates (Local Grid: 7 wide x 5 high)
# These represent the cells that will be blocked (fully closed).
PATTERN_42: set[tuple[int, int]] = {
    # The 4
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
    (4, 4), (5, 4), (6, 4),
}

# Hexadecimal Wall Bitmasks (Mandatory Requirements - Page 9 & 10)
# Bit 0 (LSB) = North (1)
# Bit 1       = East  (2)
# Bit 2       = South (4)
# Bit 3       = West  (8)
WALL_BITS: dict[str, int] = {
    "N": 1,  # 0001 in binary
    "E": 2,  # 0010 in binary
    "S": 4,  # 0100 in binary
    "W": 8   # 1000 in binary
}

# Minimum dimensions required to fit the logo
LOGO_WIDTH: int = 7
LOGO_HEIGHT: int = 5