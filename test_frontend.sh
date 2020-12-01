#!/bin/bash
set -e

if [[ -z "$TEST_FRONTEND" ]]; then
    echo "No frontend tests to run, exiting..."
    exit 0
fi

cd $FRONTEND
echo "Running tests..."
npm run test:unit
echo "Tests done"
exit 0
