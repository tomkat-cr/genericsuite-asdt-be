#!/bin/bash
# run_openlit.sh
# 2025-02-08 | CR
# Run OpenLit
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

if [ "$OTEL_EXPORTER_OTLP_ENDPOINT" = "" ]; then
    echo "WARNING: OTEL_EXPORTER_OTLP_ENDPOINT not set"
    echo "assign it in the .env file or export it in the environment"
    echo "E.g. export OTEL_EXPORTER_OTLP_ENDPOINT=\"http://127.0.0.1:4318\""
    exit 1
fi

if [ "$ACTION" = "" ]; then
    ACTION="$1"
fi
if [ "$ACTION" = "" ]; then
    echo "Usage: run_openlit.sh <run|down|logs>"
    exit 1
fi

if [ "$ACTION" = "run" ]; then
    echo ""
    echo "Run OpenLit"
    echo ""
    rm -rf /tmp/openlit
    mkdir -p /tmp/openlit
    cd /tmp/openlit
    if ! git clone git@github.com:openlit/openlit.git
    then
        if ! git clone https://github.com/openlit/openlit.git
        then
            echo "ERROR: git clone git@github.com:openlit/openlit.git failed"
            exit 1
        fi
    fi
    cd openlit
    if ! docker compose up -d
    then
        echo "ERROR: docker compose up -d failed"
        exit 1
    fi
    docker ps
    docker compose logs -f

elif [ "$ACTION" = "down" ]; then
    echo ""
    echo "Stop OpenLit"
    echo ""
    cd /tmp/openlit
    docker compose down

elif [ "$ACTION" = "logs" ]; then
    echo ""
    echo "OpenLit logs"
    echo ""
    cd /tmp/openlit
    docker compose logs -f

else
    echo "Unknown action: $ACTION"
    exit 1
fi

echo ""
echo "Done"
