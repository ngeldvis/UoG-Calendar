import datetime
from dateutil.parser import parse as parse_datetime, ParserError
from playwright.sync_api import sync_playwright, Browser
from typing import List

from classes.event import Event
 
# Includes all web-scraping functionality of the app

URL_PREFIX = 'https://calendar.uoguelph.ca'
GUELPH_CALENDAR_URL = f'{URL_PREFIX}/undergraduate-calendar/schedule-dates/'

DEFAULT_FILTERS = ['D.V.M.', '6 Week Format', 'Session', 'Reading']

# filter function to filter out unwanted calendars
# * param: table - dictionary that includes title, year, and html table object
def includeCalender(text: str, filters: List[str]) -> bool:
    for phrase in filters:
        if phrase in text:
            return False
    return True


# some string with a year in it and no other numbers before the year
def get_year(title: str) -> str:
    for token in title.split():
        try:
            int(token)
            return token
        except ValueError:
            continue
    return None

# get the events from a specific page
def get_page_events(browser: Browser, url: str, year: str) -> List[Event]:

    page = browser.new_page()
    page.goto(URL_PREFIX + url)

    events = []

    table = page.query_selector('.tbl_calendar')
    for row in table.query_selector_all('tbody tr'):
        try: # if parser can't determine a date, skip
            col1_text = row.query_selector('.column0').inner_text()
            event_date = parse_datetime(col1_text + ' ' + year).date()
        except ParserError:
            continue

        for event in row.query_selector_all('.column1 li'):
            event_title = event.inner_text()
            events.append(Event(event_date, event_title))

    return events

# gets a list of all guelph events on their site
def get_events() -> List[Event]:

    events = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(GUELPH_CALENDAR_URL)

        links = page.query_selector_all('.sitemap a')
        
        for a in links:
            a_href, a_text = a.get_attribute('href'), a.inner_text()

            if includeCalender(a_text, DEFAULT_FILTERS) and a_href:
                new_events = get_page_events(browser, a_href, get_year(a_text))
                events.extend(new_events)

    return events


def save_events_to_ics(events: List[Event]) -> None:
    today = datetime.datetime.today()
    today_str = today.strftime("%Y-%m-%d")

    with open(f'calendars/events-{today_str}.ics', 'w') as file:
        # write the ics header
        file.write('BEGIN:VCALENDAR\n')
        file.write('VERSION:2.0\n')
        file.write('PRODID:-//Guelph Calendar Scraper//EN\n')
        file.write('CALSCALE:GREGORIAN\n')
        file.write('METHOD:PUBLISH\n')
        file.write('X-WR-CALNAME:UoG Events\n')
        file.write('X-WR-TIMEZONE:America/Toronto\n')
        file.write('X-WR-CALDESC:Event\'s from the University of Guelph\'s official course calendar. Not affiliated with the University of Guelph\n')

        # write each event to the file
        for event in events:
            file.write('BEGIN:VEVENT\n')
            file.write(f'DTSTART;VALUE=DATE:{event.date.strftime("%Y%m%d")}\n')
            file.write(f'DTSTAMP:{today.strftime("%Y%m%dT%H%M%SZ")}\n')
            file.write(f'CREATED:{today.strftime("%Y%m%dT%H%M%SZ")}\n')
            file.write('DESCRIPTION:\n')
            file.write(f'LAST-MODIFIED:{today.strftime("%Y%m%dT%H%M%SZ")}\n')
            file.write('LOCATION:\n')
            file.write('SEQUENCE:0\n')
            file.write('STATUS:CONFIRMED\n')
            file.write(f'SUMMARY:{event.title}\n')
            file.write('TRANSP:OPAQUE\n')
            file.write('END:VEVENT\n')

        # write the ics footer
        file.write('END:VCALENDAR\n')

# get all the events and print them to the console
def main() -> None:
    events = get_events()
    for event in events:
        print(event)


if __name__ == '__main__':
    main()
