# Generated by Django 4.0.5 on 2022-07-06 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_lead_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures'),
        ),
    ]
