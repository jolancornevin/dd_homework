test:
	python -m coverage run --source=src -m unittest tests
	python -m coverage report -m
