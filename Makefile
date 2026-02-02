VENV   = venv
PYTHON = $(VENV)/bin/python3
PIP    = $(VENV)/bin/pip

# --------------------
# Create venv & install deps
install:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements
# 	after this comand run source venv/bin/activate to run virtual enverinemnt

# --------------------
# Run app inside venv
run:
	$(PYTHON) a_maze_ing.py config.conf

# --------------------
# Debug inside venv
debug:
	$(PYTHON) -m pdb a_maze_ing.py config.conf

# --------------------
# Linting (still uses venv python if needed)
lint:
	flake8 . --exclude=$(VENV)
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude $(VENV)

# --------------------
# Cleanup
clean:
	rm -rf venv __pycache__ */__pycache__ .mypy_cache */*.mypy_cache *.txt */*.txt
