from rest_framework import serializers

from reviews.models import User

FORBIDDEN_NAME = 'me'
FORBIDDEN_NAME_MSG = 'Имя пользователя "me" не разрешено.'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        if data.get('username') == FORBIDDEN_NAME:
            raise serializers.ValidationError(
                {'username': FORBIDDEN_NAME_MSG})
        return data


class AuthSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data.get('username') == FORBIDDEN_NAME:
            raise serializers.ValidationError(
                {'username': FORBIDDEN_NAME_MSG})
        return data


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)
