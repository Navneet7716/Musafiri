# Generated by Django 3.1.7 on 2021-05-18 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210518_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='train',
            name='companyName',
            field=models.CharField(max_length=300),
        ),
    ]
