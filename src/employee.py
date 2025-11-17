
from dataclasses import dataclass
from datetime import datetime

# from pay import Pay

@dataclass
class Employee:
    id: int
    fname: str
    lname: str
    address: str
    # pay: dict[str,str|int] # Pay
    hire_date: datetime
    active: bool
