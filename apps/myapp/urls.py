from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('addmovie', views.addmovie),
    path('displaymovie', views.displaymovie),
    path('showmovie/<id>', views.showmovie),
    path('favorite/<id>', views.favorite),
    path('unfavorite/<id>', views.unfavorite),
    path('delete/<id>', views.delete),
    path('processmovie', views.processmovie),
    path('login', views.login),
    path('logout', views.logout)
]
