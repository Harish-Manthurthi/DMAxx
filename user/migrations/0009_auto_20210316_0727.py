# Generated by Django 2.2 on 2021-03-16 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20210316_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forgetpasswordotp',
            name='expired_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profileactivation',
            name='expired_status',
            field=models.BooleanField(default=False),
        ),
    ]
