#!/usr/bin/env bash

set -e
set -x

# coverage run --source=app -m pytest
coverage run --source=app -m pytest tests/scripts/test_backend_pre_start.py
coverage report --show-missing
coverage html --title "${@-coverage}"
