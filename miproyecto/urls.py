from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ==============================================================================
# Configuración de URLs del Proyecto Principal
# ==============================================================================

urlpatterns = [
    # Panel de Administración de Django
    path('admin/', admin.site.urls),
    
    # Incluimos las URLs de nuestra aplicación 'vistas'
    # Esto delega el manejo de las rutas vacías ('') a vistas.urls
    path('', include('vistas.urls')),
]

# Configuración para servir archivos multimedia (imágenes subidas por usuarios)
# Solo funciona en modo DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
