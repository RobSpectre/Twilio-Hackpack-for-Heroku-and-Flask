init:
	pip install -r requirements.txt --use-mirrors

test:
	nosetests -v tests

configure:
	python configure.py
