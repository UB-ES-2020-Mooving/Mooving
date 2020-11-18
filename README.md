# Mooving

App for motorbikes sharing with a new _spicy_ flavor.

## How to use it

Just go to the website, sing-up with all the necessary information and take a look at the catalog. 

## The app itself

The app is formed by a _vue_ app for frontend and a _flask_ app for the backend, coupled with a _sqlite_ database.

### Local set-up

For the frontend, _loosely_ follow the **build_frontend.sh** file, a more formal script is on the way. In short, create the app, add the needed depencies and copy the **frontend** directory content. To build it, you will have to do it as the script, or you can modify the **package.json** file at the _script_ _build_ keyword, adding: `--mode personal`.

For the backend, simply install the requirements at **flaskProject/requirements.txt** and create the database with `./local_create_db.sh`. Optionally, run `python flaskProject/add_data.py` to populate it.
