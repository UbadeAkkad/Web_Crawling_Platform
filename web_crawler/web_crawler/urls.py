from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('crawler_api.urls')),
    path("django-rq/", include('django_rq.urls')),
    path('/', include('react_frontend.urls')),
]