PYTHON = python3
PIP = pip3
MAIN = a_maze_ing.py
CONFIG = config.txt
PKG_DIR = mazegen_pkg

.PHONY: install run debug lint lint-strict clean build-pkg

install:
	$(PIP) install flake8 mypy build --break-system-packages 2>/dev/null || \
	$(PIP) install flake8 mypy build

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	flake8 .
	mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.pyo" -delete 2>/dev/null || true
	rm -f maze.txt

build-pkg:
	cd $(PKG_DIR) && $(PYTHON) -m build
	cp $(PKG_DIR)/dist/mazegen-*.whl . 2>/dev/null || true
	cp $(PKG_DIR)/dist/mazegen-*.tar.gz . 2>/dev/null || true
	@echo "Package built successfully."
