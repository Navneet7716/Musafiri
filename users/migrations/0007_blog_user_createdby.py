# Generated by Django 3.1.7 on 2021-05-18 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_history_hotel'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog_user',
            name='createdBy',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
