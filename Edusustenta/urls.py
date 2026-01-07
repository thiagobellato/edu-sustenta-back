from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path('', home),                     # status da API
    path('admin/', admin.site.urls),     # Django Admin
    path('api/', include('core.urls')),  # API REST
]
