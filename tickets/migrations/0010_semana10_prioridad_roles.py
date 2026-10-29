import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


def normalizar_estados_y_pesos(apps, schema_editor):
    Ticket = apps.get_model("tickets", "Ticket")
    Categoria = apps.get_model("tickets", "Categoria")

    reemplazos = {
        "Pendiente": "abierto",
        "En progreso": "en_progreso",
        "Completado": "completado",
    }
    for antiguo, nuevo in reemplazos.items():
        Ticket.objects.filter(estado=antiguo).update(estado=nuevo)

    pesos = {
        "Hardware": 3,
        "Software": 3,
        "Red e Internet": 4,
        "Acceso y cuentas": 2,
        "Correo electrónico": 2,
        "Otros": 1,
    }
    for nombre, peso in pesos.items():
        Categoria.objects.filter(nombre=nombre).update(peso=peso)


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0009_categoria_padre_alter_categoria_nombre"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="categoria",
            name="peso",
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="ticket",
            name="impacto",
            field=models.PositiveSmallIntegerField(default=3),
        ),
        migrations.AddField(
            model_name="ticket",
            name="fecha_apertura",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="ticket",
            name="formula_postfija",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="ticket",
            name="propietario",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="tickets", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="estado",
            field=models.CharField(choices=[("abierto", "Abierto"), ("en_progreso", "En progreso"), ("completado", "Completado")], default="abierto", max_length=20),
        ),
        migrations.RunPython(normalizar_estados_y_pesos, migrations.RunPython.noop),
    ]
