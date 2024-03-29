# UoG Calendar

> Not affiliated with the University of Guelph

Web scraper to gets events from the University of Guelph's [Schedule of Dates](https://calendar.uoguelph.ca/undergraduate-calendar/schedule-dates/) page and add them to a user's google calendar.

The calendar includes only the events from the standard 12 week undergraduate tables meaning the 6 week summer session events and all D.V.M. semester events are not included

**Click [here](https://calendar.google.com/calendar/u/0?cid=YmU3ZDZjYzgxNTc0ZGExMWMyNTMxOGE5NDBlZTI1NWQwNTJmYWQyMjA2NTk0NzZlNDUzNWQwMTAyM2I2MzA4MUBncm91cC5jYWxlbmRhci5nb29nbGUuY29t) to add the events to your own calendar.**

You can also download the most recent `.ics` file from the `calendars` directory

### Requirements

- Python 3+

```bash
# install all required dependancies
$ pip install -r requirements.txt
```

### Resources

Google Calendar API - [https://developers.google.com/calendar/api](https://developers.google.com/calendar/api)

### Potential Future Plans

- create a database to store calendar events and auto update google calendar when new events are found
