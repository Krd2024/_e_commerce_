from django.shortcuts import redirect, render
from django.http import JsonResponse

# from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from shop.process_db.processor_db import (
    create_cart_item,
    get_category,
    get_products_in_category,
    create_order_from_cart,
    get_orders,
    delete_product_in_bascket,
    get_bascet,
    delete_product_in_bascket_all,
)
import json
import time


def index_views(request):
    """Показать категории"""

    contex_to_html = get_category(request)
    return contex_to_html


def product_in_category(request, category_name):
    """Показать товары в категории"""

    products = get_products_in_category(category_name)

    return render(
        request,
        "product_in_category.html",
        {"products": products},
    )


# @csrf_exempt  # Отключаем проверку CSRF
def add_to_bascet(request):
    """Добавить товар в корзину"""

    if not request.user.is_authenticated:
        return JsonResponse({"status": 0})

    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("productId")
        quantity = data.get("quantity")

        print(product_id, quantity)

        if product_id is None or quantity == 0:
            return JsonResponse({"status": "error", "message": "Что-то пошло не так"})

        # Добавление в корзину
        res = create_cart_item(product_id, quantity, request.user)

        if res == 0:
            return JsonResponse({"status": "error", "message": "Что-то пошло не так"})

        return JsonResponse(
            {"status": "success", "productId": product_id, "quantity": quantity}
        )

    # Если метод запроса не POST, возвращаем ошибку
    return JsonResponse(
        {"status": "error", "message": "Метод запроса должен быть POST"}
    )


def bascket(request):
    """Посмотреть корзину"""

    try:
        bascket = get_bascet(request)
        return render(request, "bascket.html", {"bascket": bascket})

    except Exception as e:
        print(e)
        return redirect("/")


def checkout_view(request):
    """Оформить заказ = покупка"""

    user = request.user
    order = create_order_from_cart(user)

    if order:
        messages.success(request, "Ваш заказ был успешно оформлен!")
    else:
        messages.error(request, "Произошла ошибка при оформлении заказа.")
    return redirect("/")


def order(request):
    """Посмотреть заказы"""

    user = request.user
    orders = get_orders(user)
    # total_price = order.get_order_items().aggregate(
    #     total_price=models.Sum("total_price")
    # )["total_price"]
    # print(f"Total Price: {total_price}")
    return render(request, "order.html", {"orders": orders})


def delete_product(request, product_id):
    """Удалить товар из корзины"""

    user = request.user
    action = delete_product_in_bascket(user, product_id)

    if action:
        messages.success(request, "Товар удалён")
        return redirect("bascet")

    messages.success(request, "Что-то пошло не так")
    return redirect("bascet")


def delete_cart(request):
    """Удалить всё из корзины"""

    user = request.user
    delete_product_in_bascket_all(user)
    return redirect("bascet")


def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = "{:02d}:{:02d}".format(mins, secs)
        print(timeformat, end="\r")  # Перезапись строки
        time.sleep(1)
        seconds -= 1

    print("00:00")  # Отображение 00:00 по завершении


# countdown_timer(10)  # Таймер на 10 секунд
