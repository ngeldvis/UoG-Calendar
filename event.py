from dateutil.parser import parser as dateparser

class Event:
    
    def __init__(self, date: str, title: str) -> None:
        self.date = dateparser(date)
        self.title = title

    def __str__(self) -> str:
        return f'{self.date} - {self.title}'

    def __repr__(self) -> str:
        return f"'{self.date}':'{self.title}'"
