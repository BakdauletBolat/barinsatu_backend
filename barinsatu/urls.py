from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve
import os
from .views import privacy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLUTTER_WEB_APP = os.path.join(BASE_DIR, 'web')

def flutter_redirect(request, resource):
    return serve(request, resource, FLUTTER_WEB_APP)

urlpatterns = [
    path('privacy/',privacy),
     path('api/',include('api.urls')),
    path('admin/', admin.site.urls),
    path('', lambda r: flutter_redirect(r, 'index.html')),
    path('<path:resource>', flutter_redirect),
   
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




