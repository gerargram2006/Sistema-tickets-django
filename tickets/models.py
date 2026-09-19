from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre


class Ticket(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, default="Abierto")
    agente_asignado = models.ForeignKey(
        Usuario, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"[{self.pk}] {self.titulo} - {self.estado}"
