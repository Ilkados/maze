class Cell:
    """
    Represent one cell of the maze.

    Attributes:
        north (bool): True if the north wall exists.
        east (bool): True if the east wall exists.
        south (bool): True if the south wall exists.
        west (bool): True if the west wall exists.
        visited (bool): True if the cell was visited during generation.
    """

    def __init__(self) -> None:
        """Create a new cell with all walls closed and visited set to False."""
        self.north: bool = True
        self.east: bool = True
        self.south: bool = True
        self.west: bool = True
        self.visited: bool = False