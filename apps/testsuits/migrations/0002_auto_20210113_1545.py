# Generated by Django 3.0 on 2021-01-13 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testsuits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testsuits',
            name='include',
            field=models.TextField(help_text='包含的接口id', verbose_name='包含的接口id'),
        ),
    ]
