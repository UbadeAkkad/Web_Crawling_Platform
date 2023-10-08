from django.urls import path
from .views import Reactindex

urlpatterns = [
    path('', Reactindex,name="reactapp"),
    path('<path:path>', Reactindex),
]