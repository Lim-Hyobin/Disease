from .models import SwiperContent
from rest_framework import serializers

class SwiperContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwiperContent
        fields = '__all__'