from icalendar import Calendar, Event
import tempfile, os


def __init__(self):
    print('cal_maker.py')


def converter(timetable):
    num_of_classes = len(timetable)
    print("Your total number of classes is: " + str(num_of_classes))

    #  Generating .ics file
    cal = Calendar()
    cal.add('PRODID', '-//Che-dev//timetable 1.0//EN')
    cal.add('version', '2.0')
    cal.add('CATEGORIES', 'EDUCATION')
    #cal.add('URL', "None") TODO: to be enabled on server version
    cal.add('NAME', 'University of Adelaide Timetable')
    cal.add('X-WR-CALNAME', 'University of Adelaide Timetable')



    for course in timetable:
        event = Event()
        event['SUMMARY'] = course['course']
        cal.add_component(event)






    print(cal.to_ical())

    directory = tempfile.mkdtemp()
    print(directory)
    f = open(os.path.join(directory, 'example.ics'), 'wb')
    f.write(cal.to_ical())
    f.close()
