import django_filters
from .models import *


class courseFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all())

    class Meta:
        model = Course
        fields = ('category',)
