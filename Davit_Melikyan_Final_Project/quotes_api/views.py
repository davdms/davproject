from rest_framework import viewsets
from .serializers import QuoteSerializer
from quotes.models import Quotes
from rest_framework import permissions


class QuotesListViewset(viewsets.ModelViewSet):
    queryset = Quotes.objects.all()
    serializer_class = QuoteSerializer
    #ete uzum enq partadir login exac lini
    permission_classes = [permissions.IsAuthenticated]
    # ete uzum enq login exac lini kam uxxaki diti
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
