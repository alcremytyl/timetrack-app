from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import DataTable
from typing_extensions import final

from db import get_all_employees


@final
class EmployeeTable(VerticalScroll):
    def compose(self) -> ComposeResult:
        employees = get_all_employees()

        table = DataTable[str](id="employee-table")
        table.cursor_type = "row"
        table.show_cursor = True
        table.zebra_stripes = True
        table.add_columns("Name", "Hired On", "Active")

        for emp in employees:
            color = "light_green" if emp.active else "red"
            active = "O" if emp.active else "X"

            hire = emp.hire_date.strftime('%Y-%m-%d')
            name = f"[{color}]{emp.display_name()}[/{color}]"
            active = f"[{color}]{active}[/{color}]"
            table.add_row(name, hire, active, key=str(emp.id))

        yield table

