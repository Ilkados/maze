# *This project has been created as part of the A-Maze-ing project by <moboulir>, <asmounci>.*

## Description

This project is a maze generator and solver written in Python.

It creates a random maze, displays it, and can also find the shortest path from entry to exit. The program works with two coordinate systems:

* **Logical grid** → used for maze generation (cells only) this part done by moboulir
* **Visual grid** → used for display (cells + walls) and this part done by asmounci

The maze can be **perfect** (no loops) or **imperfect** (with loops).

---

## How it works

The program uses:

* **DFS (Depth-First Search)** → to generate the maze i choose it because s used to explore the maze by going as deep as possible along each path before backtracking, which is ideal for maze generation and pathfinding.
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

```bash
python a_maze_ing.py config.txt
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
