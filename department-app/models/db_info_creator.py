import dbmodels
import random
import time
import datetime


def create_info(filename):
    with open(filename, 'r') as file:
        kek = []
        for i in file:
            kek.append(i.strip())
        return kek


def random_date():
    posix_time = random.randint(0, int(time.time() - 315360000))
    answ = datetime.datetime.utcfromtimestamp(posix_time).strftime('%Y-%m-%d')
    return (answ)


names = create_info('names.txt')
surnames = create_info('surnames.txt')
departments = create_info('departments.txt')

for i in range(1000):
    name = random.choice(names)
    surname = random.choice(surnames)
    department = random.choice(departments)
    name = f'{name} {surname}'
    date = random_date()
    person = dbmodels.Employee(name, date, random.randint(500, 5000), department)
    dbmodels.db.session.add(person)
    dbmodels.db.session.commit()


for i in departments:
    dep = dbmodels.Department(i)
    dbmodels.db.session.add(dep)
    dbmodels.db.session.commit()
