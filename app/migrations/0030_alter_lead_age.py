# Generated by Django 4.0.6 on 2022-07-19 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_alter_lead_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='age',
            field=models.IntegerField(default=0),
        ),
    ]
