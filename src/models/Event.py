from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    """Class to keep track of events"""
    title:str
    date:datetime
    id:int=-1