# Generated by Django 4.0.5 on 2022-07-16 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_lead_age_alter_lead_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='phone_number',
            field=models.IntegerField(),
        ),
    ]
