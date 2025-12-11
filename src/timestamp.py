from dataclasses import dataclass
from datetime import datetime
from typing_extensions import Literal


@dataclass
class Timestamp:
    id: int
    employee_id: int
    start_time: datetime
    end_time: datetime
    action: Literal['work', 'break']

    @property
    def delta(self):
        return self.end_time - self.start_time
