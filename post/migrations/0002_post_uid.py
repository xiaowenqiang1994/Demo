# Generated by Django 3.2.11 on 2022-02-15 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='uid',
            field=models.IntegerField(default=1),
        ),
    ]
