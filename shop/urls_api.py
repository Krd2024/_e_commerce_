from django.urls import path

from .views_api import (
    OrderCreateView,
    OrderDetailView,
    OrderItems,
    ProductDetailUpdate,
    ProductListCreateView,
)


urlpatterns = [
    path("products/", ProductListCreateView.as_view(), name="products-list"),
    path(
        "products/<int:product_id>/",
        ProductDetailUpdate.as_view(),
        name="products-detail",
    ),
    path(
        "orders/",
        OrderCreateView.as_view(),
        name="create_order",
    ),
    path(
        "orders_all/",
        OrderItems.as_view(),
        name="OrderItems",
    ),
    path(
        "orders/<id>/",
        OrderDetailView.as_view(),
        name="OrderItems",
    ),
    # path("register/", UserRegistration.as_view(), name="user-register"),
    # path("delete/<int:user_id>/", UserDelete.as_view(), name="user-delete"),
    # path("delete-all/", UserDeleteAll.as_view(), name="user-delete-all"),
    # path("user/<int:user_id>/update/", UserUpdate.as_view(), name="user-update"),
]
