import requests
import json
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'dahfygjsknlmca;dkfvla'
db = SQLAlchemy(app)
api_host_name = 'http://0.0.0.0:5010/'


@app.route('/')
def index():
    """

    :return: index page(start page)
    """
    return render_template('index.html')


@app.route('/employees', methods=['GET', 'POST'])
def employees():
    """

    :return: Employees with search and sort options
    """

    sort = request.args.get('sort')
    page = request.args.get('page')
    search_from = request.args.get('search_from')
    search_to = request.args.get('search_to')

    if request.args.get('delete'):
        id = request.args.get('id')
        r = requests.delete(api_host_name + '/api_employee_profile/' + str(id))
        return redirect(url_for('employees', sort=sort, page=page, search_from=search_from, search_to=search_to))

    info = requests.get(api_host_name + '/api_employees_list',
                        {'sort': sort, 'page': page, 'search_from': search_from, 'search_to': search_to})
    info = info.json()
    employees = info['employees']
    count_req = info['count_req']

    return render_template('employees.html', employees=employees, count_req=count_req)


@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):  # you can update data here
    """

    :param id: unique employee id
    :return: employee's profile
    """
    employee = requests.get(api_host_name + '/api_employee_profile/' + str(id))
    departments_all = requests.get(api_host_name + '/api_departments_list')
    employee = employee.json()
    departments_all = departments_all.json()

    if request.method == 'POST':
        name = request.form['name']
        birthdate = request.form['birthdate']
        salary = request.form['salary']
        department = request.form['department']
        full_info = [request.form['name'], request.form['birthdate'],
                     request.form['salary'], request.form['department']]

        if '' in full_info:
            flash('All forms must be filled')
            return redirect(url_for('profile', id=id))

        r = requests.post(api_host_name + '/api_employee_profile/' + str(id),
                          {'id': id, 'name': name, 'birthdate': birthdate, 'salary': salary, 'department': department})

        return redirect(url_for('employees'))
    else:
        return render_template('profile.html', employee=employee, departments=departments_all)


@app.route('/delete/<int:id>')
def delete(id):
    """

    :param id: unique employee's id
    :return: redirect to Employees
    """
    r = requests.delete(api_host_name + '/api_employee_profile/' + str(id))
    return redirect(url_for('employees'))


@app.route('/departments')
def departments():
    """

    :return: Departments with delete and upgrade facilities
    """
    if request.args.get('delete'):
        id = request.args.get('id')
        r = requests.delete(api_host_name + '/api_department_profile/' + str(id))
        return redirect(url_for('departments'))

    info = requests.get(api_host_name + '/api_departments_list')
    dict_info = info.json()

    return render_template('departments.html', departments=dict_info)


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    """

    :return: form for creating new department
    """
    if request.method == 'POST':
        department = request.form['content']
        print([department])

        if '' == department:
            flash('All forms must be filled')
            return render_template('add_department.html')

        r = requests.put(api_host_name + '/api_department_profile/0', json={'department': department})
        print(r)
        return redirect(url_for('departments'))

    return render_template('add_department.html')


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    """

    :return: form for creating new employee
    """
    departments_all = requests.get(api_host_name + '/api_departments_list')
    departments_all = departments_all.json()

    if request.method == 'POST':
        name = request.form['name']
        birthdate = request.form['birthdate']
        salary = request.form['salary']
        department = request.form['department']
        full_info = [name, birthdate, salary, department]

        if '' in full_info:
            flash('All forms must be filled')
            return render_template('add_employee.html', departments=departments_all)

        r = requests.put(api_host_name + '/api_employee_profile/0',
                         {'name': name, 'birthdate':birthdate, 'salary': salary, 'department': department})
        return redirect(url_for('employees'))

    return render_template('add_employee.html', departments=departments_all)


@app.route('/change_department/<int:id>', methods=['POST', 'GET'])
def change_department(id):
    """

    :param id: department's unique id
    :return: form for upgrading department
    """
    department = requests.get(api_host_name + '/api_department_profile/' + str(id))
    dict_department = json.loads(department.text)

    if request.method == 'POST':
        department_info = request.form['content']

        if '' == department_info:
            flash('All forms must be filled')
            return redirect(url_for('change_department', id=id))

        r = requests.post(api_host_name + '/api_department_profile/' + str(id),
                          {'id': id, 'department': department_info})

        return redirect(url_for('departments'))

    return render_template('change_department.html', department=dict_department[str(id)]['department'])


if __name__ == '__main__':
    app.run(port=5009, debug=True)
