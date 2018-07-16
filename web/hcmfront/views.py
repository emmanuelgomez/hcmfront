# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from hcmfront.forms import ReservationMeetingRoomForm,RequestMeetingRoomForm
from hcmfront.models import ReservationMeetingRoom, MeetingRoom

from django.shortcuts import render
from django.shortcuts import redirect
from django.core import serializers
# Create your views here.


def reservation_new(request):
    if request.method == "POST":
        form = ReservationMeetingRoomForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.save()
            return redirect('index')
    else:
        form = ReservationMeetingRoomForm()
    return render(request, 'reservation.html', {'form': form})

def request_new(request):
    if request.method == "POST":
        form = RequestMeetingRoomForm(request.POST)
        if form.is_valid():
            requestRoom = form.save(commit=False)
            requestRoom.save()
            return redirect('index')
    else:
        form = RequestMeetingRoomForm()
    return render(request, 'request.html', {'form': form})


def index(request):
    return render(request, 'index.html')

def update_meeting_room_list(request):
    if request.method == "POST" and request.is_ajax():

        date = request.POST['date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        amount_people = request.POST['amount_people']
        supplies = request.POST['supplies[]']

        meeting_room = MeetingRoom.objects.filter(capacity__gte=amount_people, supplies__id=supplies).values_list('id', 'name')

        return JsonResponse({'results': list(meeting_room)})
    else:
        status= "Bad"
        return HttpResponse(status)