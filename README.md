# Mooving

App for motorbikes sharing with a new _spicy_ flavor.

## How to use it

Just go to the website, sing-up with all the necessary information and take a look at the catalog. 

## The app itself

The app is formed by a _vue_ app for frontend and a _flask_ app for the backend, coupled with a _sqlite_ database.

### Local set-up

For the frontend, execute **build_frontend.sh** file, and erase _templates_ and _static_ folder in _flaskProject_. Change the name form _mooving_ to _frontend_ and modify the **package.json** file at the _script_ _build_ keyword, adding: `--mode personal`. And run it again `npm run build`.

For the backend, simply install the requirements at **flaskProject/requirements.txt** and create the database with `./local_create_db.sh`. Optionally, run `python flaskProject/add_data.py` to populate it.
