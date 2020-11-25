#!/bin/sh

#Script to move the frontend
#Variable FRONTEND must exist and Vue must be installed

\cp -r $FRONTEND/dist/static flaskProject
\cp $FRONTEND/dist/favicon.ico flaskProject/static
mkdir flaskProject/templates
\cp $FRONTEND/dist/index.html flaskProject/templates