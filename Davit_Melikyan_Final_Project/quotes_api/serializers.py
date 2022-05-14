from rest_framework.serializers import ModelSerializer

from quotes.models import Quotes


#Serializer-@ mer infon dardznum e json
class QuoteSerializer(ModelSerializer):
    class Meta:
        model = Quotes
        fields = ['id', 'quote', 'created_at']

