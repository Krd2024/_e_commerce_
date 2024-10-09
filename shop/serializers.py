from .models import Order, OrderItem, Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "stock_quantity", "category"]


class ProductUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "price", "description", "stock_quantity"]


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price", "total_price"]

    def create(self, validated_data):
        item = OrderItem.objects.create(**validated_data)
        return item


class OrderCreateSerializer(serializers.ModelSerializer):
    """Создать заказ"""

    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["user", "order_items", "status", "total_price"]

    def create(self, validated_data):
        order_items_data = validated_data.pop(
            "order_items"
        )  # Извлекаем данные позиций заказа

        order = Order.objects.create(**validated_data)
        # total = 0
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        #     total += item.total_price  # Суммируем стоимость каждой позиции
        # order.total_price = total  # Обновляем общую стоимость заказа
        order.save()
        return order
