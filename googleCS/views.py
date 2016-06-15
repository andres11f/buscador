import sys
import json
import pycountry
import urllib2
from django.http import HttpResponse, Http404
from django.shortcuts import render
from apiclient.discovery import build
from .models import Patron, Enlace


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
		
		if semilla:
			resultados = obtenerResultados(patron = patron, semilla = semilla)
		else:
			codPais = pycountry.countries.get(name=pais).alpha2
			resultados = obtenerResultados(patron = patron, pais = codPais, ciudad = ciudad)

		patronAGuardar = Patron(categoria = categoria, semilla = semilla, pais = pais, ciudad = ciudad, patron = patron)
		patronAGuardar.save()
		guardarEnlaces(resultados, patronAGuardar)

		busquedaExitosa = True

	return render(request, 'googleCS/inicio.html', locals())


def obtenerResultados(patron, semilla = "", pais = "", ciudad = ""):
	queries = 1
	i=1
	resultados = list()

	sys.modules['win32file'] = None

	service = build("customsearch", "v1", developerKey="AIzaSyAiVwIiFOvU7bCeAIP3OyddnKUZpMspmtE")

	rawResponse = open('response.json', 'w')
	outfile = open('links.txt', 'w')

	while(i < queries*10):
		i += 10

		#q = search expression
		#cr = country, example: cr = countryCA (canada)
		#exactTerms = Identifies a phrase that all documents in the search results must contain.
		#excludeTerms = Identifies a word or phrase that should not appear in any documents in the search results.
		#fileType = Restricts results to files of a specified extension.
		#gl = The gl parameter value is a two-letter country code. The gl parameter boosts search results whose country of origin matches the parameter value. See the Country Codes page for a list of valid values.
		#googlehost = The local Google domain (for example, google.com, google.de, or google.fr) to use to perform the search. 
		#siteSearch = Specifies all search results should be pages from a given site.
		if semilla:
			response = service.cse().list(q= patron, siteSearch = semilla, cx='005068117274016516848:ynp2_vaekys', googlehost='google.com', start = i).execute()
		else:
			response = service.cse().list(q= patron + " " + ciudad, cr = pais, cx='005068117274016516848:ynp2_vaekys', googlehost='google.com', start = i).execute()

		json.dump(response, rawResponse, sort_keys=True)

		for l in response.get('items', []):
			outfile.write(l['link'] + '\n')
			resultados.append(l['link'])

	outfile.close()
	rawResponse.close()
	return resultados


def guardarEnlaces(resultados, patron):
	for link in resultados:
		enlace = Enlace(patron = patron, enlace = link)
		guardarContenido(link, patron, enlace)
		enlace.save()

def guardarContenido(link, patron, enlace):
	response = urllib2.urlopen(link)
	webContent = response.read()

	f = open('webpages/' + link + '.html', 'w')
	f.write(webContent)
	
	contenido = Contenido(patron = patron, enlace = enlace, contenidoHoy = f)

	f.close()