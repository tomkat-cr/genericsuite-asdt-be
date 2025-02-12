#!/bin/bash
# run_agents.sh
# 2025-02-10 | CR
# Run the GenericSuite CrewAI Agents
#
set -e

REPO_BASEDIR="`pwd`"
cd "`dirname "$0"`"
SCRIPTS_DIR="`pwd`"
cd "${REPO_BASEDIR}"

ENV_FILE="${REPO_BASEDIR}/.env"
if [ ! -f "${ENV_FILE}" ]; then
    echo "ERROR: .env file not found"
    exit 1
fi

set -o allexport
if ! source "${ENV_FILE}"
then
    if ! . "${ENV_FILE}"
    then
        echo "ERROR: .env file could not be sourced"
        exit 1
    fi
fi
set +o allexport ;

if [ "$ACTION" = "" ]; then
    ACTION="$1"
fi
if [ "$ACTION" = "" ]; then
    echo "Usage: run_agents.sh <run|api|test|crewai_test>"
    exit 1
fi

test() {
	poetry run pytest tests
}

crewai_test() {
	# e.g. PROJECT="Generate blog posts for the most updated articles of the last week" TOPIC="AI LLMs" make crewai_test
	poetry run test "${PROJECT}" "${TOPIC}"
}

# App run

api() {
	poetry run api
}

run() {
	# e.g. PROJECT="generate unit test based on pytest to all functions and methods in the repo https://github.com/tomkat-cr/genericsuite-be" TOPIC="" make run
	# e.g. PROJECT="Generate blog posts for the most updated articles of the last week" TOPIC="AI LLMs" make run
	poetry run run_crew "${PROJECT}" "${TOPIC}"
}

if [ "$ACTION" = "run" ]; then
    echo ""
    echo "Run the GenericSuite CrewAI Agents"
    echo ""
    if [ "$PROJECT" = "" ]; then
        PROJECT="$2"
    fi
    if [ "$PROJECT" = "" ]; then
        echo "ERROR: PROJECT is required"
        exit 1
    fi
    if [ "$TOPIC" = "" ]; then
        TOPIC="$3"
    fi
    if [ "$TOPIC" = "" ]; then
        echo "ERROR: TOPIC is required"
        exit 1
    fi
    run
elif [ "$ACTION" = "api" ]; then
    echo ""
    echo "Run the GenericSuite CrewAI API"
    echo ""
    api
elif [ "$ACTION" = "test" ]; then
    echo ""
    echo "Run the GenericSuite CrewAI Tests"
    echo ""
    test
elif [ "$ACTION" = "crewai_test" ]; then
    echo ""
    echo "Run the GenericSuite CrewAI CrewAI Tests"
    echo ""
    crewai_test
else
    echo "Unknown action: $ACTION"
    echo "Usage: run_agents.sh <run|api|test|crewai_test>"
    exit 1
fi
