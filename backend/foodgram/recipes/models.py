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

    class Meta:
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
    color = models.CharField('Цвет в HEX', max_length=7, blank=True, null=True)
    slug = models.SlugField(
        'Слаг id', max_length=200, blank=True, null=True, unique=True
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
    recipe = models.ManyToManyField(
        'Recipe',
        through='RecipeFavorite',
        verbose_name='Избранное',
    )


class RecipeFavorite(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    favorite = models.ForeignKey('Favorite', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Рецепт-Избранное'
        verbose_name_plural = 'Рецепты-Избранное'

    def __str__(self):
        return f'{self.recipe}-{self.favorite}'


class ShopingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoping_cart',
        verbose_name='Пользователь',
    )
    recipes = models.ManyToManyField(
        'Recipe',
        through='RecipeShopingCart',
        verbose_name='Избранное',
    )


class RecipeShopingCart(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    shoping_cart = models.ForeignKey('ShopingCart', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Рецепт-Список покупок'
        verbose_name_plural = 'Рецепты-Список покупок'

    def __str__(self):
        return f'{self.recipe}-{self.shoping_cart}'
