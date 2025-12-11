from contextlib import contextmanager
from pprint import pprint
from mariadb import Cursor, Connection, connect

from employee import Employee
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
    """
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
