from rest_framework import serializers
from .models import Material


class MaterlailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

