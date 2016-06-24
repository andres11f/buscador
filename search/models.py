from django.db import models
from urllib.request import urlopen

class Patron(models.Model):
	id = models.AutoField(primary_key=True)
	categoria = models.CharField(max_length=20)
	semilla = models.URLField()
	pais = models.CharField(max_length=20)
	ciudad = models.CharField(max_length=20)
	patron = models.CharField(max_length=50)

	class Meta:
		verbose_name_plural=u'Patrones'

	def __str__(self):
		if self.semilla:
			return self.categoria+" "+self.semilla+" "+self.patron
		else:
			return self.categoria+" "+self.pais+" "+self.ciudad+" "+self.patron
		

class Enlace(models.Model):
	id = models.AutoField(primary_key=True)
	patron = models.ForeignKey(Patron)
	enlace = models.URLField()

	def __str__(self):
		return str(self.patron.id)+" "+self.enlace

class Contenido(models.Model):
	id = models.AutoField(primary_key=True)
	patron = models.ForeignKey(Patron)
	enlace = models.ForeignKey(Enlace)

	def url(self, filename):
		return "%s/%s/%s"%(self.patron.categoria, self.patron.id, filename)

	contenidoAyer = models.FileField(upload_to=url)
	contenidoHoy = models.FileField(upload_to=url)