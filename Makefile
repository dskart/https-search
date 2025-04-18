.PHONY: lint lint-fix

lint:
	mypy .
	ruff check .

lint-fix:
	ruff check --fix .
