init:
	pip install -r requirements.txt

test:
	nosetests -v tests

configure:
	python configure.py
