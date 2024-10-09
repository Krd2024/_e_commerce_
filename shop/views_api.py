from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from shop.models import Product, OrderItem
from .serializers import (
    OrderItemSerializer,
    ProductSerializer,
    ProductUpdateSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics
from .models import Order
from .serializers import OrderCreateSerializer


class ProductListCreateView(APIView):
    """
    Получить список товаров
    Создать новый продукт
    """

    @extend_schema(
        summary="Получение списка товаров",
        description="Возвращает список всех товаров.",
        responses={
            200: OpenApiResponse(
                response=ProductSerializer(many=True),
                description="Список всех товаров",
            )
        },
    )
    def get(self, request):
        users = Product.objects.all()
        serializer = ProductSerializer(users, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Добавить товар",
        description="Добавляет товар с ценой,названием,описанием,остатком",
        request=ProductSerializer,
        responses={
            201: OpenApiResponse(
                response=ProductSerializer, description="Товар успешно создан"
            ),
            400: OpenApiResponse(description="Ошибки валидации"),
        },
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(
                {"status": "Product created", "id": product.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from django.views.decorators.csrf import csrf_exempt


class ProductDetailUpdate(APIView):
    """
    Информации о товаре
    Обновление продукта
    """

    @extend_schema(
        summary="Получение информации о товаре",
        description="Возвращает информацию о товаре по его ID.",
        responses={
            200: OpenApiResponse(
                response=ProductSerializer, description="Информация о товаре"
            ),
            404: OpenApiResponse(description="Товар не найден"),
        },
    )
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @extend_schema(
        summary="Обновление продукта",
        description="Обновляет продукта ",
        request=ProductUpdateSerializer,
        responses={
            200: OpenApiResponse(
                response=ProductUpdateSerializer,
                description="Продукт успешно обновлён",
            ),
            400: OpenApiResponse(description="Ошибки валидации"),
        },
    )
    # @csrf_exempt
    def put(self, request, product_id):
        try:
            obj_product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(obj_product, data=request.data)

        if serializer.is_valid():
            product = serializer.save()
            return Response(
                {"status": "Product updated", "id": product.id},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Удаление продукт",
        description="Удаляет продукт по его ID. Если продукт не найден, возвращает ошибку.",
        responses={
            200: OpenApiResponse(description="Продукт успешно удалён"),
            404: OpenApiResponse(description="Продукт не найден"),
            400: OpenApiResponse(description="ID продукта не предоставлен"),
        },
    )
    def delete(self, request, product_id):
        if product_id:
            try:
                user = Product.objects.get(id=product_id)
                user.delete()
                return Response(
                    {"status": "Product deleted"}, status=status.HTTP_200_OK
                )
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {"error": "Product ID not provided"}, status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    summary="Создать заказ (на доработке)",
    description="Создаёт заказ",
    responses={
        201: OpenApiResponse(description="Успех"),
        415: OpenApiResponse(description="Unsupported Media Type"),
        400: OpenApiResponse(description="Запрос неправильно сформирован"),
    },
)
class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer


class OrderItems(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderDetailView(generics.RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    lookup_field = "id"  # Используем 'id' для поиска заказа


# ----------------------------------------------------------------

# class OrderItems(APIView):
#     """Посмотреть все заказы"""

#     @extend_schema(
#         summary="Посмотреть все заказы",
#         description="Посмотреть все заказы",
#         responses={
#             200: OpenApiResponse(
#                 response=OrderItemSerializer, description="Все заказы"
#             ),
#             404: OpenApiResponse(description="Заказы не найдены"),
#         },
#     )
#     def get(self, request):
#         try:
#             orderItem = OrderItem.objects.all()
#         except OrderItem.DoesNotExist:
#             return Response(
#                 {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = OrderItemSerializer(orderItem, many=True)
#         return Response(serializer.data)


# ==================================================================================


# class UserDelete(APIView):


# class UserDeleteAll(APIView):
#     @extend_schema(
#         summary="Удаление всех пользователей",
#         description="Удаляет всех пользователей из базы данных.",
#         responses={
#             200: OpenApiResponse(description="Все пользователи успешно удалены")
#         },
#     )
#     def delete(self, request):
#         User.objects.all().delete()
#         return Response({"status": "All users deleted"}, status=status.HTTP_200_OK)
