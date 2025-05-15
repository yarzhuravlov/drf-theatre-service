from rest_framework import routers

from reservations import views

router = routers.DefaultRouter()
router.register("", views.ReservationViewSet)

urlpatterns = router.urls

app_name = "reservations"
