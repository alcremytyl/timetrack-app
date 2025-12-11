# HACK: quick debugging 
from components.app import TimeTrackApp
from db import cursor


if __name__ == "__main__":
    with cursor() as cur:
        cur.execute("""
            DELETE FROM employees
            WHERE fname = "Foo" AND lname = "Bar";
        """)

    TimeTrackApp().run()

