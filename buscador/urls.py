from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^googleCS/', include('googleCS.urls')),
    url(r'^admin/', admin.site.urls),
]