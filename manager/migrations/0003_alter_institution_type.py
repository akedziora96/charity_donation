# Generated by Django 4.0.6 on 2022-07-26 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_alter_institution_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.PositiveIntegerField(choices=[(2, 'organizacja pozarządowa'), (3, 'zbiórka lokalna'), (1, 'fundacja')], default=1, verbose_name='status organizacji'),
        ),
    ]
