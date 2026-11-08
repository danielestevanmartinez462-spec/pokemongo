from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pokemon import views

router = DefaultRouter()
router.register('crecimiento', views.CrecimientoViewSet, basename='crecimiento')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('pokemon/', views.lista_pokemones, name='lista_pokemones'),
    path('entrenadores/', views.lista_entrenadores, name='entrenadores'),
    path('gimnasios/', views.lista_gimnasios, name='gimnasios'),
    path('crear/', views.crear_pokemon, name='crear_pokemon'),
    path('editar/<int:id>/', views.editar_pokemon, name='editar_pokemon'),
    path('eliminar/<int:id>/', views.eliminar_pokemon, name='eliminar_pokemon'),
    path('entrenar/<int:id>/', views.entrenar_pokemon, name='entrenar_pokemon'),
    path('api/', include(router.urls)),
]