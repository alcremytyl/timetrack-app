from pprint import pprint
import yaml

from employee import Employee
from timestamp import Timestamp

import mariadb

with open("sample.yaml", "r") as f:
    _data = yaml.safe_load(f.read())
    # employees: dict[int, Timestamp] = {d['id']:Employee(**d) for d in _data['employees']}
    # timestamps: dict[int, Timestamp] = {d['id']:Timestamp(**d) for d in _data['timestamps']}

class Database:
    def __enter__(self)

try:
    conn = mariadb.connect(db="timetrack")
    cur = conn.cursor(dictionary=True)
except:
    raise mariadb.Error("Failed to connect")

employees = dict[int, Employee]()
timestamps = dict[int, Timestamp]()

_ = cur.execute("SELECT * FROM employees;")

for e in cur:
    employee = Employee(**e)
    employees[employee.id] = employee
    

pprint(employees)
pprint(timestamps)
_ = conn.close()

