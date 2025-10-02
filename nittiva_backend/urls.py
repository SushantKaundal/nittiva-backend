from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from api.views import healthz, readyz 


urlpatterns = [
    path('healthz/', healthz, name='healthz'),   # <-- New
    path('readyz/', readyz, name='readyz'),      # <-- New


    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('api/', include('api.urls')),
]