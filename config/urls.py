from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

api_v1_urlpatterns = [
    path("theatre/", include("theatre.urls", namespace="theatre")),
    path(
        "reservations/", include("reservations.urls", namespace="reservations")
    ),
    path("payments/", include("payments.urls")),
    path("accounts/", include("accounts.urls")),
    # Schema & Docs
    path(
        "schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"
    ),
    path(
        "docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="v1:schema"),
        name="swagger",
    ),
    path(
        "docs/redoc/",
        SpectacularRedocView.as_view(url_name="v1:schema"),
        name="redoc",
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include((api_v1_urlpatterns, "v1"), namespace="v1")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
