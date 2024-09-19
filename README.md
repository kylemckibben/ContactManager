Straight forward contact manager. I am using token authentication rather than sessions, so CSRF exemptions are applied to the API endpoints (views). Additionally, I implemented my own fuzzy search using Levenshtein distance. I omitted the use of environment variables for DB info and the secret key since I will not be deploying this project.

### Stack
* Django REST Framework
* PostgreSQL
* React

## Using the contact manager
If you want to run the project, after cloning go into the main `ContactManager` directory:
(Note - I am using a [python virtual environment](https://docs.python.org/3/tutorial/venv.html))

Move into the `frontend` directory and run install command
```
npm install
```

If you setup a virtual environment, activate it.
Now move into the top level `contact_manager` directory and install the following packages
```
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install psycopg2
```

For the database you will need to install PostgreSQL and create a database and user consistent with the information in `settings.py` under DATABASES, or change that information to match your information. Once the database is setup, run the following (still inside the top level `contact_manager`)
```
python3 manage.py migrate
```

To run the app start the frontend by going inside `frontend` and running
```
npm run dev
```
then start the backend inside top level `contact_manager`
```
python3 manage.py runserver
```