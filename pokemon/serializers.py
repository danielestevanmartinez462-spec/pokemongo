from rest_framework import serializers
from .models import pokemon
from .logic import xp_para_nivel, grupo_crecimiento, evoluciones_posibles, NIVEL_MAX


class PokemonCrecimientoSerializer(serializers.ModelSerializer):
    entrenador_nombre = serializers.SerializerMethodField()
    grupo_crecimiento = serializers.SerializerMethodField()
    progreso = serializers.SerializerMethodField()
    proxima_evolucion = serializers.SerializerMethodField()

    class Meta:
        model = pokemon
        fields = ["id", "nombre", "imagen", "elemento", "entrenador", "entrenador_nombre",
                  "nivel", "experiencia", "grupo_crecimiento", "progreso", "proxima_evolucion"]
        read_only_fields = fields

    def get_entrenador_nombre(self, obj):
        return f"{obj.entrenador.nombre} {obj.entrenador.apellido}" if obj.entrenador else None

    def get_grupo_crecimiento(self, obj):
        return grupo_crecimiento(obj)

    def get_progreso(self, obj):
        if obj.nivel >= NIVEL_MAX:
            return {"porcentaje": 100, "xp_nivel_actual": obj.experiencia, "xp_siguiente_nivel": None}
        grupo = grupo_crecimiento(obj)
        base = xp_para_nivel(grupo, obj.nivel)
        meta = xp_para_nivel(grupo, obj.nivel + 1)
        pct = round((obj.experiencia - base) / (meta - base) * 100, 1) if meta > base else 100
        return {"porcentaje": pct, "xp_nivel_actual": base, "xp_siguiente_nivel": meta}

    def get_proxima_evolucion(self, obj):
        evos = evoluciones_posibles(obj)
        return evos[0] if evos else None