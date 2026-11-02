
from django.shortcuts import render, redirect, get_object_or_404
from .models import Gimnasio, entrenador, pokemon


def inicio(request):
    pokemones = pokemon.objects.all()
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
