from django import forms
from django.contrib.admin import widgets

from .models import ReservationMeetingRoom,RequestMeetingRoom

class ReservationMeetingRoomForm(forms.ModelForm):

    class Meta:
        model = ReservationMeetingRoom
        fields = ('date', 'start_time', 'end_time', 'amount_people', 'employee', 'supplies', 'meeting_room')
        widgets = {
             'date': forms.DateInput(attrs={'class': 'datepicker'}),
             'start_time': forms.TimeInput(attrs={'class': 'timepicker'}),
             'end_time': forms.TimeInput(attrs={'class': 'timepicker'}),

        }

class RequestMeetingRoomForm(forms.ModelForm):

    class Meta:
        model = RequestMeetingRoom
        fields = ('reservation_meeting_room', 'employee')


