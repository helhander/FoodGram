from django.contrib.auth import get_user_model
from django.db import models

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

    def __str__(self):
        return self.text


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_name_measurement_unit',
                fields=('name', 'measurement_unit'),
            ),
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe', related_name='recipe_ingredients', on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField('Количество')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_recipe_ingredient',
                fields=('recipe', 'ingredient'),
            ),
        ]

    def __str__(self):
        return f'{self.recipe}-{self.ingredient}'


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField('Цвет в HEX', max_length=7, unique=True)
    slug = models.SlugField('Слаг id', max_length=200, unique=True)

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_recipe_tag',
                fields=('recipe', 'tag'),
            ),
        ]

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
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_favorite_recipe_user',
                fields=('recipe', 'user'),
            ),
        ]


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
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_shoppingcart_recipe_user',
                fields=('recipe', 'user'),
            ),
        ]
