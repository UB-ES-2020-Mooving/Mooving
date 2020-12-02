#!/bin/sh
set -ev
#Script to build the frontend
#Variable FRONTEND must exist and Vue must be installed

cd $FRONTEND
#build specification depending on branch pushed
case $BRANCH in
    DEVOPS)
        ./node_modules/.bin/vue-cli-service build --mode devops
        ;;
    STAGING)
        ./node_modules/.bin/vue-cli-service build --mode staging --fix
        ;;
    PRODUCTION)
        ./node_modules/.bin/vue-cli-service build --mode production --fix
        ;;
    *)
        ./node_modules/.bin/vue-cli-service build --mode personal
        ;;
esac

