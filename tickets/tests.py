from django.test import SimpleTestCase, TestCase
from .models import Area
from .estructuras.red import red_de_areas
from .estructuras.arbol_bst import (
    construir_balanceado,
    a_lista,
    altura,
    contar_pasos,
)

from django.contrib.auth.models import User
from tickets.estructuras.cola_prioridad import MinHeap, primeros
from tickets.estructuras.ranking import heap_sort


class ArbolBalanceadoTest(SimpleTestCase):
    def setUp(self):
        self.datos = []
        for i in range(1, 101):
            self.datos.append((i, "Ticket " + str(i)))
        self.raiz = construir_balanceado(self.datos)

    def test_altura_balanceada(self):
        self.assertLessEqual(altura(self.raiz), 7)

    def test_inorden_sale_ordenado(self):
        salida = []
        a_lista(self.raiz, salida)
        self.assertEqual(salida, self.datos)

    def test_lista_vacia(self):
        self.assertIsNone(construir_balanceado([]))


class ListaTicketsTest(TestCase):
    def test_pide_iniciar_sesion(self):
        respuesta = self.client.get("/tickets/todos/")
        self.assertEqual(respuesta.status_code, 302)


class BusquedaTest(SimpleTestCase):
    def test_busqueda_rapida(self):
        datos = [(i, "Ticket " + str(i)) for i in range(1, 101)]
        raiz = construir_balanceado(datos)
        pasos = contar_pasos(raiz, 100)
        self.assertLessEqual(pasos, 7)


class RedAreasTest(TestCase):
    def test_red_es_dirigida(self):
        mesa = Area.objects.create(nombre="Mesa de ayuda")
        redes = Area.objects.create(nombre="Redes")
        mesa.deriva_a.add(redes)
        red = red_de_areas(Area.objects.order_by("nombre"))
        self.assertEqual(red.vecinos("Mesa de ayuda"), ["Redes"])
        self.assertEqual(red.vecinos("Redes"), [])

    def test_area_sin_derivaciones(self):
        seguridad = Area.objects.create(nombre="Seguridad")
        red = red_de_areas(Area.objects.order_by("nombre"))
        self.assertEqual(red.grado("Seguridad"), 0)
        self.assertEqual(red.grado_entrada("Seguridad"), 0)


class ColaUrgentesTest(TestCase):
    def test_extrae_primero_el_mas_urgente(self):
        cola = MinHeap()
        cola.insertar((-3, 1, "normal"))
        cola.insertar((-9, 2, "urgente"))
        cola.insertar((-5, 3, "media"))
        self.assertEqual(primeros(cola, 1)[0]["titulo"], "urgente")

    def test_empate_sale_el_mas_antiguo(self):
        cola = MinHeap()
        cola.insertar((-5, 8, "nuevo"))
        cola.insertar((-5, 2, "antiguo"))
        self.assertEqual(primeros(cola, 1)[0]["id"], 2)

    def test_orden_completo(self):
        cola = MinHeap()
        for i, p in enumerate([4, 9, 1, 7, 9, 2], start=1):
            cola.insertar((-p, i, f"ticket {i}"))
        prioridades = [t["prioridad"] for t in primeros(cola, 10)]
        self.assertEqual(prioridades, sorted(prioridades, reverse=True))


class UrgentesAPITest(TestCase):
    def test_sin_sesion_da_403(self):
        respuesta = self.client.get("/api/tickets/urgentes/")
        self.assertEqual(respuesta.status_code, 403)

    def test_con_sesion_da_200(self):
        User.objects.create_user("agente_test", password="clave12345")
        self.client.login(username="agente_test", password="clave12345")
        respuesta = self.client.get("/api/tickets/urgentes/?n=3")
        self.assertEqual(respuesta.status_code, 200)

class RankingTest(TestCase):
    def test_heap_sort_coincide_con_sorted(self):
        datos = [(3, "ana"), (7, "beto"), (3, "luis"), (1, "carla"), (7, "zoe")]
        self.assertEqual(heap_sort(datos), sorted(datos, reverse=True))

    def test_tablero_pide_login(self):
        respuesta = self.client.get("/tablero/")
        self.assertEqual(respuesta.status_code, 302)