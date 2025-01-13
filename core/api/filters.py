import django_filters
from core.models import Course

class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class CourseFilter(django_filters.FilterSet):
    category = CharInFilter(field_name='category__slug', lookup_expr='in')
    paid = django_filters.BooleanFilter(field_name='paid')
    user = django_filters.NumberFilter(field_name='user__id')

    class Meta:
        model = Course
        fields = ['category', 'paid', 'user']