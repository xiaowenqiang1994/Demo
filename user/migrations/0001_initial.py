# Generated by Django 3.2.11 on 2022-02-09 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, max_length=64, null=True, unique=True)),
                ('password', models.CharField(blank=True, max_length=128, null=True)),
                ('icon', models.ImageField(upload_to='')),
                ('age', models.IntegerField()),
                ('sex', models.CharField(choices=[('M', '男'), ('F', '女'), ('U', '保密')], max_length=8)),
            ],
        ),
    ]
