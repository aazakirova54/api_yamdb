from rest_framework.viewsets import ModelViewSet
from reviews.models import Title, Category, Genre, Comment, Review, Title
from .serializers import (TitleSerializer,
                          TitleReadSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          CommentSerializer,
                          ReviewSerializer,
                          )
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api_yamdb.settings import EMAIL_ADMIN
from reviews.models import User

from .permissions import (IsAdminOrStaff, IsUser)
from .serializers import (AuthSignUpSerializer, AuthTokenSerializer,
                          UserSerializer)


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


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ()

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = ()

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrStaff,)
    search_fields = ('=username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(IsUser,)
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    username = request.data.get('username')

    if not User.objects.filter(username=username).exists():
        serializer = AuthSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['username'] != 'me':
            serializer.save()
            send_confirmation_code(username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            'Username указан неверно!', status=status.HTTP_400_BAD_REQUEST
        )
    user = get_object_or_404(User, username=username)
    serializer = AuthSignUpSerializer(
        user, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data['email'] == user.email:
        serializer.save()
        send_confirmation_code(username)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        'Почта указана неверно!', status=status.HTTP_400_BAD_REQUEST
    )


def send_confirmation_code(username):
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    send_mail(
        'Код регистрации',
        f'Код для получения токена {user.confirmation_code}',
        EMAIL_ADMIN,
        [user.email],
        fail_silently=False,
    )
    user.save()


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            'Пользователь не найден', status=status.HTTP_404_NOT_FOUND
        )
    if user.confirmation_code == confirmation_code:
        refresh = RefreshToken.for_user(user)
        token_data = {'token': str(refresh.access_token)}
        return Response(token_data, status=status.HTTP_200_OK)
    return Response(
        'Неверный код подтверждения', status=status.HTTP_400_BAD_REQUEST
    )
