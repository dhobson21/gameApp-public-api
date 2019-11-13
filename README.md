# BOARD-UP Public API

Built with Django REST Framework
to serve data to the [React Client](https://github.com/joekennerly/kterclient)

## 0. Getting Started
To contribute to this project, you will need the following:
* Bash Terminal
* Python3
* Pip3
* Text Editor

## 1. Create virtual environment
Once you've cloned the repo, cd into it and run this command from your terminal:
```
python -m venv backendCapstoneEnv
```
>Windows Users can run this in GitBash or Command Line

Start your virtual environment by running one of the following commands:
* Mac: `source ./backendCapstone/bin/activate`
* Windows: `source ./backendCapstone/Scripts/activate`

## 2. Install Dependencies
```
pip install -r requirements.txt
```

## 3. Initial Migrations
Now that the project is ready, we need to setup the database. Lucky for us, all of this is done by running a shell script *in a bash terminal*:
```
./seed_db.sh
```
>>> If you ever need to reset the database with new migrations. **Close all connections** to the db before doing so!

## 4. Start up the server
```
python manage.py runserver
```