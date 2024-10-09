from django.core.exceptions import ObjectDoesNotExist
from shop.models import Cart, CartItem, Category, Order, OrderItem, Product
from django.shortcuts import render, get_object_or_404


# def index_process(request):
#     test = Product.objects.all()
#     res = render(request, "index.html", {"test": test})
#     return res


def get_category(request):
    """Показать все категории"""

    category_obj = Category.objects.all()
    contex = render(request, "index.html", {"category": category_obj})
    return contex


def get_products_in_category(category_name):
    category = get_object_or_404(Category, name=category_name)
    # product.quantity_bascket = product.stock_quantity

    return Product.objects.filter(category=category)


def get_bascet(request):

    cart_obj = Cart.objects.prefetch_related("items").get(user=request.user)
    return cart_obj


def create_cart_item(product_id, quantity, user):
    """Создать корзину + добавить товар"""

    try:
        cart, created = Cart.objects.get_or_create(user=user)

        product = Product.objects.get(id=product_id)
        try:
            product.stock_quantity -= quantity
            product.save()

            cart_item = CartItem.objects.get(cart=cart, product=product)
            #  обновить кол-во товара в корзине
            cart_item.quantity += quantity
            cart_item.save()

            print("добавили товар в карзину")

        except ObjectDoesNotExist:
            # Если нет такого товара в корзине , создать
            cart_item = CartItem.objects.create(
                cart=cart, product=product, quantity=quantity, price=product.price
            )
        except Exception as e:
            print(e)

    except Exception as e:
        print(e)
        status = 0
        return status


def create_order_from_cart(user):
    """Создать заказ = купить"""

    try:
        # Получить корзину с товарами пользователя
        cart_obj = Cart.objects.prefetch_related("items").get(user=user)

        total_amount = sum(cart_item.total_price for cart_item in cart_obj.items.all())
        if total_amount == 0:
            return

        order = Order.objects.create(user=user, total_price=total_amount)

        for cart_item in cart_obj.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.price,
            )

        # Очищаем корзину после создания заказа
        cart_obj.items.all().delete()

        return order
    except Exception as e:
        print(e)
        return None


def get_orders(user):
    """Получить все заказы пользователя"""

    orders = Order.objects.filter(user=user)
    return orders


def delete_product_in_bascket(user, product_id, all=False):
    """Удалить товар из корзины по id"""

    print(user, product_id)
    cart = get_object_or_404(Cart, user=user)
    try:
        product_del = get_object_or_404(
            CartItem, cart=cart, product=(Product.objects.get(id=product_id))
        )
        print(product_del.quantity, "<<< -----на удаление ")

        product = Product.objects.get(id=product_id)
        product.stock_quantity += product_del.quantity

        product.save()
        product_del.delete()
        return True
    except Exception as e:
        print(e)


def delete_product_in_bascket_all(user):
    """Удалить содержимое корзины"""

    try:
        cart_obj = Cart.objects.prefetch_related("items").get(user=user)
        all_product = cart_obj.items.all()
        for product in all_product:
            add_quantity = Product.objects.get(pk=product.product.id)
            add_quantity.stock_quantity += product.quantity
            add_quantity.save()
        cart_obj.delete()
    except Exception as e:
        print(e)
    # print(product.quantity)
    # print(product.product.id)
    # print(product.product.name)
    # print(product.quantity)
