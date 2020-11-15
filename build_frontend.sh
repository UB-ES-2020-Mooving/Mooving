#!/bin/sh

#Script designed for creation and build ONLY on server depending on branch
npm install -g @vue/cli
#Create vue project
vue create --preset preset_v1.json patata
sed -i 's/"rules": {}/"rules": {\n\t\t\t"no-unused-vars": "off"\n\t\t\t}/' patata/package.json
#copy frontend source files
\cp -r frontend/bootstrap frontend/src frontend/tests frontend/vue.config.js patata
#copy env files
\cp frontend/.env.devops frontend/.env.production frontend/.env.staging patata 
#install depencies
cd patata
npm install --save axios bootstrap-vue vuelidate vue-router
#build depending on branch
case $BRANCH in
    DEVOPS)
        ./node_modules/.bin/vue-cli-service build --mode devops
        ;;
    STAGING)
        ./node_modules/.bin/vue-cli-service build --mode staging
        ;;
    PRODUCTION)
        ./node_modules/.bin/vue-cli-service build --mode production
        ;;
    *)
        ./node_modules/.bin/vue-cli-service build
        ;;
esac
#move build files
cd ..
\cp -r patata/dist flaskProject
#Done
echo "Success"