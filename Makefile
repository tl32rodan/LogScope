PYTHON ?= python3
export PYTHONPATH := src

.PHONY: run demo clean test

RUN_ARGS ?= analysis example/config.json ./example/issues

run:
	$(PYTHON) -m logscope.app.cli $(RUN_ARGS)

demo:
	$(PYTHON) -m logscope.app.cli analysis example/config.json ./example/issues

clean:
	rm -rf example/issues example/output .pytest_cache .mypy_cache .coverage
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +

test:
	$(PYTHON) -m unittest discover
