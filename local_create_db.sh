#!/bin/sh
cd flaskProject
if [ -e "migrations" ]; then
    rm -r "migrations"
fi

if [ -e "__pycache__" ]; then
    rm -r "__pycache__"
fi

if [ -f "data.db" ]; then
    rm "data.db"
fi

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
cd ..
echo "Succes creating empty database"
