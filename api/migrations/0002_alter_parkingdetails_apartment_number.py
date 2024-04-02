# Generated by Django 5.0.1 on 2024-04-01 05:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingdetails',
            name='apartment_number',
            field=models.ForeignKey(blank=True, help_text='Apartment associated with the parking space.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parking_spaces', to='api.apartmentdetails'),
        ),
    ]
