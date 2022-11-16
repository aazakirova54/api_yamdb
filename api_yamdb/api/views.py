from rest_framework.viewsets import ModelViewSet

from reviews.models import Title
from .serializers import TitleSerializer


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = pass
