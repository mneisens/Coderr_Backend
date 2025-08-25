import django_filters
from ..models import Offer


class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(field_name='user', lookup_expr='exact')
    min_price = django_filters.NumberFilter(method='filter_min_price')
    max_delivery_time = django_filters.NumberFilter(method='filter_max_delivery_time')

    class Meta:
        model = Offer
        fields = ['user']

    def filter_min_price(self, queryset, name, value):
        return queryset.filter(details__price__gte=value).distinct()

    def filter_max_delivery_time(self, queryset, name, value):
        return queryset.filter(details__delivery_time_in_days__lte=value).distinct()
