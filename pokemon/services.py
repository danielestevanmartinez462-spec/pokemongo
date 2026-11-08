import requests
from functools import lru_cache

BASE = "https://pokeapi.co/api/v2"


def _get(url):
    try:
        r = requests.get(url, timeout=10)
        return r.json() if r.status_code == 200 else None
    except requests.RequestException:
        return None


@lru_cache(maxsize=256)
def obtener_pokemon(nombre_o_id):
    return _get(f"{BASE}/pokemon/{nombre_o_id}/")


@lru_cache(maxsize=256)
def obtener_especie(nombre_o_id):
    return _get(f"{BASE}/pokemon-species/{nombre_o_id}/")


@lru_cache(maxsize=256)
def obtener_cadena(url):
    return _get(url)