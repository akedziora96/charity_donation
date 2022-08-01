# Generated by Django 4.0.6 on 2022-08-01 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_alter_category_options_alter_donation_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.PositiveIntegerField(choices=[(3, 'Zbiórka Lokalna'), (2, 'Organizacja Pozarządowa'), (1, 'Fundacja')], default=1, verbose_name='Status organizacji'),
        ),
    ]
