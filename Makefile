lint:
	python -m isort -c -rc enochecker_cli/ tests/
	python -m black --line-length 160 --check enochecker_cli/ tests/
	python -m flake8 --select F --per-file-ignores="__init__.py:F401" enochecker_cli/ tests/
	python -m mypy enochecker_cli/ tests/

format:
	python -m isort -rc enochecker_cli/ tests/
	python -m black --line-length 160 enochecker_cli/ tests/

test:
	pip install .
	python -m pytest
