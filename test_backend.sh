#!/bin/sh
set -e

if [[ -z "$TEST_BACKEND" ]]; then
    echo "No backend tests to run, exiting..."
    exit 0
fi

cd flaskProject
echo "Installing depencies"
pip install --upgrade pip
pip install -r requirements.txt
echo "Running tests..."
case $TEST_BACKEND in
    SECONDARY)
        python -m pytest tests/tests_secondary
        ;;
    ENDPOINTS)
        python -m pytest tests/tests_endpoints
        ;;
    ALMOST_ALL)
        python -m pytest tests/tests_auto
        python -m pytest tests/tests_secondary
        ;;
    *)
        python -m pytest tests/
        ;;
esac
echo "Tests done"
exit 0