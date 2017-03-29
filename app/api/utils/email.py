# python
import json

# django/tastypie
from django.core.mail.backends.smtp import EmailBackend

class SnapEmailBackend(EmailBackend):

    def send_messages(self, email_messages):
        """
        Insert extra snapable headers into the email.
        """

        # custom headers
        email_headers = {
            #'X-SMTPAPI': json.dumps(sendgrid_header) # convert the sendgrid headers to json string
        }

        # merge in the new headers to existing email
        for email in email_messages:
            email.extra_headers = dict(email.extra_headers, **email_headers)

        # call the parent function to send email
        super(SnapEmailBackend, self).send_messages(email_messages)