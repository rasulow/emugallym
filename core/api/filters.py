import django_filters
from core.models import Course

class CourseFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='in')
    user = django_filters.CharFilter(field_name='user__id', lookup_expr='in')
    paid = django_filters.BooleanFilter(field_name='paid')

    class Meta:
        model = Course
        fields = ['category', 'paid', 'user']