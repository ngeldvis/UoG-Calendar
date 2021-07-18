from time import sleep
from datetime import date, datetime
from typing import List
from dateutil.parser import parse as parse_datetime

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from event import Event

 
# Includes all web-scraping functionality of the app


GUELPH_CALENDAR_URL = 'https://calendar.uoguelph.ca/undergraduate-calendar/schedule-dates/'


# gets the Selenium webdriver used to scrape the website
def get_webdriver():
    opts = webdriver.ChromeOptions()
    opts.headless = True
    driver = webdriver.Chrome(options=opts)
    driver.get(GUELPH_CALENDAR_URL)
    return driver


# filter function to filter out unwanted calendars
# * param: table - dictionary that includes title, year, and html table object
def filter_table(table: dict) -> bool:
    phrases_to_filter = ['D.V.M.', '6 Week Format', 'Session']
    for phrase in phrases_to_filter:
        if phrase in table['title']:
            return False
    return True


# get the year of the calender from it's header
# * param: title - title of a calendar
def get_year(title: str) -> int:
    for string in title.split():
        try:
            return int(string)
        except ValueError:
            continue
    return 0


# gets a list of all wanted guelph events on the webpage
def get_events() -> List[Event]:

    driver = get_webdriver()

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
            date_str = row.find_element_by_css_selector('td.column0').text + ', ' + str(table['year'])
            date = parse_datetime(date_str).date()
            row_events = [event.text for event in row.find_elements_by_css_selector('td.column1 li')]
            for event in row_events:
                e = Event(date, event)
                events.append(e)
   
    return events


# get all the events and print them to the console
def main() -> None:    
    for event in get_events():
        print(event)


if __name__ == '__main__':
    main()
