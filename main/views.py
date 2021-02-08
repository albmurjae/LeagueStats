#encoding:utf-8
from main.models import Campeon, Jugador
from main.forms import CampeonPorNombreForm, JugadorPorNombreForm
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup

import os
from whoosh import qparser
from whoosh.fields import DATETIME, TEXT, ID, NUMERIC, Schema
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser, QueryParser, OrGroup
import urllib.request
from urllib.request import Request, urlopen
import lxml
from datetime import datetime
from django.conf import settings

#función auxiliar que hace scraping en la web y carga los datos en la base datos
def populateDB():
    #variables para contar el número de registros que vamos a almacenar
    num_campeones = 0
    
    #borramos todas las tablas de la BD
    Campeon.objects.all().delete()
    
    #extraemos los datos de la web con BS
    #urllib inicio
    url = 'https://www.leagueofgraphs.com/'
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
    f = urlopen(req)
    s = BeautifulSoup(f, "lxml")

    lista_campeones = s.find("div", id="championListBox").find_all("div", class_="championBox")
    for link_campeon in lista_campeones:
        #urllib campeon
        url = 'https://www.leagueofgraphs.com/'+link_campeon.a['href']
        req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
        f = urlopen(req)
        s = BeautifulSoup(f, "lxml")

        imagen = s.find("div", class_="img").find("img")["src"]
        imagen = "https:"+imagen
        nombre = s.find("div", class_="txt").find("h2").string.strip()

        print(nombre)
        print("---------")

        #urllib stats
        if nombre == "Wukong":
            url = 'https://www.leagueofgraphs.com/champions/stats/' + "monkeyking"
            req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
            f = urlopen(req)
            s = BeautifulSoup(f, "lxml")
        else:
            url = 'https://www.leagueofgraphs.com/champions/stats/' + nombre.replace(" ","").replace("'","").replace(".","").lower()
            req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
            f = urlopen(req)
            s = BeautifulSoup(f, "lxml")

        winRate = s.find("div", id="graphDD2").string.strip()
        winRate = winRate.replace("%","")
        fechaLanzamiento = s.find("div", class_="number solo-number").string.strip()

        banRate = s.find("div", id="graphDD3").string.strip()
        banRate = banRate.replace("%","")
        popularidad = s.find("div", id="graphDD1").string.strip()
        popularidad = popularidad.replace("%","")
        
        c = Campeon.objects.create(nombre = nombre, 
                                imagen = imagen,
                                winRate = winRate,
                                banRate = banRate,
                                popularidad = popularidad,
                                fechaLanzamiento = fechaLanzamiento)
        num_campeones = num_campeones +1

        #creamos el schema
        schemCampeones = Schema(nombre=TEXT(stored=True),
        imagen=TEXT(stored=True), 
        winRate=NUMERIC(stored=True, decimal_places=1), 
        banRate=NUMERIC(stored=True, decimal_places=1), 
        popularidad=NUMERIC(stored=True, decimal_places=1), 
        fechaLanzamiento=TEXT(stored=True))

        main_dir = 'league'
        campeones_dir = main_dir + '/' + 'campeones'

        if not os.path.exists(main_dir):
            os.mkdir(main_dir)
        if not os.path.exists(campeones_dir):
            os.mkdir(campeones_dir)

        ix1 = create_in(campeones_dir, schema=schemCampeones)

        writer1 = ix1.writer()

        #añadimos al schema

        writer1.add_document(nombre = nombre, 
                                imagen = imagen,
                                winRate = winRate,
                                banRate = banRate,
                                popularidad = popularidad,
                                fechaLanzamiento = fechaLanzamiento)   
        writer1.commit()
    return ((num_campeones))


#función auxiliar que hace scraping en la web y carga los datos en la base datos
def populateDBJugadores():
    #variables para contar el número de registros que vamos a almacenar
    num_jugadores = 0
    
    #borramos todas las tablas de la BD
    Jugador.objects.all().delete()
    
    #extraemos los datos de la web con BS
    for i in range(1,6):
    #urllib inicio
        url = 'https://www.leagueofgraphs.com/es/rankings/summoners/page-'+format(i)
        req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
        f = urlopen(req)
        s = BeautifulSoup(f, "lxml")

        lista_jugadores = s.find("table", class_="data_table summonerRankingsTable with_sortable_column").find_all("tr")[1:]
        for lj in lista_jugadores:

            #urllib jugador
            prueba = lj.find("td", class_="text-right hide-for-small-down")
            if prueba == None:
              prueba == prueba 
            else:
                prueba = lj.find("img")
                if prueba == None:
                    imagen == "https://lolg-cdn.porofessor.gg/img/summonerIcons/11.2/36/29.png"
                else:
                    imagen = lj.find("img")["src"]
                    imagen = "https:"+imagen
                posicion = lj.find("td", class_="text-right hide-for-small-down").string.strip()
                posicion = posicion.replace(".","")
                nombre = lj.find("div", class_="txt").find("span", class_="name").string.strip()
                servidor = lj.find("div", class_="txt").find("i").string.strip()
                enlace = lj.a['href']
                enlace = "https://www.leagueofgraphs.com/" + enlace
        
  
                ls = lj.find("td", class_="text-center")
                sololiga = ls.find("div", class_="summonerTier").string.strip()
                solopl = ls.find("div", class_="leaguePoints").i.string.strip()
                solopl = solopl.replace("PL:","")
                solowins = ls.find("div", class_="wins").i.string.strip()
                solowins = solowins.replace("Victorias: ", "")

                print(nombre)
                print("---------")
        


        #almacenamos en la BD

                j = Jugador.objects.create(nombre = nombre, 
                                imagen = imagen,
                                posicion = posicion,
                                servidor = servidor,
                                enlace = enlace,
                                sololiga = sololiga,
                                solopl = solopl,
                                solovictorias = solowins)
                num_jugadores = num_jugadores +1

        #creamos el schema

                schemJugadores = Schema(nombre=TEXT(stored=True),
                imagen=TEXT(stored=True), 
                posicion=NUMERIC(stored=True), 
                servidor=TEXT(stored=True), 
                enlace=TEXT(stored=True), 
                sololiga=TEXT(stored=True), 
                solopl=NUMERIC(stored=True), 
                solovictorias=NUMERIC(stored=True))

                main_dir = 'league'
                jugadores_dir = main_dir + '/' + 'jugadores'

                if not os.path.exists(main_dir):
                    os.mkdir(main_dir)
                if not os.path.exists(jugadores_dir):
                    os.mkdir(jugadores_dir)
        
                ix2 = create_in(jugadores_dir, schema=schemJugadores)

                writer2 = ix2.writer()

        #añadimos al schema

                writer2.add_document(nombre = nombre, 
                                imagen = imagen,
                                posicion = posicion,
                                servidor = servidor,
                                enlace = enlace,
                                sololiga = sololiga,
                                solopl = solopl,
                                solovictorias = solowins) 
                writer2.commit()

    return ((num_jugadores))

#carga los datos desde la web en la BD
def carga(request):
 
    if request.method=='POST':
        if 'Aceptar' in request.POST:    
            num_jugadores = populateDBJugadores()  
            num_campeones = populateDB()
            mensaje="Se han almacenado: " + str(num_campeones) +" campeones y " + str(num_jugadores) + " jugadores." 
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')

#muestra el número de campeones y jugadores que hay en la BD
def inicio(request):
    num_campeones=Campeon.objects.all().count()
    num_jugadores=Jugador.objects.all().count()
    return render(request,'inicio.html', {'num_campeones':num_campeones, 'num_jugadores':num_jugadores})

#muestra un listado con los datos de los campeones
def lista_campeones(request):
    campeones=Campeon.objects.all()
    return render(request,'campeones.html', {'campeones':campeones})

#muestra un listado con los datos de los jugadores
def lista_jugadores(request):
    jugadores=Jugador.objects.all()
    return render(request,'jugadores.html', {'jugadores':jugadores})

#muestra la lista de jugadores agrupadas por servidor
def lista_jugadoresporservidor(request):
    jugadores=Jugador.objects.all().order_by('servidor')
    return render(request,'jugadoresporservidor.html', {'jugadores':jugadores})

#busqueda de campeones por nombre
def buscarCampeonPorNombre(request):
    formulario = CampeonPorNombreForm()
    campeones = None
    
    if request.method == 'POST':
        formulario = CampeonPorNombreForm(request.POST)
        if formulario.is_valid():
            campeones = Campeon.objects.filter(nombre=formulario.cleaned_data['nombrecampeon'])
    return render(request, 'campeonespornombre.html', {'formulario': formulario, 'campeones': campeones})

#busqueda de jugador por nombre
def buscarJugadorPorNombre(request):
    formulario = JugadorPorNombreForm()
    jugadores = None
    if request.method == 'POST':
        formulario = JugadorPorNombreForm(request.POST)
        if formulario.is_valid():
            jugadores = Jugador.objects.filter(nombre=formulario.cleaned_data['nombrejugador'])
    return render(request, 'jugadorespornombre.html', {'formulario': formulario, 'jugadores': jugadores})