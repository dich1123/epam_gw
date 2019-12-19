import unittest
import requests

api_host_name = 'http://127.0.0.1:5000'


class TestRest(unittest.TestCase):

    def test_list_departments(self):
        r = requests.get(api_host_name + '/api_departments_list')
        print(r.status_code)
        self.assertEqual(r.status_code, 200)

    def test_list_employees_one_date(self):
        page = 1
        sort = 'name_up'
        search_from = '1996-11-10'
        search_to = ''
        r = requests.get(api_host_name + '/api_employees_list',
                     {'sort': sort, 'page': page, 'search_from': search_from, 'search_to': search_to})
        self.assertEqual(r.status_code, 200)

    def test_list_employee_two_dates(self):
        page = 1
        sort = 'name_up'
        search_from = '1996-11-10'
        search_to = '2009-11-10'
        r = requests.get(api_host_name + '/api_employees_list',
                         {'sort': sort, 'page': page, 'search_from': search_from, 'search_to': search_to})
        self.assertEqual(r.status_code, 200)

    def test_get_employee_profile(self):
        r = requests.get(api_host_name + '/api_employee_profile/' + str(2002))
        self.assertEqual(r.status_code, 200)

    def test_post_employee_profile(self):
        r = requests.post(api_host_name + '/api_employee_profile/' + str(0),
                          {'id': 2002, 'name': 'Dima Cherenkov', 'birthdate': '1996-11-10',
                           'salary': '2000', 'department': 'Research and development'})
        self.assertEqual(r.status_code, 201)

    def test_get_department_profile(self):
        r = requests.get(api_host_name + '/api_department_profile/' + str(1))
        self.assertEqual(r.status_code, 200)

    def test_post_department_profile(self):
        r = requests.post(api_host_name + '/api_department_profile/' + str(1),
                          {'id': 1, 'department': 'Accounts and Finance'})
        self.assertEqual(r.status_code, 201)
