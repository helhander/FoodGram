# Generated by Django 2.2.19 on 2022-08-24 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20220823_2103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeshoppingcart',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='recipeshoppingcart',
            name='shopping_cart',
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='recipes',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='recipes',
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe', verbose_name='Рецепт'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe', verbose_name='Рецепт'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='RecipeFavorite',
        ),
        migrations.DeleteModel(
            name='RecipeShoppingCart',
        ),
    ]
