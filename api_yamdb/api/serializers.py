from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Comment, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        request = self.context['request']
        author = request.user
        if request.method == 'POST':
            if Review.objects.filter(author, title).exists():
                raise serializers.ValidationError(
                    'Можно оставить только один отзыв на произведение')
        return data

    def validate_score(self, data):
        if not 1 <= self.context['request'].score <= 10:
            raise serializers.ValidationError(
                'Значение должно быть от 1 до 10')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
