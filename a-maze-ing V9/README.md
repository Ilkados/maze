*This project has been created as part of the 42 curriculum by your_login.*

# A-Maze-ing 🌀

A maze generator in Python that creates perfect (or imperfect) mazes, embeds a "42" pattern, and provides an interactive terminal display.

---

## Description

**A-Maze-ing** generates random mazes from a configuration file, writes them to a hexadecimal output file, and renders them visually in the terminal with ANSI colors. The user can interactively regenerate mazes, show/hide the shortest solution path, and cycle through color themes.

**Key features:**
- Recursive Backtracker (DFS) maze generation algorithm
- Perfect maze mode (exactly one path between any two cells)
- Reproducible generation via seed
- Embedded "42" pattern (closed cells forming the digits)
- BFS shortest path solver
- Interactive terminal display with color themes
- Reusable `mazegen` Python package

---

## Instructions

### Requirements
- Python 3.10 or later
- No external dependencies for the core program

### Installation

```bash
# Install development tools (linting, type checking, packaging)
make install
```

### Run

```bash
python3 a_maze_ing.py config.txt
```

Or:

```bash
make run
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint
```

### Clean

```bash
make clean
```

### Build the mazegen package

```bash
make build-pkg
```

---

## Configuration File Format

The configuration file uses `KEY=VALUE` pairs (one per line). Lines starting with `#` are comments.

| Key | Required | Description | Example |
|-----|----------|-------------|---------|
| `WIDTH` | ✅ | Number of columns | `WIDTH=20` |
| `HEIGHT` | ✅ | Number of rows | `HEIGHT=15` |
| `ENTRY` | ✅ | Entry coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | ✅ | Exit coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | ✅ | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | ✅ | Perfect maze? | `PERFECT=True` |
| `SEED` | ❌ | Random seed | `SEED=42` |
| `ALGORITHM` | ❌ | Generation algorithm | `ALGORITHM=backtracker` |

Example `config.txt`:
```
# A-Maze-ing configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

---

## Output File Format

The output file contains:
1. One row per line, each cell encoded as a single hex digit (0–F)
2. An empty line
3. Entry coordinates `x,y`
4. Exit coordinates `x,y`
5. Shortest path as a string of `N`, `E`, `S`, `W` characters

**Wall bitmask encoding:**
| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

A value of `1` means the wall is **closed**; `0` means **open**.

---

## Maze Generation Algorithm

### Recursive Backtracker (DFS)

The algorithm works as follows:
1. Start from cell (0,0) with all walls closed
2. Randomly choose an unvisited neighbor
3. Remove the shared wall and recurse
4. Backtrack when all neighbors are visited

**Why this algorithm?**
- Produces long, winding corridors — visually interesting and challenging
- Guarantees a connected maze (spanning tree = perfect maze)
- Simple recursive implementation
- Easily seeded for reproducibility
- Well-suited for embedding the "42" pattern post-generation

---

## Reusable mazegen Package

### What is reusable?

The `MazeGenerator` class inside `mazegen_pkg/src/mazegen/maze_generator.py` is fully reusable. It can be installed as a pip package.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Usage

```python
from mazegen import MazeGenerator

# Create a 20x15 perfect maze with seed 42
gen = MazeGenerator(width=20, height=15, seed=42, perfect=True)
gen.generate(entry=(0, 0), exit_=(19, 14))

# Access the grid (2D list of int bitmasks)
grid = gen.grid          # grid[row][col] = bitmask

# Get solution directions
solution = gen.solution  # ['S', 'E', 'N', ...]

# Get solution coordinates
path = gen.solution_path  # [(0,0), (0,1), ...]

# Get hex-encoded rows (for output file)
for row in gen.get_hex_grid():
    print(row)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `width` | `int` | `20` | Number of columns |
| `height` | `int` | `15` | Number of rows |
| `seed` | `int` | `None` | Random seed |
| `perfect` | `bool` | `True` | Generate perfect maze |

---

## Interactive Terminal Display

When you run the program, you get an interactive menu:

```
==== A-Maze-ing ====
1. Re-generate a new maze
2. Show/Hide path from entry to exit
3. Rotate maze wall colors
4. Show/Hide '42' pattern color
5. Quit
```

**Legend:**
- `S` = Start (entry)
- `E` = Exit
- `·` = Solution path (when shown)
- `▪` = Cells forming the "42" pattern

---

## Team and Project Management

### Roles
- **your_login** — Full implementation: maze generation, solver, display, packaging, tests

### Planning
- Day 1–2: Study the subject, choose algorithm, implement `MazeGenerator`
- Day 3: Implement config parser, output writer, BFS solver
- Day 4: Terminal display with interactive menu and ANSI colors
- Day 5: "42" pattern embedding, packaging, README, tests

### What worked well
- Recursive Backtracker is simple and produces great mazes
- Separating maze logic into a standalone module made testing easy
- Solving the maze before embedding "42" avoids connectivity issues

### What could be improved
- Multiple algorithm support (Prim's, Kruskal's)
- Graphical MLX display
- Animation during generation

### Tools used
- Python 3.10+
- flake8, mypy for code quality
- setuptools/build for packaging
- Claude AI — for scaffolding the project structure, debugging the "42" pattern placement logic, and drafting docstrings

---

## Resources

- [Maze generation algorithms - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracker - Jamis Buck's blog](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Prim's and Kruskal's maze algorithms](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Python typing module](https://docs.python.org/3/library/typing.html)
- [PEP 257 – Docstring conventions](https://peps.python.org/pep-0257/)
- [Python packaging guide](https://packaging.python.org/en/latest/)

### AI Usage

Claude AI (claude.ai) was used for:
- Scaffolding the initial project file structure
- Debugging the "42" pattern boundary condition (off-by-one in the fit check)
- Identifying the generation order bug (42 cells were blocking BFS)
- Drafting and formatting docstrings and this README

All AI-generated code was reviewed, understood, tested, and corrected before inclusion.
