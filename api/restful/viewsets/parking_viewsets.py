from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from api.models import ParkingDetails
from api.restful.serializers import ParkingDetailsSerializer
from api.restful.viewsets.base_filter_viewsets import BaseFilterViewSet
from bma_backend.permissions import ParkingPermissions
from api.filters import ParkingDetailsFilter


class ParkingDetailsViewSet(BaseFilterViewSet):
    """
    CRUD Operations for listing/creating/updating parking details.
    """
    queryset = ParkingDetails.objects.all().order_by('parking_number')
    serializer_class = ParkingDetailsSerializer
    permission_classes = [ParkingPermissions]
    http_method_names = ["get", "post", "put", "patch"]
    filterset_class = ParkingDetailsFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        
        if isinstance(request.data, list):
            instances = ParkingDetails.objects.bulk_create([ParkingDetails(**item) for item in serializer.validated_data])
            serializer = self.get_serializer(instances, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
