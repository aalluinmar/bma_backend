# Generated by Django 5.0.1 on 2024-04-12 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leasedetails',
            name='duration',
            field=models.PositiveIntegerField(choices=[(6, '6 months'), (9, '9 months'), (12, '12 months')], help_text='Duration of the lease in months.'),
        ),
    ]