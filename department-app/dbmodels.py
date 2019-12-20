from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:Hardpas!1123@localhost/gwdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dahfygjsknlmca;dkfvla'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Department(db.Model):
    """
    Department module for DB
    """
    id = db.Column('id', db.Integer, primary_key=True)
    department = db.Column('department', db.String(100), unique=True, nullable=False)

    def __init__(self, department):
        self.department = department

    def __repr__(self):
        return f'Departmment department:{self.department}'


class Employee(db.Model):
    """
    Employee model for DB
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=False)

    def __init__(self, name, birthdate, salary, department):
        self.name = name
        self.birthdate = birthdate
        self.salary = salary
        self.department = department

    def __repr__(self):
        return f'Employee name:{self.name},birthdate:{self.birthdate},salary{self.salary},department:{self.department}'


if __name__ == '__main__':
    manager.run()
