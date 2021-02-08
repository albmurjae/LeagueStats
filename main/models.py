#encoding:utf-8
from django.db import models
from django.core.validators import MinValueValidator

class Campeon(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=40)
    imagen = models.URLField(max_length=200)
    winRate = models.DecimalField(max_digits=5, decimal_places=1)
    banRate = models.DecimalField(max_digits=5, decimal_places=1)
    popularidad = models.DecimalField(max_digits=5, decimal_places=1)
    fechaLanzamiento = models.CharField(verbose_name='Fecha de lanzamiento', max_length=50)

    def __str__(self):
        return self.imagen + '' + self.nombre 

class Jugador(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=40)
    imagen = models.URLField(max_length=300)
    posicion = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    servidor = models.CharField(verbose_name='Servidor', max_length=20)
    enlace = models.URLField(max_length=200)
    sololiga = models.CharField(verbose_name='Liga Soloqueue', max_length=30)
    solopl = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    solovictorias = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.posicion + self.nombre