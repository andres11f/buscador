from django.contrib import admin

from .models import Patron, Enlace, Contenido

admin.site.register(Patron)
admin.site.register(Enlace)
admin.site.register(Contenido)