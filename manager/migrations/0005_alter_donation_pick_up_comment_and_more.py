# Generated by Django 4.0.6 on 2022-08-01 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_remove_donation_adress_donation_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='pick_up_comment',
            field=models.TextField(verbose_name='Komentarz'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, 'Fundacja'), (2, 'Organizacja Pozarządowa'), (3, 'Zbiórka Lokalna')], default=1, verbose_name='Status organizacji'),
        ),
    ]
