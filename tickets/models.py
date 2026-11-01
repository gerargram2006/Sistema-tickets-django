from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from .estructuras.arbol_expresion import construir_postfija, evaluar_con_variables


FORMULA_PRIORIDAD = "impacto peso * dias +"


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=60)
    peso = models.PositiveIntegerField(default=1)
    padre = models.ForeignKey(
        "self", null=True, blank=True,
        on_delete=models.CASCADE, related_name="subcategorias"
    )

    def __str__(self):
        return self.nombre

class Ticket(models.Model):
    ESTADOS = (
        ("abierto", "Abierto"),
        ("en_progreso", "En progreso"),
        ("completado", "Completado"),
    )

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="abierto")
    impacto = models.PositiveSmallIntegerField(
        choices=((1, "Muy bajo"), (2, "Bajo"), (3, "Medio"), (4, "Alto"), (5, "Crítico")),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    creado = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tickets",
    )
    agente_asignado = models.ForeignKey(
        Usuario, null=True, blank=True, on_delete=models.SET_NULL
    )
    categoria = models.ForeignKey(
        Categoria, null=True, blank=True, on_delete=models.SET_NULL
    )

    @property
    def propietario(self):
        return self.creado_por

    @propietario.setter
    def propietario(self, value):
        self.creado_por = value

    def prioridad(self):
        valores = {
            "impacto": self.impacto,
            "peso": self.categoria.peso if self.categoria else 1,
            "dias": (timezone.now() - self.creado).days,
        }
        arbol = construir_postfija(FORMULA_PRIORIDAD)
        return evaluar_con_variables(arbol, valores)

    def __str__(self):
        return f"[{self.pk}] {self.titulo} - {self.estado}"

class Articulo(models.Model):
    titulo = models.CharField(max_length=150, unique=True)
    contenido = models.TextField()

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="comentarios"
    )
    texto = models.TextField()
    autor = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor} en [{self.ticket_id}]"
