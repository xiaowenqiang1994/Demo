# Generated by Django 3.2.11 on 2022-02-15 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('name', models.CharField(max_length=64)),
                ('content', models.TextField()),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='uid',
            field=models.IntegerField(),
        ),
    ]