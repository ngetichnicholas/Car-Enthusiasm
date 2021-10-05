# Generated by Django 3.2.5 on 2021-10-05 16:54

from django.db import migrations, models
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('cars_app', '0004_auto_20211005_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='city',
            field=models.CharField(default='bomet', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='car',
            name='car_location',
            field=location_field.models.plain.PlainLocationField(max_length=63),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
