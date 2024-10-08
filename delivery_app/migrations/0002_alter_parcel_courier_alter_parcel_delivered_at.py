# Generated by Django 5.1.1 on 2024-09-04 09:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='courier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courier_parcels', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
