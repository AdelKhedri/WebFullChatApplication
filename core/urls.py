from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, info


urlpatterns = [
    path('myadmin/', admin.site.urls),
    path('', include('user.urls')),
    path('chat/', include('chatapp.urls')),
    path('', home, name='home'),
    path('info',info, name='info'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)