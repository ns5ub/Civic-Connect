from django.urls import path, include
from . import views
from django.views.generic import TemplateView


app_name = 'CivicConnect'

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path("logout/", views.logout_request, name="logout")
    #path('accounts/', include('allauth.urls')),
]
