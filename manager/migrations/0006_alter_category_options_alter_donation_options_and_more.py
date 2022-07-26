# Generated by Django 4.0.6 on 2022-08-01 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_alter_donation_pick_up_comment_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Kategoria', 'verbose_name_plural': 'Kategorie'},
        ),
        migrations.AlterModelOptions(
            name='donation',
            options={'verbose_name': 'Darowizna', 'verbose_name_plural': 'Darowizny'},
        ),
        migrations.AlterModelOptions(
            name='institution',
            options={'verbose_name': 'Organizacja', 'verbose_name_plural': 'Organizacje'},
        ),
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.PositiveIntegerField(choices=[(3, 'Zbiórka Lokalna'), (1, 'Fundacja'), (2, 'Organizacja Pozarządowa')], default=1, verbose_name='Status organizacji'),
        ),
    ]
