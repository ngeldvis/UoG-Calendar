import os.path

from typing import List

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import scraper
from classes.event import Event


SCOPES = ['https://www.googleapis.com/auth/calendar']
CLIENT_SCRET_FILE = 'credentials.json'


# get google OAuth2 credentials to access google calendar api
def get_credentials():

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SCRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


# publish event to user's calendar
# * param: event - event dictionary containing relevant event information
# * param: service - google OAuth2 service client to access calendar
def publish_event(event: dict, service) -> None:
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event Created')


# publish a list of events to user's calendar
# * param: events - list of Event objects to add to user's calendar
# * param: service - google OAuth2 service client to access calendar
def publish_events(events: List[Event], service) -> None:
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
        publish_event(event)


# add all University of Guelph calendar events to user calendar
def main() -> None:

    service = build('calendar', 'v3', credentials=get_credentials())
    # publish_events(scraper.get_events, service)

    event = {
        'summary': 'Test Event',
        'start': {
            'date': '2021-07-18'
        },
        'end': {
            'date': '2021-07-18'
        }
    }

    publish_event(event, service)


if __name__ == '__main__':
    main()