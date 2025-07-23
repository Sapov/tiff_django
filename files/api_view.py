from rest_framework.viewsets import ViewSet, ModelViewSet

from .serializers import MaterlailSerializer
from .models import Material


class FilesViewSet(ModelViewSet):
    serializer_class = MaterlailSerializer
    queryset = Material.objects.all()