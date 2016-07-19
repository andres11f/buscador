from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.buscar, name='buscar'),
    url(r'^categorias/', views.mostrarCategorias, name='mostrarCategorias'),
]