# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Availability(models.Model):
    start_time = models.TimeField(u'Hora  de Inicio', help_text=u'Horario de Disponibilidad')
    end_time = models.TimeField(u'Hora de Fin', help_text=u'Horario de Disponibilidad')

    def __str__(self):
        return u'%s : %s' % (self.start_time, self.end_time)

    class Meta:
        verbose_name = u'Horario de Disponibilidad'
        verbose_name_plural = u'Horarios Disponibles'

class Input(models.Model):
    name = models.CharField(u'Nombre', help_text=u'Nombre del Insumo', max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Insumo'
        verbose_name_plural = u'Insumos'


class MeetingRoom(models.Model):
    name = models.CharField(u'Nombre', help_text=u'Nombre de la Sala', max_length=250)
    location = models.CharField(u'Ubicacion', help_text=u'Ubicacion de la Sala', blank=True, null=True, max_length=500)
    capacity = models.IntegerField(u'Capacidad', help_text=u'Capacidad de la Sala')

    availability = models.ManyToManyField(Availability, verbose_name=u'Horarios Disponibles', help_text=u'Lista de horarios disponibles.')
    supplies = models.ManyToManyField(Input, verbose_name=u'Insumos', help_text=u'Lista de insumos disponibles.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Sala de Reuniones'
        verbose_name_plural = u'Salas de Reuniones'


class Employee(models.Model):
    name = models.CharField(u'Nombre', help_text=u'Nombre del Empleado', max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Empleados'
        verbose_name_plural = u'Empleados'


class ReservationMeetingRoom(models.Model):
    date = models.DateField(u'Fecha', help_text=u'Fecha de inicio de la Reservacion')
    start_time = models.TimeField(u'Hora  de Inicio', help_text=u'Horario de la Reservacion')
    end_time = models.TimeField(u'Hora de Fin', help_text=u'Horario de la Reservacion')
    amount_people = models.IntegerField(u'Cantidad de Personas', help_text=u'Cantidad de Personas de la Reservacion')

    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE, verbose_name=u'Sala de Reuniones', help_text=u'Sala de Reunion reservada.')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=u'Empleado', help_text=u'Empleado que realiza la reservacion.')
    supplies = models.ManyToManyField(Input, verbose_name=u'Lista de insumos', help_text=u'Insumos seleccionados para la reservacion.')

    def __str__(self):
        return u'%s %s:%s' % (self.date, self.start_time, self.end_time)

    class Meta:
        verbose_name = u'Reservacion'
        verbose_name_plural = u'Reservaciones'

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (
                new_end >= fixed_start and new_end <= fixed_end):  # innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
            overlap = True

        return overlap

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.start_time))

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Ending times must after starting times')

        reservations = ReservationMeetingRoom.objects.filter(day=self.day)
        if reservations.exists():
            for reservation in reservations:
                if self.check_overlap(reservation.start_time, reservation.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        'There is an overlap with another reservation: ' + str(reservation.day) + ', ' + str(
                            reservation.start_time) + '-' + str(reservation.end_time))


class RequestMeetingRoom(models.Model):
    status = models.NullBooleanField(u'Estado', help_text=u'Especifica si la peticion fue aceptada', blank=True, null=True)

    reservation_meeting_room = models.ForeignKey(ReservationMeetingRoom, on_delete=models.CASCADE, verbose_name=u'Reservacion', help_text=u'Reservacion de Sala de Reservacion a la cual se realiza la peticion.')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=u'Empleado', help_text=u'Empleado que realiza la peticion.')

    def __str__(self):
        return u'%s %s:%s' % (self.employee.name, self.reservation_meeting_room, self.status)

    class Meta:
        verbose_name = u'Solicitar Sala de Reuniones'
        verbose_name_plural = u'Solicitudes de Salas de Reuniones'