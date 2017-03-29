# -*- coding: utf-8 -*-
import envitro

##### Stripe #####
STRIPE_KEY_SECRET = envitro.str('STRIPE_KEY_SECRET')
STRIPE_KEY_PUBLIC = envitro.str('STRIPE_KEY_PUBLIC')
STRIPE_CURRENCY = envitro.str('STRIPE_CURRENCY', 'usd')

# setup stripe
import stripe
stripe.api_key = STRIPE_KEY_SECRET
