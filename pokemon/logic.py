from .services import obtener_pokemon, obtener_especie, obtener_cadena

NIVEL_MAX = 100

_especies = {}
_cadenas = {}


def _especie(id_api):
    if id_api not in _especies:
        datos = obtener_especie(id_api)
        if not datos:
            return None
        _especies[id_api] = datos
    return _especies[id_api]


def _cadena(url):
    if url not in _cadenas:
        datos = obtener_cadena(url)
        if not datos:
            return None
        _cadenas[url] = datos
    return _cadenas[url]


def xp_para_nivel(grupo, n):
    if n <= 1:
        return 0
    if grupo == "fast":
        return int(4 * n**3 / 5)
    if grupo == "medium-slow":
        return max(0, int(6 / 5 * n**3 - 15 * n**2 + 100 * n - 140))
    if grupo == "slow":
        return int(5 * n**3 / 4)
    return n**3


def _id_api(poke):
    if poke.pokemon_id_api:
        return poke.pokemon_id_api
    datos = obtener_pokemon(poke.nombre.lower().strip())
    if datos:
        poke.pokemon_id_api = datos["id"]
        poke.save(update_fields=["pokemon_id_api"])
        return datos["id"]
    return None


def grupo_crecimiento(poke):
    id_api = _id_api(poke)
    especie = _especie(id_api) if id_api else None
    if especie:
        return especie["growth_rate"]["name"]
    return "medium-fast"


def _buscar_nodo(nodo, nombre):
    if nodo["species"]["name"] == nombre:
        return nodo
    for hijo in nodo["evolves_to"]:
        encontrado = _buscar_nodo(hijo, nombre)
        if encontrado:
            return encontrado
    return None


def evoluciones_posibles(poke):
    id_api = _id_api(poke)
    especie = _especie(id_api) if id_api else None
    if not especie:
        return []

    cadena = _cadena(especie["evolution_chain"]["url"])
    if not cadena:
        return []

    nodo = _buscar_nodo(cadena["chain"], poke.nombre.lower().strip())
    if not nodo:
        return []

    resultado = []
    for evo in nodo["evolves_to"]:
        for det in evo["evolution_details"]:
            if det["trigger"]["name"] == "level-up" and det.get("min_level"):
                resultado.append({
                    "nombre": evo["species"]["name"],
                    "id": int(evo["species"]["url"].rstrip("/").split("/")[-1]),
                    "nivel_requerido": det["min_level"],
                })
                break
    return resultado


def evolucionar(poke, evo):
    datos = obtener_pokemon(evo["id"])
    poke.pokemon_id_api = evo["id"]
    poke.nombre = evo["nombre"].title()
    if datos:
        imagen = datos["sprites"]["other"]["official-artwork"]["front_default"]
        poke.imagen = imagen or poke.imagen


def ganar_experiencia(poke, cantidad):
    eventos = []
    nivel_inicial = poke.nivel
    poke.experiencia += cantidad
    grupo = grupo_crecimiento(poke)

    while True:
        # subir de nivel mientras alcance la experiencia
        while (poke.nivel < NIVEL_MAX
               and poke.experiencia >= xp_para_nivel(grupo, poke.nivel + 1)):
            poke.nivel += 1

        # evolucionar si ya tiene el nivel pedido
        evo = None
        for e in evoluciones_posibles(poke):
            if poke.nivel >= e["nivel_requerido"]:
                evo = e
                break
        if not evo:
            break

        anterior = poke.nombre
        evolucionar(poke, evo)
        eventos.append(f"¡{anterior.title()} evolucionó a {poke.nombre}!")
        grupo = grupo_crecimiento(poke)

    if poke.nivel > nivel_inicial:
        eventos.insert(0, f"Subió del nivel {nivel_inicial} al {poke.nivel}.")
    if not eventos:
        eventos.append(f"Ganó {cantidad} XP.")

    poke.save()
    return eventos


def escala_por_nivel(nivel):
    # 0.70 en nivel 1, hasta 1.30 en nivel 50 o más
    return 0.7 + 0.6 * min(nivel, 50) / 50


def progreso_xp(poke):
    # con punto decimal para que el CSS lo entienda
    escala = f"{escala_por_nivel(poke.nivel):.2f}"

    if poke.nivel >= NIVEL_MAX:
        return {
            "porcentaje": 100,
            "xp_actual": poke.experiencia,
            "xp_meta": poke.experiencia,
            "escala": escala,
        }

    grupo = grupo_crecimiento(poke)
    base = xp_para_nivel(grupo, poke.nivel)
    meta = xp_para_nivel(grupo, poke.nivel + 1)
    total = max(meta - base, 1)
    actual = max(poke.experiencia - base, 0)
    porcentaje = max(0, min(100, int(actual / total * 100)))

    return {
        "porcentaje": porcentaje,
        "xp_actual": actual,
        "xp_meta": total,
        "escala": escala,
    }