from django import forms

from .models import ReservationMeetingRoom

class PostForm(forms.ModelForm):

    class Meta:
        model = ReservationMeetingRoom
        fields = ('date', 'start_time', 'end_time', 'amount_people', 'employee', 'supplies', 'meeting_room')