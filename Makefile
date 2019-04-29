run:
	docker build -t python-dd-homework .
	docker run python-dd-homework

install:
	pip install -r requirement.txt

test:
	docker build -f Dockerfile.test -t python-dd-homework-test .
	docker run python-dd-homework-test
