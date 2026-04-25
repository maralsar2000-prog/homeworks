from django.views import View
from django.http import HttpResponse


# ===== ООП: класс товара =====
class Product:
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description


# ===== ООП: страница =====
class ProductPage(View):

    def get(self, request):

        # ===== данные прямо в коде =====
        products = [
            Product("iPhone 14", 450000, "Apple смартфон с хорошей камерой"),
            Product("Samsung Galaxy S23", 400000, "Android флагман"),
            Product("Наушники JBL", 25000, "Беспроводные наушники"),
        ]

        # ===== HTML генерация =====
        html = """
        <html>
        <head>
            <title>Товары</title>
        </head>
        <body>
            <h1>Список товаров</h1>
        """

        for p in products:
            html += f"""
            <div style="border:1px solid #ccc; padding:10px; margin:10px;">
                <h2>{p.name}</h2>
                <p>Цена: {p.price} ₸</p>
                <p>{p.description}</p>
            </div>
            """

        html += """
        </body>
        </html>
        """

        return HttpResponse(html)


from django.urls import path
from .views import ProductPage

urlpatterns = [
    path('products/', ProductPage.as_view(), name='products'),
]

