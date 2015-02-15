# django/tastypie/libs
from django.contrib import admin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import models
from django.template.loader import get_template
from django.template import Context
from django.utils.encoding import python_2_unicode_compatible

# snapable
import dashboard


@python_2_unicode_compatible
class Guest(models.Model):

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

    def send_email(self, message=''):
        # load in the templates
        plaintext = get_template('guest_invite.txt')
        html = get_template('guest_invite.html')

        # setup the template context variables
        d = Context({
            'message': message,
            'toname': self.name,
            'fromname': self.event.account.users.all()[0].name,
        })

        # build the email
        subject, from_email, to = 'At {0} use Snapable!'.format(self.event.title), 'robot@snapable.com', [self.email]
        text_content = plaintext.render(d)
        html_content = html.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # set the invited flag
        self.is_invited = True
        self.save()


#===== Admin =====#

@admin.register(Guest, site=dashboard.site)
class GuestAdmin(admin.ModelAdmin):
    actions = ['send_email_invite', 'reset_email_invite_flag']
    list_display = ['id', 'email', 'name', 'is_invited', 'created_at', 'event_id', 'event_title', 'event_url']
    list_select_related = ['event']
    readonly_fields = ['id', 'created_at', 'event']
    search_fields = ['email', 'name', '=event__pk', '^event__title', '^event__url']
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

    def event_id(self, object):
        return object.event.pk

    def event_title(self, object):
        return object.event.title

    def event_url(self, object):
        return object.event.url

    def send_email_invite(self, request, queryset):
        for guest in queryset.iterator():
            guest.send_email()
        self.message_user(request, "Successfully sent email.")

    def reset_email_invite_flag(self, request, queryset):
        for guest in queryset.iterator():
            guest.is_invited = False
            guest.save()
        self.message_user(request, "Successfully sent email.")
