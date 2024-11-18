from django.urls import path
from . import views

urlpatterns = [
    path('create-order/',views.order_create,name='order_create'),
    path('admin/order/<int:order_id>/pdf/',views.admin_order_pdf,name='admin-order-pdf'),
    path("success/", views.SuccessView.as_view(), name="success"),
    path("cancel/", views.CancelView.as_view(), name="cancel"),
    path(
        "create-checkout-session/",
        views.CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("webhooks/stripe/", views.StripeWebhookView.as_view(), name="stripe-webhook"),

]