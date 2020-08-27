# Generated by Django 3.1 on 2020-08-26 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200826_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
    ]