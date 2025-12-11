from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup
from textual.events import Key
from textual.reactive import Reactive
from textual.widgets import DataTable, Footer, Header

from components.add_employee import AddEmployeeModal
from components.employee_table import EmployeeTable
from components.time_table import TimeTable
from db import get_all_employees, get_timestamps_from_employee
from employee import Employee
from globals import TIME_DISPLAY_FORMAT


class TimeTrackApp(App[object]):
    theme = Reactive("catppuccin-mocha")
    BINDINGS = [
        ("left", "focus_employees", "Focus Employees"),
        ("right", "focus_timestamps", "Focus Timestamps"),
        ("a", "show_add_employee", "Add Employee"),
        #("i", "toggle_active", "Toggle Employee Active"),
        ("escape", "hide_modal", "Close Modal"),
        ("ctrl+q", "quit", "Quit"),
        # ("?", "toggle_help", "Show Help"),
    ]
    CSS = """
        Screen {align-horizontal: center; align-vertical: top;}
        Header {dock: top;}
        Footer {dock: bottom;}
        HorizontalGroup {width: auto;}
        VerticalScroll {height: auto;}
        .hidden {display: none;}
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield HorizontalGroup(
            EmployeeTable(id="employees-scroll"),
            TimeTable(id="timestamp-scroll"),
        )
        yield AddEmployeeModal(id="add-employee-modal", classes="hidden")
        yield Footer()

    # <-- hooks -->

    def on_mount(self):
        """Focus employee table on startup and load first employee timestamps."""
        emp_scroll = self.query_one("#employees-scroll", EmployeeTable)
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
        ts_scroll = self.query_one("#timestamp-scroll", TimeTable)
        table = ts_scroll.query_one("#timestamp-table", DataTable)

        table.clear()

        for ts in get_timestamps_from_employee(employee.id):
            color = "light_green" if ts.action == "work" else "red"

            start = ts.start_time.strftime(TIME_DISPLAY_FORMAT)
            end = ts.end_time.strftime(TIME_DISPLAY_FORMAT)
            elapsed = f"[{color}]{str(ts.delta)}[/{color}]"
            action = f"[{color}]{ts.action}[/{color}]"

            table.add_row(start, end, elapsed, action)

    def refresh_employees(self):
        scroll = self.query_one("#employees-scroll", EmployeeTable)
        table = scroll.query_one("#employee-table", DataTable)

        table.clear()

        employees = get_all_employees()
        last_index = -1

        for i, emp in enumerate(employees):
            color = "light_green" if emp.active else "red"
            active_mark = "O" if emp.active else "X"

            hire = emp.hire_date.strftime('%Y-%m-%d')
            name = f"[{color}]{emp.display_name()}[/{color}]"
            active = f"[{color}]{active_mark}[/{color}]"

            table.add_row(name, hire, active, key=str(emp.id))
            last_index = i

        # highlight last employee
        if last_index >= 0:
            table.cursor_type = "row"
            table.show_cursor = True
            table.move_cursor(row=last_index)
            table.focus()
            self.update_timestamps(employees[last_index])

    # <-- keybinds -->

    def action_focus_employees(self):
        self.query_one("#employee-table", DataTable).focus()

    def action_focus_timestamps(self):
        self.query_one("#timestamp-table", DataTable).focus()

    def action_show_add_employee(self):
        modal = self.query_one("#add-employee-modal", AddEmployeeModal)
        modal.remove_class("hidden")
        modal.focus()

    def action_toggle_active(self):
        self.toggle_employee_active()

    def action_hide_modal(self):
        modal = self.query_one("#add-employee-modal", AddEmployeeModal)
        modal.add_class("hidden")

    def toggle_employee_active(self):
        # TODO: next feature
        pass
