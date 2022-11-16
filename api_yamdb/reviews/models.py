from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

TEXT_LIMIT = 15


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
        auto_now_add=True
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
    pass
