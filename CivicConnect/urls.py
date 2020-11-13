from django.urls import path, include
from . import views
#from django.views.generic import TemplateView


app_name = 'CivicConnect'
urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path("logout/", views.logout_request, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.update_profile, name="edit_profile"),
    path('representatives/', views.representatives, name='representatives'),
    path('contactrepresentative/', views.contactrepresentative, name='contactrepresentative'),
    #path('contactrepresentative/sendemail/' views.sendemail, name='sendemail'), ## for emails
    path("templatesubmission/", views.templatesubmission, name="templatesubmission"),
    path("templatesubmission/templates/", views.templates, name="templates"),
    #path("contactrepresentative/picktemp/", views.templates, name="templates"),
    #path("add_user/", views.signup, name="add_user"),
    #path('accounts/', include('allauth.urls')),
]
