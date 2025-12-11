from contextlib import contextmanager
from datetime import datetime
from mariadb import Cursor, Connection, connect

from employee import Employee
from globals import TIME_STORE_FORMAT
from timestamp import Timestamp

"""
Database tools
"""


QUERIES = {
    "get_all_employees": "SELECT * FROM employees;",
    "get_employee":      "SELECT * FROM employees WHERE id=?;",
    "get_all_timestamps": """
        SELECT t.*
        FROM timestamps t
        INNER JOIN employees e
                ON e.id = t.employee_id;
    """,
    "get_timestamps_from_employee": """
        SELECT t.*
        FROM timestamps t
        INNER JOIN employees e
                ON e.id = t.employee_id
        WHERE e.id=?;
    """,
    "add_employeee":"""
        INSERT INTO employees (fname, lname, active, address, hire_date) 
        VALUES (?,?,?,?,?);
    """,
    "toggle_employee_active":"UPDATE employees SET active = NOT active WHERE id=?;",
}


@contextmanager
def cursor():
    """Cursor context manager"""
    conn: Connection|None = None
    cur: Cursor|None = None

    try:
        conn = connect(db="timetrack")
        cur = conn.cursor(dictionary=True)

        yield cur

        conn.commit()

    except Exception:
        if conn:
            conn.rollback()
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_employee(id: int) -> Employee|None:
    with cursor() as cur:
        cur.execute(QUERIES["get_employee"], (id,))
        _data = cur.fetchone()
    try:
        return Employee(**_data) #pyright:ignore
    except ValueError:
        return None

def get_all_employees() -> list[Employee]:
    with cursor() as cur:
        cur.execute(QUERIES["get_all_employees"])
        return [Employee(**e) for e in cur.fetchall()] #pyright:ignore

def get_all_timestamps() -> list[Timestamp]:
    with cursor() as cur:
        cur.execute(QUERIES["get_all_timestamps"])
        return [Timestamp(**ts) for ts in cur.fetchall()] #pyright:ignore

def get_timestamps_from_employee(id: int) -> list[Timestamp]:
    with cursor() as cur:
        cur.execute(QUERIES["get_timestamps_from_employee"], (id,))
        return [Timestamp(**ts) for ts in cur.fetchall()] #pyright:ignore

def add_employee(fname:str, lname:str, active:bool, address:str, hire_date:datetime):
    with cursor() as cur:
        cur.execute(
            QUERIES["add_employeee"],
            (fname, lname, active, address, hire_date.strftime(TIME_STORE_FORMAT))
        )

        cur.execute("SELECT LAST_INSERT_ID();")
        if (_data:=cur.fetchone()) is not None:
            return Employee(_data['LAST_INSERT_ID()'], fname, lname,address,hire_date, active)
        else:
            raise ValueError("Failed to insert")

def toggle_employee_active(emp_id: int):
    with cursor() as cur:
        cur.execute(QUERIES["toggle_employee_active"], (emp_id,))
