from django.urls import path
from . import views

app_name = 'rota'

urlpatterns = [
    path('', views.index, name='index'),
    path('contato/', views.contato, name='contato'),
]
