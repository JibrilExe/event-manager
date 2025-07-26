from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    """Class to keep track of events"""
    name:str
    date:datetime