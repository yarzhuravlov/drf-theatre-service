from rest_framework import routers

from theatre import views

router = routers.DefaultRouter()
router.register("plays", views.PlayViewSet)
router.register("performances", views.PerformanceViewSet)
router.register("actors", views.ActorViewSet)
router.register("genres", views.GenreViewSet)

urlpatterns = router.urls

app_name = "theatre"
