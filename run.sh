#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# --- Start script ---
# -----------------------------------------------------------------------------
if [ "$1" = "" ]; then
    echo "Main usage:
    ./run.sh first_app -- to run API server for save raw data
    ./run.sh second_app -- to run API server for convert raw data to Avro
    ./run.sh freeze -- to save requirements
    ./run.sh pylint -- to start pylint validator
    ./run.sh tests -- to start pytest
    "
else
    case "$1" in
        freeze)
            # -----------------------------------------------------------------
            # --- Save requirements to file ---
            # -----------------------------------------------------------------
            source venv/bin/activate
            pip freeze | grep -v "pkg-resources" > requirements.txt
        ;;
        tests)
            pytest -s "$2" -W ignore::DeprecationWarning
        ;;
        pylint)
            # -----------------------------------------------------------------
            # --- Save requirements to file ---
            # -----------------------------------------------------------------
            source venv/bin/activate
            pylint app --disable=missing-docstring,import-outside-toplevel,cyclic-import
        ;;
        *)
            # -----------------------------------------------------------------
            # --- Run scripts ---
            # -----------------------------------------------------------------
            source venv/bin/activate
            python ./manage.py "$@"
    esac
fi
