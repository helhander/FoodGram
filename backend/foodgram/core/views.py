from rest_framework import mixins, viewsets
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.db.models import Sum

class ListRetrieveViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    pass

def get_shopping_cart_file(self, request):
    """Качаем список с ингредиентами."""
    buffer = io.BytesIO()
    page = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('FreeSans',
                            'recipes/fonts/FreeSans.ttf'))
    x_position, y_position = 50, 800
    shopping_cart = (
        request.user.shopping_cart.get().recipes.
        values(
            'ingredients__name',
            'ingredients__measurement_unit'
        ).annotate(amount=Sum('recipe_ingredients__amount')).order_by())
    page.setFont('FreeSans', 14)
    if shopping_cart:
        indent = 20
        page.drawString(x_position, y_position, 'Cписок покупок:')
        for index, recipe in enumerate(shopping_cart, start=1):
            page.drawString(
                x_position, y_position - indent,
                f'{index}. {recipe["ingredients__name"]} - '
                f'{recipe["amount"]} '
                f'{recipe["ingredients__measurement_unit"]}.')
            y_position -= 15
            if y_position <= 50:
                page.showPage()
                y_position = 800
        page.save()
        buffer.seek(0)
        return buffer
    page.setFont('FreeSans', 24)
    page.drawString(
        x_position,
        y_position,
        'Cписок покупок пуст!')
    page.save()
    buffer.seek(0)
    return buffer