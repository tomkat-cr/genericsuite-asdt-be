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

crewai_install:
	bash scripts/run_crewai_agents.sh install

crewai_update:
	bash scripts/run_crewai_agents.sh update

crewai_lock:
	bash scripts/run_crewai_agents.sh lock

camelai_install:
	bash scripts/run_camelai_agents.sh install

camelai_update:
	bash scripts/run_camelai_agents.sh update

camelai_lock:
	bash scripts/run_camelai_agents.sh lock

# Testing

crewai_test:
	bash scripts/run_crewai_agents.sh test

crewai_other_test:
	bash scripts/run_crewai_agents.sh crewai_test

test: crewai_test

# App run

crewai_run:
	bash scripts/run_crewai_agents.sh run "${PROJECT}" "${TOPIC}"

crewai_api:
	bash scripts/run_crewai_agents.sh api

api: crewai_api
run: crewai_run

camelai_run:
	bash scripts/run_camelai_agents.sh run "${PROJECT}" "${TOPIC}"

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
