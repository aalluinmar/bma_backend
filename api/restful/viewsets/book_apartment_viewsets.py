
from rest_framework import viewsets

from api.models import LeaseDetails
from api.restful.serializers import BookApartmentSerializer
from api.restful.viewsets.pagination import CustomPagination
from api.restful.viewsets.base_filter_viewsets import BaseFilterViewSet
from bma_backend.permissions import ActiveUserPermissions


class BookApartmentViewSet(BaseFilterViewSet):
    """
    Booking an apartment for a tenant. This will create a lease for the tenant.
    """
    queryset = LeaseDetails.objects.all().order_by("start_date")
    serializer_class = BookApartmentSerializer
    permission_classes = [ActiveUserPermissions]
    http_method_names = ["post"]
