from re import search
from rest_framework import mixins, viewsets,status
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
from reportlab.pdfgen import canvas
from django.db.models import Sum
import django_filters

from core.enums import BynaryFilterValues

from .serializers import RecipeSimpleSerializer
from recipes.models import Recipe


class ListRetrieveNoPagViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    pagination_class = None

def get_shopping_cart_file(self, request):
    """Качаем список с ингредиентами."""
    buffer = io.BytesIO()   
    page = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('AlternaNr',
                        'backend/foodgram/core/fonts/AlternaNr.ttf'))
    page.setFont('AlternaNr', 14)
    x_position, y_position = 50, 800
    shopping_cart = (
        request.user.shopping_cart.all().
        values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit'
        ).annotate(amount=Sum('recipe__recipe_ingredients__amount')).order_by())

    if shopping_cart:
        indent = 20
        page.drawString(x_position, y_position, 'Cписок покупок:')
        for index, recipe in enumerate(shopping_cart, start=1):
            page.drawString(
                x_position, y_position - indent,
                f'{index}. {recipe["recipe__ingredients__name"]} - '
                f'{recipe["amount"]} '
                f'{recipe["recipe__ingredients__measurement_unit"]}.')
            y_position -= 15
            if y_position <= 50:
                page.showPage()
                y_position = 800
    else:
        page.drawString(
        x_position,
        y_position,
        'В списке покупок ничего нет =(')

    page.save()
    buffer.seek(0)
    return buffer

def get_recipe_action_response(self, request, pk, model):
    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user        
    model_item = model.objects.get_or_create(user=user,recipe=recipe)
    if request.method=='DELETE':
        model_item[0].delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = RecipeSimpleSerializer(recipe)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK,
                    headers=headers)

class RecipeFilter(django_filters.FilterSet):
    is_favorited = django_filters.NumberFilter(method='get_is_favorited')
    is_subscribed = django_filters.NumberFilter(method='get_is_subscribed')
    tags = django_filters.CharFilter(method='get_tags')
    author = django_filters.NumberFilter()

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_subscribed', 'tags', 'author']              

    def get_is_favorited(self, queryset, name, value):        
        user = self.request.user
        if user.is_anonymous:
            return queryset.none()
        recipe_ids = user.favorites.values_list('recipe__id', flat=True)
        if value==BynaryFilterValues.select.value:
            return queryset.filter(id__in=recipe_ids)
        elif value==BynaryFilterValues.exclude.value:
            return queryset.exclude(id__in=recipe_ids)        

        raise ValueError(f'{value} is not a valid filter value')

    def get_is_subscribed(self, queryset, name, value):
        user = self.request.user
        if user.is_anonymous:
            return queryset.none()
        subscribing = user.subscribing.values('author')
        if value==BynaryFilterValues.select.value:
            return queryset.filter(author__in=subscribing)
        elif value==BynaryFilterValues.exclude.value:
            return queryset.exclude(author__in=subscribing)

        raise ValueError(f'{value} is not a valid filter value')

    def get_tags(self, queryset, name, value):
        tags = self.request.query_params.getlist('tags')
        return queryset.filter(tags__slug__in=tags)

class IngredientSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_value = request.query_params.get('search')
        return queryset.filter(name__iregex=rf'^{search_value}')