from django.contrib import admin

# Register your models here.

from .models import EventTemplate, Event, Member, Field, Participation


class FieldInline(admin.StackedInline):
    model = Field
    extra = 3


class EventTemplateAdmin(admin.ModelAdmin):
    inlines = [FieldInline]
    list_display = ('title', 'creation_date')
    list_filter = ('creation_date',)
    search_fields = ('title',)


class ParticipationInline(admin.StackedInline):
    model = Participation
    extra = 1

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(ParticipationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'field':
            if request.__obj__ is not None:
                field.queryset = field.queryset.filter(event_template=request.__obj__.template)
            else:
                field.queryset = field.queryset.none()
        return field


class EventAdmin(admin.ModelAdmin):
    inlines = [ParticipationInline]
    list_display = ('title', 'start_date', 'active', 'template')
    readonly_fields = ('template',)
    list_filter = ('active', 'start_date', 'template')
    search_fields = ('title',)

    def get_form(self, request, obj=None, **kwargs):
        request.__obj__ = obj
        return super(EventAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(EventTemplate, EventTemplateAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Member)
