init:
	pip install -r requirements.txt --use-mirrors

test:
	nosetests tests

configure:
	python configure.py
