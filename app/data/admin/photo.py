# -*- coding: utf-8 -*-
from django.contrib import admin

# models
from ..models import Guest, Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    exclude = ['metrics']
    list_display = ['id', 'event', 'caption', 'is_streamable', 'created_at']
    list_display_links = ['id', 'event']
    readonly_fields = ['id', 'event', 'created_at']
    search_fields = ['caption']
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'caption',
                'is_streamable',
                'created_at',
            )
        }),
        ('Ownership', {
            'classes': ('collapse',),
            'fields': (
                'event',
                'guest',
            )
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        object_id = filter(None, request.path.split('/'))[-1]
        photo = Photo.objects.get(pk=object_id)
        if db_field.name == 'guest':
            kwargs['queryset'] = Guest.objects.filter(event=photo.event)
        return super(PhotoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
