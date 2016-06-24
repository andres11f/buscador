import sys
import json
import pycountry
from urllib.request import urlopen
from django.http import HttpResponse, Http404
from django.shortcuts import render
from apiclient.discovery import build
from .models import Patron, Enlace, Contenido
from django.core.files.base import ContentFile

# Bing API key
API_KEY = "af0EhUPMQ5EtWH2zO6y615x0FSBV0dnNyYVDSCW9x+U"

def buscar(request):
	categorias = {'Transporte', 'Mision', 'Vision', }
	ciudades = {'Pereira', 'Bogota'}
	resultados = list()

	paises = list()
	for c in pycountry.countries:
		paises.append(c.name)

	if request.method == 'POST':
		categoria = request.POST['categoria']
		patron = request.POST['patron']
		
		pais = ''
		ciudad = ''
		semilla = ''

		if request.POST['pais']: pais = request.POST['pais']
		if request.POST['ciudad']: ciudad = request.POST['ciudad']
		if request.POST['semilla']: semilla = request.POST['semilla']
		
		query = categoria + ' ' + patron

		if semilla:
			query = 'site:' + semilla + ' ' + categoria + ' ' + patron
			resultados = obtenerResultados(query=query)
		else:
			codPais = pycountry.countries.get(name=pais).alpha2
			query = 'location:' + codPais + ' ' + categoria + ' ' + patron
			resultados = obtenerResultados(query=query)

		patronAGuardar = Patron(categoria = categoria, semilla = semilla, pais = pais, ciudad = ciudad, patron = patron)
		patronAGuardar.save()
		guardarEnlaces(resultados, patronAGuardar)

		busquedaExitosa = True

	return render(request, 'search/inicio.html', locals())


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
	query = '%27' + urllib.parse.quote(query) + '%27'
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
	query = '%27' + urllib.parse.quote(query) + '%27'
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


def guardarEnlaces(resultados, patron):
	for link in resultados:
		enlace = Enlace(patron = patron, enlace = link)
		enlace.save()
		guardarContenido(link, patron, enlace)


def guardarContenido(link, patron, enlace):
	response = urlopen(link)
	webContent = response.read()

	contenido = Contenido(patron = patron, enlace = enlace)
	contenido.contenidoHoy.save(link.replace('http://','').replace('https://','').replace('/', '-'), ContentFile(webContent))
	contenido.save()