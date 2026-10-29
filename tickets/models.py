from django.conf import settings
from django.db import models
from django.utils import timezone


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=60)
    peso = models.PositiveSmallIntegerField(default=1)
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
    impacto = models.PositiveSmallIntegerField(default=3)
    fecha_apertura = models.DateTimeField(default=timezone.now)
    formula_postfija = models.CharField(max_length=100, blank=True)
    propietario = models.ForeignKey(
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
    def dias_abierto(self):
        diferencia = timezone.now() - self.fecha_apertura
        return max(0, diferencia.days)

    @property
    def es_urgente(self):
        return self.estado == "abierto" and self.impacto >= 4

    def actualizar_prioridad(self):
        from .arbol_expresion import calcular_prioridad
        peso = self.categoria.peso if self.categoria else 1
        _, formula = calcular_prioridad(self.impacto, peso, self.dias_abierto)
        self.formula_postfija = formula

    def save(self, *args, **kwargs):
        self.actualizar_prioridad()
        super().save(*args, **kwargs)

    def prioridad(self):
        from .arbol_expresion import calcular_prioridad
        peso = self.categoria.peso if self.categoria else 1
        prioridad, _ = calcular_prioridad(self.impacto, peso, self.dias_abierto)
        return prioridad

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
