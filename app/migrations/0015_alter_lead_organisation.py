# Generated by Django 4.0.5 on 2022-06-12 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_lead_date_added_lead_description_lead_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.userprofile'),
        ),
    ]
