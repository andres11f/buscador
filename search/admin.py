from django.contrib import admin

from .models import Patron, Enlace, Contenido, Categoria, CategoriaEnlace

admin.site.register(Patron)
admin.site.register(Enlace)
admin.site.register(Contenido)
admin.site.register(Categoria)
admin.site.register(CategoriaEnlace)