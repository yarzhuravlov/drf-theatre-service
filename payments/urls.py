from django.urls import path

from payments import views

urlpatterns = [
    path(
        "session/<int:reservation_id>/",
        views.CreateCheckoutSessionView.as_view(),
        name="create-session",
    ),
    path(
        "stripe/webhook",
        views.StripeWebhookView.as_view(),
        name="stripe-webhook",
    ),
]

app_name = "payments"
