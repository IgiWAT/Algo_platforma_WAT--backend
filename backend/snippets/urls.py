from django.urls import path
from . import views

urlpatterns = [
    path('', views.snippet_list, name="lista_kodow"),
    path('nowy/', views.snippet_new, name="nowy_kod"),
    path('<int:pk>/', views.snippet_detail, name='szczegoly_kodu'),
    path('rejestracja/', views.rejestracja, name='rejestracja')
]