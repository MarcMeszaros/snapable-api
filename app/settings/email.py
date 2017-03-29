# -*- coding: utf-8 -*-
import envitro

EMAIL_BACKEND = 'api.utils.email.SnapEmailBackend'
EMAIL_HOST = envitro.str('EMAIL_HOST', 'smtp.mailgun.org')
EMAIL_PORT = envitro.int('EMAIL_PORT', 587)
EMAIL_USE_TLS = envitro.bool('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = envitro.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = envitro.str('EMAIL_HOST_PASSWORD')

##### sendwithus #####
SENDWITHUS_KEY = envitro.str('SENDWITHUS_KEY') # no email
