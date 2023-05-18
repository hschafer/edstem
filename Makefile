all: test type-check format

format:
	black --check edstem tests

test:
	poetry run pytest

type-check:
	poetry run mypy edstem tests

