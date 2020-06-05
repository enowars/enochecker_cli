lint:
	python -m isort -c -rc enochecker_cli/
	python -m black --check enochecker_cli/
	python -m flake8 --select F --per-file-ignores="__init__.py:F401" enochecker_cli/
	python -m mypy enochecker_cli/

format:
	python -m isort -rc enochecker_cli/
	python -m black --line-length 160 enochecker_cli/

test:
	pip install .
	python -m pytest
