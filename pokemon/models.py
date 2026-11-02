from django.db import models

class pokemon(models.Model):
    nombre = models.CharField(max_length=30)
    peso = models.FloatField()
    imagen =models.URLField(blank=True)
    entrenador = models.ForeignKey('entrenador', on_delete=models.SET_NULL, null=True, blank=True, related_name="pokemones")
    habilidades = models.TextField()
    naturaleza = models.CharField(max_length=50)
    elemento = models.CharField(max_length=50)
    descripcion =models.TextField()

     
    def __str__(self):
        return f'{self.nombre}-{self.peso}- {self.imagen}-{self.entrenador}-{self.naturaleza}-{self.habilidades}{self.elemento}-{self.descripcion}'
class Gimnasio(models.Model):
    lider = models.CharField(max_length=50)
    elemento = models.CharField(max_length=50)
    medallas = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.lider} - {self.elemento} -{self.medallas}'

class entrenador (models.Model):
    id_documento = models.CharField(max_length=40)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    medallas = models.ManyToManyField(Gimnasio, blank=True)

    def __str__(self):
        return f'{self.id_documento}-{self.nombre}-{self.apellido}-{self.medallas}'

  