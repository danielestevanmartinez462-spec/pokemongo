from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Gimnasio, entrenador, pokemon
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import PokemonCrecimientoSerializer
from .logic import ganar_experiencia, evoluciones_posibles, progreso_xp
 
XP_PERMITIDA = (50, 500)

def inicio(request):
    pokemones = list(pokemon.objects.all())
    for p in pokemones:
        info = progreso_xp(p)
        p.pct = info["porcentaje"]
        p.xp_actual = info["xp_actual"]
        p.xp_meta = info["xp_meta"]
        p.escala = info["escala"]
    return render(request, 'pokemon/inicio.html', {
        'pokemones': pokemones
    })
 
 
def lista_pokemones(request):
    pokemones = pokemon.objects.all()
    return render(request, 'pokemon/pokemones.html', {
        'pokemones': pokemones
    })
 
 
def lista_gimnasios(request):
    gimnasios = Gimnasio.objects.all()
    return render(request, 'pokemon/gimnasios.html', {
        'gimnasios': gimnasios
    })
 
 
def lista_entrenadores(request):
    entrenadores = entrenador.objects.all()
    return render(request, 'pokemon/entrenadores.html', {
        'entrenadores': entrenadores
    })
 
 
def crear_pokemon(request):
    entrenadores = entrenador.objects.all()
 
    if request.method == 'POST':
        pokemon.objects.create(
            nombre=request.POST.get('nombre'),
            peso=request.POST.get('peso'),
            imagen=request.POST.get('imagen'),
            entrenador_id=request.POST.get('entrenador') or None,
            habilidades=request.POST.get('habilidades'),
            naturaleza=request.POST.get('naturaleza'),
            elemento=request.POST.get('elemento'),
            descripcion=request.POST.get('descripcion')
        )
 
        return redirect('lista_pokemones')
 
    return render(request, 'pokemon/crear.html', {
        'entrenadores': entrenadores
    })
 
 
def editar_pokemon(request, id):
    pok = get_object_or_404(pokemon, id=id)
    entrenadores = entrenador.objects.all()
 
    if request.method == 'POST':
        pok.nombre = request.POST.get('nombre')
        pok.peso = request.POST.get('peso')
        pok.imagen = request.POST.get('imagen')
        pok.entrenador_id = request.POST.get('entrenador') or None
        pok.habilidades = request.POST.get('habilidades')
        pok.naturaleza = request.POST.get('naturaleza')
        pok.elemento = request.POST.get('elemento')
        pok.descripcion = request.POST.get('descripcion')
 
        pok.save()
        return redirect('lista_pokemones')
 
    return render(request, 'pokemon/editar.html', {
        'pok': pok,
        'entrenadores': entrenadores
    })
 
 
def eliminar_pokemon(request, id):
    pok = get_object_or_404(pokemon, id=id)
 
    if request.method == 'POST':
        pok.delete()
        return redirect('lista_pokemones')
 
    return render(request, 'pokemon/eliminar.html', {
        'pok': pok
    })
 
 
def entrenar_pokemon(request, id):
    """Botones 'Entrenar': suma 50 o 500 XP y vuelve a la misma tarjeta."""
    poke = get_object_or_404(pokemon, id=id)
 
    if request.method == 'POST':
        try:
            xp = int(request.POST.get('xp', 50))
        except (TypeError, ValueError):
            xp = 50
        if xp not in XP_PERMITIDA:
            xp = 50
 
        eventos = ganar_experiencia(poke, xp)
        messages.success(request, f"{poke.nombre}: " + " ".join(eventos))
 
    destino = request.META.get('HTTP_REFERER', '')
    if destino and url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}):
        return redirect(destino.split('#')[0] + f'#poke-{poke.id}')
    return redirect('inicio')
 
class CrecimientoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = pokemon.objects.select_related("entrenador").order_by("id")
    serializer_class = PokemonCrecimientoSerializer
 
    @action(detail=True, methods=["post"])
    def entrenar(self, request, pk=None):
        poke = self.get_object()
        try:
            xp = int(request.data.get("xp", 50))
        except (TypeError, ValueError):
            return Response({"error": "'xp' debe ser un número."}, status=status.HTTP_400_BAD_REQUEST)
        if not 1 <= xp <= 100000:
            return Response({"error": "'xp' debe estar entre 1 y 100000."}, status=status.HTTP_400_BAD_REQUEST)
 
        eventos = ganar_experiencia(poke, xp)
        return Response({"eventos": eventos, "pokemon": self.get_serializer(poke).data})
 
    @action(detail=True, methods=["get"])
    def evoluciones(self, request, pk=None):
        poke = self.get_object()
        return Response({"pokemon": poke.nombre, "nivel": poke.nivel,
                         "evoluciones": evoluciones_posibles(poke)})
