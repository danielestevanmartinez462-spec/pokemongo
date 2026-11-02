
from django.contrib import admin
from django.urls import path
from pokemon import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('pokemon/', views.lista_pokemones, name='lista_pokemones'),
    path('entrenadores/', views.lista_entrenadores, name='entrenadores'),
    path('gimnasios/', views.lista_gimnasios, name='gimnasios'),
    path('crear/', views.crear_pokemon, name='crear_pokemon'),
    path('editar/<int:id>/', views.editar_pokemon, name='editar_pokemon'),
    path('eliminar/<int:id>/', views.eliminar_pokemon, name='eliminar_pokemon'),
]