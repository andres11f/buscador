from django.db import models
from urllib.request import urlopen

class Patron(models.Model):
	id = models.AutoField(primary_key=True)
	categoria = models.CharField(max_length=20)
	semilla = models.URLField()
	pais = models.CharField(max_length=20)
	patron = models.CharField(max_length=50)

	class Meta:
		verbose_name_plural=u'Patrones'

	def __str__(self):
		if self.semilla:
			return self.categoria+" "+self.semilla+" "+self.patron
		else:
			return self.categoria+" "+self.pais+" "+self.patron
		

class Enlace(models.Model):
	id = models.AutoField(primary_key=True)
	patron = models.ForeignKey(Patron)
	enlace = models.URLField()

	def __str__(self):
		return self.enlace

class Contenido(models.Model):
	id = models.AutoField(primary_key=True)
	patron = models.ForeignKey(Patron)
	enlace = models.ForeignKey(Enlace)

	def url(self, filename):
		if len(filename) > 80:
			filename = filename[:80]
		return "%s/%s/%s"%(self.patron.categoria, self.patron.id, filename)

	contenidoAyer = models.FileField(upload_to=url, max_length=200)
	contenidoHoy = models.FileField(upload_to=url, max_length=200)

class Categoria(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=50)
	categoriaPadre = models.IntegerField()

	def __str__(self):
		return str(self.nombre)

class CategoriaEnlace(models.Model):
	id = models.AutoField(primary_key=True)
	enlace = models.ForeignKey(Enlace)
	categoria = models.ForeignKey(Categoria)