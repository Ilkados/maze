PYTHON = python3
PIP = pip3
NAME = a_maze_ing.py
CONFIG = config.txt

.PHONY: all install run debug clean lint lint-strict

all: run

install:
	$(PIP) install flake8 mypy build

run:
	$(PYTHON) $(NAME) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(NAME) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf dist
	rm -rf *.egg-info

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3 -m flake8 .
	python3 -m mypy . --strict