from django.contrib import admin
from main.models import Jugador, Campeon

#registramos en el administrador de django los modelos 

admin.site.register(Jugador)
admin.site.register(Campeon)