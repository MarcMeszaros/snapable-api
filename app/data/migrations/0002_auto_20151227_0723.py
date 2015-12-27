# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_packages(apps, schema_editor):
    # We can't import the Package model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Package = apps.get_model("data", "Package")

    pkg1 = Package(
        name="Free",
        short_name="free",
        amount=0,
        is_enabled=True,
        items={
            "addons": [],
            "features": ["guest_reminders", "slideshow", "table_cards"],
            "modifiers": {
                "albums": 1,
                "price_per_print": 100
            }
        }
    )
    pkg1.save()

    pkg2 = Package(
        name="Standard",
        short_name="standard",
        amount=7900,
        is_enabled=False,
        items={
            "features": ["guest_reminders", "storage_12months", "table_cards"],
            "addons": [],
            "modifiers": {
                "price_per_print": 100
            }
        },
        interval="year",
        interval_count=1
    )
    pkg2.save()


    pkg3 = Package(
        name="Standard",
        short_name="standard",
        amount=4900,
        is_enabled=True,
        items={
            "features": ["guest_reminders", "storage_12months", "table_cards"],
            "addons": [],
            "modifiers": {
                "price_per_print": 100
            }
        },
        interval="year",
        interval_count=1
    )
    pkg3.save()

class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_packages),
    ]
