from django_filters import rest_framework as filters

from theatre.models import Performance


class PerformanceFilter(filters.FilterSet):
    play__title = filters.CharFilter(lookup_expr="icontains")
    show_time__gt = filters.DateTimeFilter(
        field_name="show_time",
        lookup_expr="gt",
    )
    show_time__lt = filters.DateTimeFilter(
        field_name="show_time",
        lookup_expr="lt",
    )
    show_time_date = filters.DateFilter(
        field_name="show_time",
        lookup_expr="date",
    )
    actors = filters.BaseInFilter(
        field_name="play__actors__id",
        lookup_expr="in",
    )
    genres = filters.BaseInFilter(
        field_name="play__genres__name",
        lookup_expr="in",
    )

    class Meta:
        model = Performance
        fields = ["play"]
