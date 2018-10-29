from datetime import date, datetime, timedelta, timezone
import icalendar
from dateutil.rrule import *
import urllib.request
import pytz
import os

utc=pytz.UTC

def get_events_from_ics(ics_string, window_start, window_end):
    
    events = []

    def append_event(e):

        if e['startdt'] > window_end:
            return
        if e['enddt']:
            if e['enddt'] < window_start:
                return

        events.append(e)

    def get_recurrent_datetimes(recur_rule, start, exclusions):
        rules = rruleset()
        first_rule = rrulestr(recur_rule, dtstart=start)
        rules.rrule(first_rule)
        if not isinstance(exclusions, list):
            exclusions = [exclusions]

        for xdt in exclusions:
            try:
                rules.exdate(xdt.dt)
            except AttributeError:
                pass

        dates = []

       
        for d in rules.between(window_start, window_end):
            dates.append(d)
        return dates


    cal = filter(lambda c: c.name == 'VEVENT',
         icalendar.Calendar.from_ical(ics_string).walk()
        )

    def date_to_datetime(d):
        return datetime(d.year, d.month, d.day, tzinfo=timezone.utc)


    for vevent in cal:
        summary = str(vevent.get('summary'))
        description = str(vevent.get('description'))
        location = str(vevent.get('location'))
        rawstartdt = vevent.get('dtstart').dt
        rawenddt = rawstartdt + timedelta(minutes=1)
        if 'dtend' in vevent:
            rawenddt = vevent.get('dtend').dt
        allday = False
        if not isinstance(rawstartdt, datetime):
            allday = True
            startdt = date_to_datetime(rawstartdt)
            if rawenddt:
                enddt = date_to_datetime(rawenddt)
        else:
            startdt = rawstartdt
            enddt = rawenddt

        exdate = vevent.get('exdate')
        if vevent.get('rrule'):
            reoccur = vevent.get('rrule').to_ical().decode('utf-8')
            if vevent.get('rrule').get('UNTIL') is  None:
                continue
            end_time = vevent.get('rrule').get('UNTIL')[0]
            end_time = datetime(end_time.year, end_time.month, end_time.day)
            if end_time > datetime.now():
                for d in get_recurrent_datetimes(reoccur, startdt, exdate):
                    new_e = {
                        'startdt': d,      
                        'allday': allday,                  
                        'summary': summary,
                        'desc': description,
                        'loc': location
                        }
                    if enddt:
                        new_e['enddt'] = d + (enddt-startdt)                        
                    append_event(new_e)
        else:
            append_event({
                'startdt': startdt,
                'enddt': enddt,
                'allday': allday,
                'summary': summary,
                'desc': description,
                'loc': location
                })
    events.sort(key=lambda e: e['startdt'])
    return events
    
def lambda_handler(event, context):
    
    url = os.environ['CalendarUrl']
    course_keywords = os.environ['CourseKeywords']
    stack_id = os.environ['StackId']
    
    print(course_keywords)
    
    with urllib.request.urlopen(url) as response:
       ics_string = response.read()
    
    window_start = datetime.now(timezone.utc)
    window_end = window_start + timedelta(minutes=30)
    window_start = window_start - timedelta(hours=5)
    events = get_events_from_ics(ics_string, window_start, window_end)
    
    for e in events:
        print('{} - {}'.format(e['startdt'], e['summary']))
