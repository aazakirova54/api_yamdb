from rest_framework.viewsets import ModelViewSet

from reviews.models import Title, Category, Genre
from .serializers import (TitleSerializer,
                          TitleReadSerializer,
                          CategorySerializer,
                          GenreSerializer,
                         )


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = ()

    def get_serializer_class(self):
        if self.action in ('list', 'retrive'):
            return TitleReadSerializer
        return TitleSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = ()


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = ()
