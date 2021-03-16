from django.contrib import admin

# Register your models here.

from .models import Event, Member, Field, Participation


class FieldInline(admin.StackedInline):
    model = Field
    extra = 3


class EventAdmin(admin.ModelAdmin):
    inlines = [FieldInline]
    list_display = ('title', 'start_date', 'active')

admin.site.register(Event, EventAdmin)
admin.site.register(Member)
admin.site.register(Participation)
