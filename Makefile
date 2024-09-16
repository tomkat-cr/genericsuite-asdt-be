# .DEFAULT_GOAL := local
.PHONY: install update lock test crewai_test requirements lock-rebuild build publish-test publish dev-prepare-local dev-prepare-git dev-prepare-pypi dev-prepare-publish 
SHELL := /bin/bash

# App management

install:
	poetry install

update:
	poetry update

lock:
	poetry lock

# Testing

test:
	poetry run pytest tests

crewai_test:
	# e.g. PROJECT="Generate blog posts for the most updated articles of the lst week" TOPIC="AI LLMs" make crewai_test
	poetry run test "${PROJECT}" "${TOPIC}"

# App run

api:
	poetry run api

run:
	# e.g. PROJECT="generate unit test based on pytest to all functions and methods in the repo https://github.com/tomkat-cr/genericsuite-be" TOPIC="" make un
	# e.g. PROJECT="Generate blog posts for the most updated articles of the lst week" TOPIC="AI LLMs" make run
	poetry run run_crew "${PROJECT}" "${TOPIC}"

crewai_run: run

# Package publish

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

lock-rebuild:
	poetry lock --no-update
	poetry install --sync

build:
	# Build 'dist' directory needed for the Pypi publish
	poetry lock --no-update
	rm -rf dist
	python3 -m build

publish-test: dev-prepare-publish requirements build
	# Pypi Test publish
	python3 -m twine upload --repository testpypi dist/*

publish: dev-prepare-publish requirements build
	# Production Pypi publish
	python3 -m twine upload dist/*

dev-prepare-local:
    # Just in case this package requires the "genericsuite-be" package...
	# poetry add --group dev ../genericsuite-be

dev-prepare-git:
    # Just in case this package requires the "genericsuite-be" package...
	# poetry add --group dev git+https://github.com/tomkat-cr/genericsuite-be

dev-prepare-pypi:
    # Just in case this package requires the "genericsuite-be" package...
	# poetry add --group dev genericsuite

dev-prepare-publish:
    # Just in case this package requires the "genericsuite-be" package...
	# if ! poetry remove genericsuite; then echo "'genericsuite' was not removed..."; else "'genericsuite' removed successfully..."; fi;
