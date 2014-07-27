# django/tastypie/libs
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# snapable
import admin

@python_2_unicode_compatible
class Guest(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'
    
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

    name = models.CharField(max_length=255, help_text='The guest name.')
    email = models.CharField(max_length=255, help_text='The guest email address.')
    is_invited = models.BooleanField(default=False, help_text='If the guest has been invited.')
    created_at = models.DateTimeField(auto_now_add=True, help_text='The guest timestamp.')

    # virtual properties #
    # return the number of photos related to this event
    @property
    def photo_count(self):
        return self.photo_set.count()

    def __str__(self):
        return u'{0} ({1})'.format(self.name, self.email)

    def __repr__(self):
        return str({
            'created_at': self.created_at,
            'email': self.email,
            'event': self.event,
            'is_invited': self.is_invited,
            'name': self.name,
            'photo_count': self.photo_count,
        })

class GuestAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'name', 'is_invited', 'created_at']
    readonly_fields = ['id', 'created_at', 'event']
    search_fields = ['email', 'name']
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'email', 
                'name',
                'is_invited',
                'created_at',
            ),
        }),
        ('Ownership', {
            'classes': ('collapse',),
            'fields': (
                'event',
            )
        }),
    )

admin.site.register(Guest, GuestAdmin)
