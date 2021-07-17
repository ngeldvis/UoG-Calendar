from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from google.oauth2 import service_account

from .event import Event

# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials

GUELPH_CALENDAR_URL = 'https://calendar.uoguelph.ca/undergraduate-calendar/schedule-dates/'
GOOGLE_CAL_API_KEY = 'AIzaSyBc1zvQYjU-1CwSQ89WTb2cOnffjbsLLu4'
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service_account.json'



def filter_table(table: dict) -> bool:
    phrases_to_filter = ['D.V.M.', '6 Week Format', 'Session']
    for phrase in phrases_to_filter:
        if phrase in table['title']:
            return False
    return True


def get_year(title: str) -> int:
    # return the first string that casts to a int successfully
    for string in title.split():
        try:
            return int(string)
        except:
            continue
    return 0


def get_events(driver: WebDriver) -> list:
    raw_tables = driver.find_elements_by_css_selector('.tbl_calendar')
    raw_headers = driver.find_elements_by_css_selector('.page_content h2')[1:]

    unfiltered_data = [{
        'title': raw_headers[i].text, 
        'table': raw_tables[i],
        'year': get_year(raw_headers[i].text)
    } for i in range(len(raw_tables))]

    # get rid of unwanted tables
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
    return service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


def main() -> None:
    opts = webdriver.ChromeOptions()
    opts.headless = True
    driver = webdriver.Chrome(options=opts)
    driver.get(GUELPH_CALENDAR_URL)

    sleep(1)

    # creds = get_credentials()
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
        print(event)


if __name__ == '__main__':
    main()
