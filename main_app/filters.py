import django_filters
from .models import Projects

class statusFilter(django_filters.FilterSet):
    class Meta:
        model = Projects
        fields = ['status']
