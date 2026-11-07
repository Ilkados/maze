# A-Maze-ing

A Python terminal program that generates a maze, finds the shortest route from entry to exit, and lets you toggle the solution or generate a new layout.

![Solved seed-42 maze with the route highlighted in light green](docs/maze-preview.svg)

The preview uses the checked-in configuration with seed 42. The light green cells trace the route through the dark green walls.

## Collaboration

This 42 project was created by **moboulir** and **asmounci**. Moboulir worked on the logical grid used to generate the maze. Asmounci worked on the visual grid used to display cells and walls.

## How it works

The program uses:

* **DFS (Depth-First Search)** → to generate the maze by following a passage until it must backtrack.
* **BFS (Breadth-First Search)** → to find the shortest path

Steps:

1. Convert input to logical grid
2. Generate maze using DFS
3. Optionally make it imperfect (add loops)
4. Solve maze using BFS
5. Convert everything to visual grid for display

---

## Installation & Usage

### Run the program

From the repository root, use a Unix-like terminal and Python 3.10 or later. The viewer uses `termios` for keyboard input.

```bash
python3 a_maze_ing.py config.txt
```

### Lint (code style check)

```bash
make lint
```

---

## Configuration file

The program uses a configuration file with this format:

```
WIDTH=31
HEIGHT=31
ENTRY=(1,1)
EXIT=(29,29)
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

### Explanation

* `WIDTH`, `HEIGHT` → size of maze (visual grid)
* `ENTRY`, `EXIT` → start and end positions (row, col)
* `OUTPUT_FILE` → file where maze is saved
* `PERFECT` → True = no loops, False = loops
* `SEED` → optional, makes maze reproducible

---

## Features

* Generate random maze
* Show / hide shortest path
* Regenerate maze
* Change wall colors
* Save maze to file
* Support animation of generation

---

## Maze Generator Module

The logic is separated into modules:

* `maze.py` → main maze class
* `generator.py` → DFS generation
* `solver.py` → BFS solving
* `validator.py` → rules checking
* `cell.py` → cell structure
* `validator` → for 3x3 open loop

### Important concepts

* Logical → Visual: `* 2 + 1`
* Visual → Logical: `// 2`

---

## Algorithm choice

We use **DFS** because:

* simple to implement
* creates long paths
* guarantees all cells are reachable

We use **BFS** for solving because:

* it finds the shortest path

---

## Output file

The output file contains:

* the maze grid
* entry and exit positions
* shortest path (N, E, S, W directions)

---

## Team work

* Logic part → maze generation, solving, validation
* Visual part → display, animation, colors

### What worked well

* clear separation between logic and display
* modular design

### What can be improved

* better error handling
* more algorithms

---

## Resources

* Python documentation
* DFS and BFS algorithms tutorials
* StackOverflow for debugging

---

## Summary

This project shows how to:

* build a maze generator
* use graph algorithms
* separate logic and visualization
* handle user interaction and configuration

---
