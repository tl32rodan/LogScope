PYTHON ?= python3
export PYTHONPATH := src

.PHONY: run test

RUN_ARGS ?= example/config.json

run:
	$(PYTHON) -m logscope.app.cli $(RUN_ARGS)

test:
	$(PYTHON) -m unittest discover