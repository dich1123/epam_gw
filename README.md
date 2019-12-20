
Prerequisites
-
- Install everything from requirements.txt

Command: ~$ pip install -r requirements.txt

Installing
-
- Download all files to your computer
- Run gunicorn server for API
- Command: ~$ gunicorn --bind 0.0.0.0:5010 wsgi:app
- WARNING! You should run it from ./department-app/service
- Run app.py 
- Command: ~$ python3 app.py
- WARNING! You should run it from ./department-app

Now you can send api requests to http://0.0.0.0:5010 (if it necessary)
 you can change it in command(then don't forget to change api_host_name 
 in app.py). Your web app will run http://127.0.0.1:5009/ (if it necessary
 you can change port in app.py in line with 'app.run()')
 
 Tests
 -
 
 Unittest tests main function for work with db.
 - You need upgrade tests for your db data.
 - Then run command: ~$ python3 -m unittest discover
 - WARNING! Run command from ./
 
Coding style tests working via pylint and can show basic 
problems with your syntax.
 - You need to run next commands:
 - ~$ pylint department-app/service/rest_db_operations.py
 - ~$ pylint department-app/dbmodels.py
 - ~$ pylint department-app/app.py
 - WARNING! Run them from ./
 
 Authors
 -
 -Cherenkov Dima(DiCh)