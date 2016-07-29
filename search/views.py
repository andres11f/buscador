import sys
import json
import pycountry
import urllib
import requests
import json
from django.http import HttpResponse, Http404
from django.shortcuts import render
#from apiclient.discovery import build
from .models import Patron, Enlace, Categoria, CategoriaEnlace
from django.core.files.base import ContentFile
from requests.auth import HTTPBasicAuth
from django.template.defaulttags import register

# Bing API key
API_KEY = "af0EhUPMQ5EtWH2zO6y615x0FSBV0dnNyYVDSCW9x+U"

def buscar(request):
	categoriasOrdenadas = ordenarCategorias(Categoria.objects.all())

	resultados = list()
	paises = list()
	patrones = list()

	for c in pycountry.countries:
		paises.append(c.name)

	if request.method == 'POST':
		categoria = request.POST['categoria']
		patron = request.POST['patron1']
		patrones.append(request.POST['patron1'])

		#if request.POST['patron2']: patrones.append(request.POST['patron2'])
		#if request.POST['patron3']: patrones.append(request.POST['patron3'])
		#if request.POST['patron4']: patrones.append(request.POST['patron4'])
		#if request.POST['patron5']: patrones.append(request.POST['patron5'])

		print("-------------------------------------------")
		print(patrones)

		pais = ''
		semilla = ''

		if request.POST['pais']: pais = request.POST['pais']
		if request.POST['semilla']: semilla = request.POST['semilla']
		
		if '----' in categoria: categoria = categoria.strip('-')

		if semilla:
			query = 'site:' + semilla + ' ' + categoria + ' ' + patron
			resultados = obtenerResultados(query=query)
		else:
			codPais = pycountry.countries.get(name=pais).alpha2
			query = 'location:' + codPais + ' ' + categoria + ' ' + patron
			resultados = obtenerResultados(query=query)

		patronAGuardar = Patron(categoria = categoria, semilla = semilla, pais = pais, patron = patron)
		patronAGuardar.save()
		guardarEnlaces(resultados, patronAGuardar, categoria)

		busquedaExitosa = True

	return render(request, 'search/inicio.html', locals())

def mostrarCategorias(request):
	categoriasAMostrar = categoriasMostrar()

	return render(request, 'search/categorias.html', locals())

def categoriasMostrar():
	categorias = CategoriaEnlace.objects.all()
	categoriasAMostrar = dict()

	categoriasMostrar = list()

	for c in categorias:
		if c.categoria.nombre not in categoriasAMostrar.keys():
			categoriasAMostrar[c.categoria.nombre] = list()

	for c in categorias:
		categoriasAMostrar[c.categoria.nombre].append(c.enlace.enlace)
	return categoriasAMostrar


def ordenarCategorias(categorias):
	categoriasOrdenadas = list()
	for c in categorias:
		if c.categoriaPadre == 0:

			categoriasOrdenadas.append(c.nombre)
			
			for ca in categorias:
				if ca.categoriaPadre == c.id:
					categoriasOrdenadas.append("-----"+ca.nombre)

	return categoriasOrdenadas

def obtenerResultados(query):
	"""Returns the decoded json response content
    
    :param query: query for search
    :param source_type: type for seacrh result
    :param top: number of search result
    :param format: format of search result
    """

	source_type = "Web"
	top = 10
	format = 'json'
	resultados = list()

	# set search url
	query = '%27' + urllib.quote(query) + '%27'
	# web result only base url
	base_url = 'https://api.datamarket.azure.com/Bing/Search/v1/' + source_type
	url = base_url + '?Query=' + query + '&$top=' + str(top) + '&$format=' + format

	# create credential for authentication
	user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"
	# create auth object
	auth = HTTPBasicAuth(API_KEY, API_KEY)
	# set headers
	headers = {'User-Agent': user_agent}

	# get response from search url
	response_data = requests.get(url, headers=headers, auth = auth)
	# decode json response content
	json_result = response_data.json()

	outfile = open('results.txt', 'w')

	for l in json_result['d']['results']:
		outfile.write(l['Url'] + '\n')
		resultados.append(l['Url'])

	outfile.close()
	return resultados

def guardarEnlaces(resultados, patron, nombreCategoria):
	for link in resultados:
		enlace = Enlace(patron = patron, enlace = link)
		enlace.save()

		try:
			categoria = Categoria.objects.get(nombre = nombreCategoria)
		except Categoria.DoesNotExist:
			return

		cateEnlace = CategoriaEnlace(enlace = enlace, categoria = categoria)
		cateEnlace.save()

		#guardarContenido(link, patron, enlace)


def guardarContenido(link, patron, enlace):
	try:
		response = urlopen(link)
		webContent = response.read()
	except urllib.error.HTTPError:
		return

	contenido = Contenido(patron = patron, enlace = enlace)
	contenido.contenidoHoy.save(link.replace('http://','').replace('https://','').replace('/', '-'), ContentFile(webContent))
	contenido.save()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)