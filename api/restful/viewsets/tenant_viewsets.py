from rest_framework import viewsets

from api.models import Tenant
from api.restful.serializers import TenantSerializer
from api.restful.viewsets.pagination import CustomPagination
from api.restful.viewsets.base_filter_viewsets import BaseFilterViewSet

from bma_backend.permissions import IsAdminPermissions


class TenantViewSet(BaseFilterViewSet):
    """
    CRUD Operations for listing/creating/updating Tenant details.
    """
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAdminPermissions]
    http_method_names = ["get", "patch"]
    pagination_class = CustomPagination  # Enable pagination
