# Generated by Django 4.0.6 on 2022-08-11 17:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_alter_donation_created_alter_institution_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 11, 17, 10, 37, 769224, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.PositiveIntegerField(choices=[(3, 'Zbiórka Lokalna'), (1, 'Fundacja'), (2, 'Organizacja Pozarządowa')], default=1, verbose_name='status organizacji'),
        ),
    ]
