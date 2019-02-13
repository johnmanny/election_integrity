# Author: John Nemeth
# Description: This file contains simple shell commands for installing,
#		running, and cleaning up files for a webserver using Flask,
#		python, and associated utilities


# Create variable for executing all commands in an environment context
INENV = . env/bin/activate ;

# default target for installing environment requirements to run the server
install: env

# installs environment and requirements
env:
	python3 -m venv env
	$(INENV) pip3 install -r requirements.txt

# runs the webserver
run: 	env
	($(INENV) cd source; python3 flask_main.py) || true

# DO NOT USE FOR NOW
test:	env
	$(INENV) cd server; nosetests

# to freeze requirements in requirements.txt
dist:	env
	$(INENV) pip3 freeze > requirements.txt

# cleans up the directories
clean:
	rm -f *.pyc */*.pyc
	rm -rf __pycache__ */__pycache__

veryclean:
	make clean
	rm -rf env
