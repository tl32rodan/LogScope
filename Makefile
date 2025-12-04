PYTHON ?= python3
export PYTHONPATH := src

.PHONY: run test

run:
	$(PYTHON) -m logscope.app.cli example/config.json

test:
	$(PYTHON) -m unittest discover
