from datetime import datetime
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.events import Key
from textual.widget import Widget
from textual.widgets import Button, Input, Static
from typing_extensions import final, override

from db import add_employee


@final
class AddEmployeeModal(Widget):
    @override
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Insert Employee", id='modal-title'),
            Input(placeholder="First Name", id='fname'),
            Input(placeholder="Last Name", id='lname'),
            Input(placeholder="Address", id='address'),
            Input(placeholder='Hire Date (YYYY-MM-DD)', id='hire-date'),
            Button("Submit", id='submit')
        , id='add-employee-modal')


    def on_button_pressed(self, event:Button.Pressed):
        if event.button.id != "submit":return
        
        fname = self.query_one("#fname", Input).value.strip()
        lname = self.query_one("#lname", Input).value.strip()
        address = self.query_one("#address", Input).value.strip()
        hire_str = self.query_one("#hire-date", Input).value.strip()

        if not (fname and lname and address and hire_str):
            return

        try: 
            hire_date = datetime.strptime(hire_str, "%Y-%m-%d")
        except ValueError: return
        
        add_employee(fname, lname,True,address,hire_date)
        self.app.refresh_employees() #pyright:ignore
        self.add_class("hidden")

