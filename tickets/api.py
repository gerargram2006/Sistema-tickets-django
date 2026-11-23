from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Ticket
from .estructuras.cola_prioridad import cola_urgentes, primeros


class UrgentesAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        n = int(request.GET.get("n", 5))
        abiertos = Ticket.objects.filter(estado__iexact="Abierto")
        cola = cola_urgentes(abiertos)
        return Response(primeros(cola, n))