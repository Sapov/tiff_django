from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import MaterlailSerializer, FinishWorkSerializer
from .models import Material, FinishWork


class FilesViewSet(ReadOnlyModelViewSet):
    serializer_class = MaterlailSerializer
    queryset = Material.objects.all()


class FinishWorkViewSet(ReadOnlyModelViewSet):
    serializer_class = FinishWorkSerializer
    queryset = FinishWork.objects.all()