from calendar import HTMLCalendar, LocaleHTMLCalendar
from datetime import datetime as dtime, date, time
from django.urls import reverse
import datetime
from .models import Scheduler


class EventCalendar(LocaleHTMLCalendar):
    
    def __init__(self, events=None, *args, **kwargs):
        super().__init__()
        self.events = events

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell
        """
        events_from_day = events.filter(day__day=day)
        events_html = "<ul>"
        for event in events_from_day:
            events_html += event.get_absolute_url() + "<br>"
        events_html += "</ul>"
 
        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            # <a href="%s">Ver detalles dia</a>
            return '<td class="%s">%d&nbsp;%s</td>' % (
                self.cssclasses[weekday],
                day,
                #reverse('admin:schedules_schedulerday_changelist') + '?created__day=7&created__month=12&created__year=2018',
                events_html)
 
    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s
 
    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
 
        events = Scheduler.objects.filter(day__month=themonth)
 
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)