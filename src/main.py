from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import DataTable, Footer, Header, Label
from typing_extensions import final, override

from db import get_all_employees, get_timestamps_from_employee
from employee import Employee

TIME_FORMAT="%I:%M %p"

@final
class EmployeesScroll(VerticalScroll):
    @override
    def compose(self) -> ComposeResult:
        employees = get_all_employees()

        table = DataTable[str](id="employee-table")
        table.cursor_type = "row"
        table.show_cursor = True
        table.zebra_stripes = True

        table.add_columns("Name", "Active", "Hired On")

        for emp in employees:
            table.add_row(
                emp.display_name(),
                "O" if emp.active else "X",
                emp.hire_date.strftime("%Y-%m-%d"),
            )

        yield table


@final
class TimestampScroll(VerticalScroll):
    @override
    def compose(self) -> ComposeResult:
        table = DataTable[str](id="timestamp-table")
        table.cursor_type = "row"
        table.show_cursor = True
        table.zebra_stripes = True
        table.add_columns("Start", "End", "Elapsed", "Type")
        yield table


@final
class TimeTrackApp(App[object]):

    CSS = """
        Screen { align: center middle; }
        Header { dock: top; }
        Footer { dock: bottom; }
    """

    @override
    def compose(self) -> ComposeResult:
        yield Header()
        yield HorizontalGroup(
            EmployeesScroll(id="employees-scroll"),
            TimestampScroll(id="timestamp-scroll"),
        )
        yield Footer()

    # <-- hooks -->

    def on_mount(self):
        """Focus employee table on startup and load first employee timestamps."""
        emp_scroll = self.query_one("#employees-scroll", EmployeesScroll)
        emp_table = emp_scroll.query_one("#employee-table", DataTable)
        emp_table.focus()

        # pre-load timestamps
        if emp_table.row_count > 0:
            first_employee = get_all_employees()[0]
            self.update_timestamps(first_employee)

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        if event.data_table.id != "employee-table": 
            return

        row_index = event.data_table.get_row_index(event.row_key)
        employee = get_all_employees()[row_index]
        self.update_timestamps(employee)

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted):
        if event.data_table.id != "employee-table":
            return

        row_index = event.data_table.get_row_index(event.row_key)
        employee = get_all_employees()[row_index]
        self.update_timestamps(employee)

    # <-- callbacks -->

    def update_timestamps(self, employee: Employee):
        ts_scroll = self.query_one("#timestamp-scroll", TimestampScroll)
        table = ts_scroll.query_one("#timestamp-table", DataTable)

        table.clear()

        for ts in get_timestamps_from_employee(employee.id):
            start = ts.start_time.strftime(TIME_FORMAT)
            end = ts.end_time.strftime(TIME_FORMAT)
            elapsed = str(ts.delta)

            match ts.action:
                case "break": style = "red"
                case "work":  style = "green"
            type_text = Text(ts.action, style=style)

            table.add_row(start, end, elapsed, type_text)



# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    TimeTrackApp().run()

