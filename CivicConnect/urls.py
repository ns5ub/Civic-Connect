from django.urls import path, include
from . import views
from django.views.generic import TemplateView


app_name = 'CivicConnect'

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path("logout/", views.logout_request, name="logout"),
    path("profile/", views.update_profile, name="profile"),
    path("edit_profile/", views.logout_request, name="edit_profile"),
    path("add_user/", views.signup, name="add_user"),
    #path('accounts/', include('allauth.urls')),
]
