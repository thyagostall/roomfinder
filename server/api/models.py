from django.db import models


class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)


class Professor(models.Model):
    name = models.CharField(max_length=50)


class Session(models.Model):
    code = models.CharField(max_length=5)
    course = models.ForeignKey(Course)
    professors = models.ManyToManyField(Professor)


class Room(models.Model):
    number = models.CharField(max_length=10)
    locked = models.BooleanField()


class Schedule(models.Model):
    time = models.CharField(max_length=5)
    room = models.ForeignKey(Room)
    session = models.ForeignKey(Session)
