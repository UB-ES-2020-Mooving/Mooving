#!/bin/sh
if [ -e "migrations" ]; then
    rm -r "migrations"
fi

if [ -e "__pycache__" ]; then
    rm -r "__pycache__"
fi

if [ -f "data.db" ]; then
    rm "data.db"
fi
psql -d $DATABASE_URL -c "DROP TABLE alembic_version ;"
export FLASK_APP=app
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
echo "Succes creating empty database"