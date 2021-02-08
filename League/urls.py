from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.inicio),
    path('carga/',views.carga),
    path('jugadores/', views.lista_jugadores),
    path('campeones/', views.lista_campeones),
    path('campeonespornombre/', views.buscarCampeonPorNombre),
    path('jugadorespornombre/', views.buscarJugadorPorNombre),
    path('jugadoresporservidor/', views.lista_jugadoresporservidor),
    ]
