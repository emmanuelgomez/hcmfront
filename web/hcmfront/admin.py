# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import calendar
from django.core.urlresolvers import reverse
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from utils import EventCalendar

from django.contrib import admin
from hcmfront.models import Availability, Input, MeetingRoom, Employee, ReservationMeetingRoom, RequestMeetingRoom

# Register your models here.


@admin.register(ReservationMeetingRoom)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['date', 'start_time', 'end_time', 'amount_people', 'meeting_room', 'employee', 'supplies']
    change_list_template = 'admin/events/change_list.html'

    def changelist_view(self, request, extra_context=None):
        after_day = request.GET.get('day__gte', None)
        extra_context = extra_context or {}

        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = datetime.date.today()

        previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
        previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
        previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                       day=1)  # find first day of previous month

        last_day = calendar.monthrange(d.year, d.month)
        next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
        next_month = next_month + datetime.timedelta(days=1)  # forward a single day
        next_month = datetime.date(year=next_month.year, month=next_month.month,
                                   day=1)  # find first day of next month

       # extra_context['previous_month'] = reverse('admin:events_changelist') + '?day__gte=' + str(
        #    previous_month)
        #extra_context['next_month'] = reverse('admin:events_changelist') + '?day__gte=' + str(next_month)

        cal = EventCalendar()
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        extra_context['calendar'] = mark_safe(html_calendar)
        return super(ReservationAdmin, self).changelist_view(request,extra_context)


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time']


@admin.register(Input)
class InputAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'capacity', 'availability', 'supplies']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(RequestMeetingRoom)
class RequestMeetingRoomAdmin(admin.ModelAdmin):
    list_display = ['status', 'reservation_meeting_room', 'employee', ]
