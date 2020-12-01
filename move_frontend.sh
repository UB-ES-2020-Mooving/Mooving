#!/bin/bash
set -e
#Script to move the frontend
#Variable FRONTEND must exist and Vue must be installed
if [[ -z "$FRONTEND" ]]; then
    echo "No frontend defined, it won't work..."
    exit 1
fi

\cp -r $FRONTEND/dist/static flaskProject
\cp $FRONTEND/dist/favicon.ico flaskProject/static
mkdir flaskProject/templates
\cp $FRONTEND/dist/index.html flaskProject/templates