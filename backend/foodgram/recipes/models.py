from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField('Название', max_length=200, unique=True)
    image = models.URLField('Ссылка на изображение блюда')
    text = models.TextField('Описание')
    cooking_time_min = models.PositiveIntegerField(
        'Время приготовления в минутах'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        related_name='recipe_ingredients',
        verbose_name='Ингредиент',
    )
    tags = models.ManyToManyField(
        'Tag',
        through='RecipeTag',
        related_name='recipe_tags',
        verbose_name='Тег',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.text


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                name='unique_name_measurement_unit',
                fields=('name', 'measurement_unit'),
            ),
        ]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', related_name='recipe_ingredients',on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField('Количество')

    class Meta:
        verbose_name = 'Рецепт-Ингредиент'
        verbose_name_plural = 'Рецепты-Ингредиенты'

    def __str__(self):
        return f'{self.recipe}-{self.ingredient}'


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField('Цвет в HEX', max_length=7, unique=True)
    slug = models.SlugField(
        'Слаг id', max_length=200, unique=True
    )

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name, instance=self)
    #     super().save(*args, **kwargs)


class RecipeTag(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Рецепт-Тег'
        verbose_name_plural = 'Рецепты-Теги'

    def __str__(self):
        return f'{self.recipe}-{self.tag}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
