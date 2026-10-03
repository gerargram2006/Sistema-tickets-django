import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from tickets.models import Articulo
from tickets.views import buscar_articulo


if __name__ == "__main__":
    print("--- ARTÍCULOS EN LA BASE DE DATOS ---")
    for a in Articulo.objects.all().order_by('titulo'):
        print(a.titulo)

    print(f"\nTotal de artículos: {Articulo.objects.count()}")

    titulo_buscar = "Estados de un ticket explicados"

    print("\n--- BÚSQUEDA BINARIA MANUAL ---")
    resultado, comparaciones = buscar_articulo(titulo_buscar)
    print(f"Buscando: '{titulo_buscar}'")
    print(f"Resultado: {resultado}")
    print(f"Comparaciones realizadas: {comparaciones}")

    print("\n--- BÚSQUEDA CON Articulo.objects.filter() ---")
    resultado_orm = Articulo.objects.filter(titulo=titulo_buscar)
    print(f"Resultado ORM: {list(resultado_orm)}")
