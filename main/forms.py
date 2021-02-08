#encoding:utf-8
from django import forms
   

class CampeonPorNombreForm(forms.Form):
    nombrecampeon = forms.CharField(label="Nombre del Campeón", widget=forms.TextInput, required=True)

class JugadorPorNombreForm(forms.Form):
    nombrejugador = forms.CharField(label="Nombre del Jugador", widget=forms.TextInput, required=True)
