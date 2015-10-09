from django.db import models

# Create your models here.
class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

class Professor(models.Model):
    name = models.CharField(max_length=50)

class Session(models.Model):
    code = models.CharField(max_length=5)
    course = models.ForeignKey(Course)
    professors = models.ManyToManyField(Professor)

class Schedule(models.Model):
    time = models.CharField(max_length=5)
    room = models.CharField(max_length=10)
    session = models.ForeignKey(Session)
