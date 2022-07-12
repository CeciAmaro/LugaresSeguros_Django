from django.urls import URLPattern, path
from initial import views

urlpatterns = [
    path('', views.HelloDrf.as_view(), name='index')
]