# **This is a study project**, may have issues and bugs. 
Website with CRUD app. Simulates the service that allows for users to make repair requests. 
The frameworks used here
- Flask
- Jinja2
- Flask-sql-alchemy
- Bootstrap4

Project structure:
- templates - html files
- static - css styles
- __init__ - file of python package named 'simpleCRUD'
- routes.py - logic, functions
- db_models.py - database initialization
- start.py - doesn't work, excess file
## Working with it
Start the local server with __init__ file.

### Database
Database from this project is stored on the local machine. 
Database config is in __init__ file - app.config['SQLALCHEMY_DATABASE_URI'] = //

If you use another Db engine, check how to costumize it in flask-sql-alchemy documentation.


db.create.all() - main method that creates database. Located in db.Models should run only once

### Tasks to do
- [ ] change update function work
- [ ] add bootstrap syles to cars.html page
- [ ] fix some issues
- [ ] improve database
