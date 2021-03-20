from django.db import models
from django.utils import timezone


class EventTemplate(models.Model):
    title = models.CharField(max_length=128, unique=True)
    creation_date = models.DateTimeField(editable=False, default=timezone.now)

    def __str__(self):
        return self.title


class Field(models.Model):
    title = models.CharField(max_length=128)
    representation = models.CharField(max_length=128)
    event_template = models.ForeignKey(
        EventTemplate,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    class Meta:
        unique_together = ['title', 'event_template']

    def __str__(self):
        return self.event_template.__str__() + ": " + self.title


class Member(models.Model):
    username = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    creation_date = models.DateTimeField(editable=False, default=timezone.now)

    def __str__(self):
        return self.username


class Event(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    creation_date = models.DateTimeField(editable=False, default=timezone.now)
    start_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    template = models.ForeignKey(
        EventTemplate,
        on_delete=models.RESTRICT,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class Participation(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
    )
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
    )
    creation_date = models.DateTimeField(editable=False, default=timezone.now)

    class Meta:
        unique_together = ['event', 'field', 'member']

    def get_participation_name(self):
        return self.event.__str__() + " - " + self.field.__str__() + " - " + self.member.__str__()

    def __str__(self):
        return self.get_participation_name()
