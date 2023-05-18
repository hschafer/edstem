all: test type-check

test:
	poetry run pytest

type-check:
	poetry run mypy edstem tests --exclude tests/client_ideas.py

