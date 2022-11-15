from django.db import models

from .validators import year_validator


class Genre(models.Model):
    pass


class Category(models.Model):
    pass


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

    def __str__(self):
        return self.name
