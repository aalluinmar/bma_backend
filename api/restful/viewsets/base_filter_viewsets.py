
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from api.restful.viewsets.pagination import CustomPagination


class BaseFilterViewSet(viewsets.ModelViewSet):
    """
    Base viewset with common filter configurations.
    """
    pagination_class = CustomPagination  # Enable pagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = "__all__"  # Allow filtering by all model fields
    search_fields = "__all__"  # Allow searching by all model fields
    ordering_fields = "__all__"  # Allow ordering by all model fields
