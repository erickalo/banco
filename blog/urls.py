from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('clientes/', views.clientes, name='clientes'),
    path('login/', views.login_user),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user),
    path('deposito/', views.deposito),
    path('depositar/', views.depositar),
    path('depositar/dep', views.deposito),
    path('sacar/', views.sacar),
    path('sacar/sac', views.saque),
    path('erro/', views.erro),
    path('clientes/dolar/', views.dolar)
]