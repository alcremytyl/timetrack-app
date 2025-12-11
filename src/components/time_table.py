from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import DataTable
from typing_extensions import final


@final
class TimeTable(VerticalScroll):
    def compose(self) -> ComposeResult:
        table = DataTable(id="timestamp-table")
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("Start", "End", "Elapsed", "Action")
        yield table

