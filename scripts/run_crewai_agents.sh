#!/bin/bash
# run_crewai_agents.sh
# 2025-02-10 | CR
# Run the GenericSuite CrewAI Agents
#
set -e

REPO_BASEDIR="`pwd`"
cd "`dirname "$0"`"
SCRIPTS_DIR="`pwd`"
cd "${REPO_BASEDIR}"/genericsuite_asdt/crewai

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
    echo "Usage: run_crewai_agents.sh <run|api|test|crewai_test>"
    exit 1
fi

link_common_directories() {
    if [ ! -d "${REPO_BASEDIR}/genericsuite_asdt/crewai/genericsuite_asdt/utils" ]; then
        ln -s "${REPO_BASEDIR}/genericsuite_asdt/utils" "${REPO_BASEDIR}/genericsuite_asdt/crewai/genericsuite_asdt/utils"
    fi
    if [ ! -d "${REPO_BASEDIR}/genericsuite_asdt/crewai/genericsuite_asdt/tools" ]; then
        ln -s "${REPO_BASEDIR}/genericsuite_asdt/tools" "${REPO_BASEDIR}/genericsuite_asdt/crewai/genericsuite_asdt/tools"
    fi
}

test() {
    link_common_directories
	poetry run pytest tests
}

crewai_test() {
    link_common_directories
	# e.g. PROJECT="Generate blog posts for the most updated articles of the last week" TOPIC="AI LLMs" make crewai_test
	poetry run test "${PROJECT}" "${TOPIC}"
}

install() {
    link_common_directories
    poetry install
}

update() {
    link_common_directories
    poetry update
}

lock() {
    link_common_directories
    poetry lock
}

api() {
    link_common_directories
	poetry run api
}

run() {
    link_common_directories
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
elif [ "$ACTION" = "install" ]; then
    echo ""
    echo "Run the GenericSuite CrewAI poetry install"
    echo ""
    install
elif [ "$ACTION" = "update" ]; then
    echo ""
    echo "Run the GenericSuite CrewAI poetry update"
    echo ""
    update
elif [ "$ACTION" = "lock" ]; then
    echo ""
    echo "Run the GenericSuite CrewAI poetry lock"
    echo ""
    lock
else
    echo "Unknown action: $ACTION"
    echo "Usage: run_crewai_agents.sh <run|api|test|crewai_test>"
    exit 1
fi
