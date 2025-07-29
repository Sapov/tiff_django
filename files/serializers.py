from rest_framework import serializers
from .models import Material, FinishWork


class MaterlailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['name', 'type_print', 'price_customer_retail', ]

class FinishWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishWork
        fields = ['work', 'price_customer_retail']
