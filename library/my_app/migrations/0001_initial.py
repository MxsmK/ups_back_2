# Generated by Django 4.1.3 on 2022-11-03 18:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('foto', models.URLField()),
                ('birth', models.DateField()),
                ('death', models.DateField(default=None)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('max_dur', models.DurationField()),
                ('cover', models.URLField()),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.author')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('mail', models.EmailField(max_length=254)),
                ('fine', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(default=django.utils.timezone.now)),
                ('dur', models.DurationField()),
                ('fpd', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.book')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.reader')),
            ],
        ),
    ]
