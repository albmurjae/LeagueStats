# Generated by Django 3.1.5 on 2021-01-29 15:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campeon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40, verbose_name='Nombre')),
                ('imagen', models.URLField()),
                ('winRate', models.DecimalField(decimal_places=1, max_digits=5)),
                ('banRate', models.DecimalField(decimal_places=1, max_digits=5)),
                ('popularidad', models.DecimalField(decimal_places=1, max_digits=5)),
                ('fechaLanzamiento', models.CharField(max_length=30, verbose_name='Fecha de lanzamiento')),
            ],
        ),
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40, verbose_name='Nombre')),
                ('imagen', models.URLField(max_length=300)),
                ('posicion', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('servidor', models.CharField(max_length=20, verbose_name='Servidor')),
                ('enlace', models.URLField()),
                ('sololiga', models.CharField(max_length=30, verbose_name='Liga Soloqueue')),
                ('solopl', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('solovictorias', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
    ]
