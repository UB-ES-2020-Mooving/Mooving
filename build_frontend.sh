#!/bin/sh

#Script designed for the creation and build of the frontend on server (ONLY) 

FRONTEND=mooving
npm install -g @vue/cli
#Create vue project
echo $FRONTEND
vue create --preset preset_v1.json $FRONTEND
sed -i 's/"rules": {}/"rules": {\n\t\t\t"no-unused-vars": "off",\n\t\t\t"no-multiple-empty-lines": "off"\n\t\t\t}/' $FRONTEND/package.json
#copy frontend source files
\cp -r frontend/bootstrap frontend/src frontend/tests frontend/vue.config.js $FRONTEND
#copy env files
\cp frontend/.env.devops frontend/.env.production frontend/.env.staging $FRONTEND 
#install depencies
cd $FRONTEND
npm install --save axios bootstrap-vue vuelidate vue-router
#build depending on branch
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
        ./node_modules/.bin/vue-cli-service build
        ;;
esac
#move build files
cd ..
\cp -r $FRONTEND/dist/static flaskProject
\cp $FRONTEND/dist/favicon.ico flaskProject/static
mkdir flaskProject/templates
\cp $FRONTEND/dist/index.html flaskProject/templates
#Done
echo "Success"
