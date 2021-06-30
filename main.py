import dateutil.parser as date_parser
import os.path

from time import sleep
from typing import List

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

GUELPH_CALENDAR_URL = 'https://calendar.uoguelph.ca/undergraduate-calendar/schedule-dates/'
SCOPES = ['https://www.googleapis.com/auth/calendar']

class Event:
    def __init__(self, date: str, title: str) -> None:
        self.date = date_parser.parse(date)
        self.title = title

    def __str__(self) -> str:
        return f'{self.date} - {self.title}'


def filter_table(table: dict) -> bool:
    if 'D.V.M.' in table['title'] or '6 Week Format' in table['title'] or 'Session' in table['title']:
        return False
    return True


def get_year(title: str) -> int:
    for string in title.split():
        try:
            return int(string)
        except:
            continue
    return 0


def get_events(driver: WebDriver) -> list[Event]:
    raw_tables = driver.find_elements_by_css_selector('.tbl_calendar')
    raw_headers = driver.find_elements_by_css_selector('.page_content h2')[1:]

    unfiltered_data = [{
        'title': raw_headers[i].text, 
        'table': raw_tables[i],
        'year': get_year(raw_headers[i].text)
    } for i in range(len(raw_tables))]

    data = filter(filter_table, unfiltered_data)

    events = []

    for table in data:
        rows = table['table'].find_elements_by_css_selector('tbody tr')
        for row in rows:
            date = row.find_element_by_css_selector('td.column0').text + ', ' + str(table['year'])
            row_events = [event.text for event in row.find_elements_by_css_selector('td.column1 li')]
            for event in row_events:
                e = Event(date, event)
                events.append(e)
                
    return events


def get_credentials():
    creds = Credentials.from_authorized_user_file('credentials.json', SCOPES)


def main() -> None:
    opts = webdriver.ChromeOptions()
    opts.headless = True
    driver = webdriver.Chrome(options=opts)
    driver.get(GUELPH_CALENDAR_URL)
    sleep(1)

    creds = get_credentials()

    events = get_events(driver)

    for e in events:
        event = {
            'summary': e.title,
            'start': {
                'date': e.date.isoformat()
            },
            'end': {
                'date': e.date.isoformat()
            }
        }


if __name__ == '__main__':
    main()
