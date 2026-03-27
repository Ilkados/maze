# 42 School Maze Makefile

PYTHON = python3
PIP = pip3
NAME = a_maze_ing.py
CONFIG = config.txt

.PHONY: all install run debug clean lint lint-strict

all: run

# Page 5: Install project dependencies
install:
	$(PIP) install flake8 mypy build

# Page 5: Execute the main script
run:
	$(PYTHON) $(NAME) $(CONFIG)

# Page 5: Run in debug mode
debug:
	$(PYTHON) -m pdb $(NAME) $(CONFIG)

# Page 5: Remove temporary files and caches
clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf mazegen/__pycache__
	rm -rf dist
	rm -rf *.egg-info

# Page 6: Mandatory linting (Specific flags required by Page 7)
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Optional strict checking
lint-strict:
	flake8 .
	mypy . --strict