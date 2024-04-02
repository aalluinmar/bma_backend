from api.models import BuildingDetails
from api.filters import BuildingDetailsFilter
from api.restful.serializers import BuildingDetailsSerializer
from api.restful.viewsets.base_filter_viewsets import BaseFilterViewSet

from bma_backend.permissions import IsAdminPermissions


class BuildingDetailsViewSet(BaseFilterViewSet):
    """
    CRUD Operations for listing/creating/updating building details.
    """
    queryset = BuildingDetails.objects.all().order_by("building_number")
    serializer_class = BuildingDetailsSerializer
    permission_classes = [IsAdminPermissions]
    http_method_names = ["get", "post", "put", "patch"]
    filterset_class = BuildingDetailsFilter
