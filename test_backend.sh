#!/bin/bash
set -e

if [[ -z "$TEST_BACKEND" ]]; then
    echo "No backend tests to run, exiting..."
    exit 0
fi

cd flaskProject
echo "Installing depencies"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo "Running tests..."
case $TEST_BACKEND in
    SECONDARY)
        python -m pytest tests/tests_secondary
        ;;
    ENDPOINTS)
        python -m pytest tests/tests_endpoints
        ;;
    AUTO)
        cd ..
        ./local_create_db.sh
        cd flaskProject
        python add_data.py
        python -m pytest tests/tests_auto
        ;;
    *)
        python -m pytest tests/
        ;;
esac
echo "Tests done"
exit 0