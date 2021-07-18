from datetime import date

# Event class to store an event's name and date

class Event:
    
    def __init__(self, date: date, title: str) -> None:
        self.date = date
        self.title = title

    def __str__(self) -> str:
        return f'{self.date} - {self.title}'
