define PROJECT_HELP_MSG

Usage: \n
    make help           show this message \n
    make python-reqs	install python packages in requirements.pip \n
    make start          launch a server from the local virtualenv
	make test			run the project tests

endef
export PROJECT_HELP_MSG

help:
	echo $$PROJECT_HELP_MSG

VENV = venv
export VIRTUAL_ENV := $(abspath ${VENV})
export PATH := ${VIRTUAL_ENV}/bin:${PATH}

${VENV}:
	python3.6 -m venv $@

python-reqs: requirements.pip | ${VENV}
	pip install -r requirements.txt

start:
	python sapp.py

test: data.json.gz
	python -m unittest test_sapp.py