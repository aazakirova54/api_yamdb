from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator

TEXT_LIMIT = 15


class Genre(models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='название-ссылка',
        unique=True,
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='название-ссылка',
        unique=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=200,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр',
        related_name='titles',
    )
    description = models.TextField(
        verbose_name='описание',
        max_length=400,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='категория',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    year = models.IntegerField(
        verbose_name='год',
        validators=(year_validator,),
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MaxValueValidator(10, 'Максимальное значение — 10'),
            MinValueValidator(1, 'Минимальное значение — 1')
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        default_related_name = 'reviews'
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_name_review'
            )
        ]

    def __str__(self):
        return self.text[:TEXT_LIMIT]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        max_length=500,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        default_related_name = 'comments'
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:TEXT_LIMIT]
