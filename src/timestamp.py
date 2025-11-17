from dataclasses import dataclass
from datetime import datetime
from typing_extensions import Literal


@dataclass
class Timestamp:
    id: int
    employee_id: int
    start: datetime
    end: datetime
    action: Literal['work', 'break']

    @property
    def delta(self):
        return self.end - self.start 
