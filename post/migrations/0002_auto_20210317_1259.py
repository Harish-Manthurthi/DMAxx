# Generated by Django 2.2 on 2021-03-17 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='no_of_comments',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='no_of_like',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
