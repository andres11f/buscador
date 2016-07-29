from django.contrib import admin

from .models import Patron, Enlace, Categoria, CategoriaEnlace

admin.site.register(Patron)
admin.site.register(Enlace)
admin.site.register(Categoria)
admin.site.register(CategoriaEnlace)