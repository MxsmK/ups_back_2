# Generated by Django 4.1.3 on 2022-11-04 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='book',
            name='max_dur',
            field=models.IntegerField(max_length=200),
        ),
        migrations.AlterField(
            model_name='reader',
            name='mail',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='rent',
            name='dur',
            field=models.IntegerField(),
        ),
    ]
