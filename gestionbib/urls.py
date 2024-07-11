from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

handler404 = 'adherants.views.handling_404'
handler500 = 'adherants.views.handling_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('ouvrages.urls')),
    path('', include('adherants.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
