from django.db import migrations


def crear_categorias_iniciales(apps, schema_editor):
    Categoria = apps.get_model("tickets", "Categoria")
    nombres = [
        "Hardware",
        "Software",
        "Red e Internet",
        "Acceso y cuentas",
        "Correo electrónico",
        "Otros",
    ]
    for nombre in nombres:
        Categoria.objects.get_or_create(nombre=nombre)


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0006_ticket_categoria"),
    ]

    operations = [
        migrations.RunPython(
            crear_categorias_iniciales,
            migrations.RunPython.noop,
        ),
    ]
