from django.urls import path

from .views import (inicio,
                    registro,
                    loginViews,
                    logoutViews,
                    HomeUsuario,
                    jugar,
                    tablero,
                    contacto,
                    resultado_pregunta)

urlpatterns = [

    path('', inicio, name='inicio'),
    path('home/', HomeUsuario, name='home'),
    path('registro/', registro, name='registro'),
    path('login/', loginViews, name='login'),
    path('logout/', logoutViews, name='logout'),
    path('jugar/', jugar, name='jugar'),
    path('contacto/', contacto, name='contacto'),
    path('resultado/<int:pregunta_respondida_pk>/', resultado_pregunta, name='resultado'),
    path('tablero/', tablero, name='tablero')
    
]
