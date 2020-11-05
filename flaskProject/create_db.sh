#!/bin/sh
cd flaskProject
if [ -e "migration" ]; then
    rm -r "migrations"
fi

if [ -e "__py_cahce__" ]; then
    rm -r "__pycahce__"
fi

if [ -e "data.db" ]; then
    rm "data.db"
fi

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
cd ..
