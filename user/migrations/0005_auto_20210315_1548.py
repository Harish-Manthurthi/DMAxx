# Generated by Django 2.2 on 2021-03-15 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_profileactivation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='car_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='car.CarModel'),
        ),
        migrations.DeleteModel(
            name='CarModel',
        ),
    ]
