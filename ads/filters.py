
import  django_filters
from .models import Ad
from django_filters import DateFilter

class AdFilter(django_filters.FilterSet):
    class Meta:
        model = Ad
        fields = ['category']
        