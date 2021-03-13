from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    start_date = models.DateTimeField()
    active = models.BooleanField(default=True)


class Member(models.Model):
    username = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)


class Field(models.Model):
    title = models.CharField(max_length=128, unique=True)
    representation = models.CharField(max_length=128, unique=True)
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
    )
    participants = models.ManyToManyField(
        Member,
        through='Participation',
        through_fields=('field', 'member'),
    )


class Participation(models.Model):
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
    )
    