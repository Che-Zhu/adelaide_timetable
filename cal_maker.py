from icalendar import Calendar, Event
from datetime import datetime
import pytz
import random
import os

au_timezone = pytz.timezone('Australia/Adelaide')


def timezone_adelaide_to_utc(adelaide_time):
    local = au_timezone.localize(adelaide_time)
    utc_time = local.astimezone(pytz.utc)
    return utc_time.strftime('%Y%m%dT%H%M%SZ')


def converter(timetable):
    num_of_classes = len(timetable)

    #  Generating .ics file
    cal = Calendar()
    cal.add('PRODID', '-//Che-dev//timetable//EN')
    cal.add('version', '2.0')
    cal.add('CATEGORIES', 'EDUCATION')
    # cal.add('URL', "None") TODO: to be enabled on server version
    cal.add('NAME', 'UoA Timetable v1.0-beta')
    cal.add('X-WR-CALNAME', 'UoA Timetable v1.0-beta')

    for course in timetable:
        current_time = datetime.now(tz=pytz.utc).strftime('%Y%m%dT%H%M%SZ')
        start_time = course['date'] + course['start_time']
        start_time = datetime.strptime(start_time, '%Y-%m-%d%H:%M')

        end_time = course['date'] + course['end_time']
        end_time = datetime.strptime(end_time, '%Y-%m-%d%H:%M')

        event = Event()
        event['dtstamp'] = current_time
        event['uid'] = current_time + str(start_time) + str(random.randint(1, 1000)) + 'Che-dev@outlook.com'

        event['dtstart'] = timezone_adelaide_to_utc(start_time)
        event['dtend'] = timezone_adelaide_to_utc(end_time)

        event['SUMMARY'] = course['type'] + ': ' + course['course']
        cal.add_component(event)

    f = open(os.path.join(os.getcwd(), 'generated.ics'), 'wb')
    f.write(cal.to_ical())
    f.close()
    print('Your timetable generated.ics has been successfully exported in directory: {} with {} classes.'
          .format(os.getcwd(), str(num_of_classes)))
