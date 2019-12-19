import sys
sys.path.insert(0, '../')

import dbmodels
from flask_restful import Api, Resource, reqparse
from flask import request, jsonify
import logging

logger = logging.getLogger('db_operations')
logger.setLevel(logging.INFO)

handler = logging.FileHandler('../logger_db_operations.log')
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

handler2 = logging.StreamHandler()
handler2.setLevel(logging.INFO)
handler2.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(handler2)
logger.info('rest_db_operations works')

db = dbmodels.db
app = dbmodels.app
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('name')
parser.add_argument('birthdate')
parser.add_argument('salary')
parser.add_argument('department')


def create_search_and_amount_query_employees(sort, page, search_from, search_to):
    sorts = {'name_up': 'name', 'name_down': 'name  DESC', 'birth_up': 'birthdate', 'birth_down': 'birthdate DESC',
             'dep_up': 'department', 'dep_down': 'department DESC', 'sal_up': 'salary', 'sal_down': 'salary DESC'}

    is_none_changer = lambda value, new_value: value if value is not None else new_value

    sort = is_none_changer(sort, 'name_up')
    page = int(is_none_changer(page, 1))
    search_from = is_none_changer(search_from, '1970-01-01')

    if not search_to:
        lim_start = (page-1)*30
        lim_end = 30
        some_date = search_from
        sort_type = sorts[sort]

        search_query = f"SELECT id,name,birthdate,salary,department FROM employee WHERE birthdate='{some_date}'" \
                    f" ORDER BY {sort_type} LIMIT {lim_start},{lim_end}"  # for searching by one date
        amount_query = f"SELECT COUNT(id) FROM employee WHERE birthdate='{some_date}'"
        return {'search_query': search_query, 'amount_query': amount_query}

    else:
        lim_start = (page - 1) * 30
        lim_end = 30
        start_date = search_from
        end_date = search_to
        sort_type = sorts[sort]
        search_query = f"SELECT id,name,birthdate,salary,department FROM employee WHERE birthdate" \
                    f" BETWEEN '{start_date}' AND '{end_date}'" \
                    f" ORDER BY {sort_type} LIMIT {lim_start},{lim_end}"
        amount_query = f"SELECT COUNT(id) FROM employee WHERE birthdate BETWEEN '{start_date}' AND '{end_date}'"
        return {'search_query': search_query, 'amount_query': amount_query}


class EmployeesList(Resource):
    def get(self):
        sort = request.args.get('sort')
        page = request.args.get('page')
        search_from = request.args.get('search_from')
        search_to = request.args.get('search_to')

        search_query = create_search_and_amount_query_employees(sort, page, search_from, search_to)
        info = db.engine.execute(search_query['search_query'])
        count_req = db.engine.execute(search_query['amount_query']).fetchall()
        if count_req:
            count_req = int(count_req[0][0])
        else:
            count_req = 1
        dict_info = {'employees': []}
        for i in info:
            dict_info['employees'].append({'id': str(i.id), 'name': i.name, 'birthdate': str(i.birthdate),
                               'salary': i.salary, 'department': i.department})
        dict_info['count_req'] = count_req
        logger.info('EmployeeList GET: DONE')

        return jsonify(dict_info)


class DepartmentsList(Resource):
    def get(self):
        info = db.engine.execute("select id, department, (select avg(salary) from employee where "
                                 "employee.department = department.department) average_salary from department;")

        dict_info = {}
        for i in info:
            dict_info[str(i.id)] = {'department': i.department, 'average_salary': str(i.average_salary)}
        logger.info('DepartmentsList GET: DONE')
        return jsonify(dict_info)


class EmployeeProfile(Resource):
    def get(self, id):
        employee = dbmodels.Employee.query.get_or_404(id)
        dict_info = {'id': str(employee.id), 'name': employee.name, 'birthdate': str(employee.birthdate),
                               'salary': employee.salary, 'department': employee.department}
        logger.info('EmployeeProfile GET: DONE')
        return jsonify(dict_info)

    def post(self, id):
        args = parser.parse_args()
        employee = dbmodels.Employee.query.get_or_404(args['id'])
        employee.name = args['name']
        employee.birthdate = args['birthdate']
        employee.salary = args['salary']
        employee.department = args['department']

        try:
            db.session.commit()
            logger.info('EmployeeProfile POST: DONE')
            return '', 201
        except:
            logger.error('EmployeeProfile POST: FAILED')
            return '', 500

    def delete(self, id):
        employee = dbmodels.Employee.query.get_or_404(id)

        try:
            db.session.delete(employee)
            db.session.commit()
            logger.info('EmployeeProfile DELETE: DONE')
            return '', 204
        except:
            logger.error('EmployeeProfile DELETE: FAILED')
            return '', 500

    def put(self, id):
        args = parser.parse_args()
        new_employee = dbmodels.Employee(args['name'], args['birthdate'], args['salary'], args['department'])

        try:
            db.session.add(new_employee)
            db.session.commit()
            logger.info('EmployeeProfile PUT: DONE')
            return '', 200
        except:
            logger.error('EmployeeProfile PUT: FAILED')
            return '', 500


class DepartmentProfile(Resource):
    def get(self, id):  # read profile
        department = dbmodels.Department.query.get_or_404(id)
        dict_info = {str(department.id): {'department': department.department}}
        logger.info('DepartmentProfile GET: DONE')
        return jsonify(dict_info)

    def post(self, id):  # change profile info
        args = parser.parse_args()
        department = dbmodels.Department.query.get_or_404(args['id'])
        department.department = args['department']

        try:
            db.session.commit()
            logger.info('DepartmentProfile POST: DONE')
            return '', 201
        except:
            logger.error('DepartmentProfile POST: FAILED')
            return '', 500

    def delete(self, id):  # delete profile
        department = dbmodels.Department.query.get_or_404(id)

        try:
            db.session.delete(department)
            db.session.commit()
            logger.info('DepartmentProfile DELETE: DONE')
            return '', 204
        except:
            logger.error('DepartmentProfile DELETE: FAILED')
            return '', 500

    def put(self, id):  # create new profile
        args = parser.parse_args()
        new_department = dbmodels.Department(args['department'])

        try:
            db.session.add(new_department)
            db.session.commit()
            logger.info('DepartmentProfile PUT: DONE')
            return '', 200
        except:
            logger.error('DepartmentProfile PUT: FAILED')
            return '', 500


api.add_resource(EmployeesList, '/api_employees_list')
api.add_resource(DepartmentsList, '/api_departments_list')
api.add_resource(EmployeeProfile, '/api_employee_profile/<int:id>')
api.add_resource(DepartmentProfile, '/api_department_profile/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)

# http://127.0.0.1:5008/employees?page=1&search_from=1996-11-10&search_to=2019-12-18
