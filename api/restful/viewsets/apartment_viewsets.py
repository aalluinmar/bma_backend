from rest_framework import status
from rest_framework.response import Response

from api.models import ApartmentDetails
from api.filters import ApartmentDetailsFilter
from api.restful.serializers import ApartmentDetailsSerializer
from api.restful.viewsets.base_filter_viewsets import BaseFilterViewSet
from bma_backend.permissions import ApartmentPermissions


class ApartmentDetailsViewSet(BaseFilterViewSet):
    """
    CRUD Operations for listing/creating/updating apartment details.
    """
    queryset = ApartmentDetails.objects.all().order_by("apartment_number")
    serializer_class = ApartmentDetailsSerializer
    permission_classes = [ApartmentPermissions]
    http_method_names = ["get", "post", "put", "patch"]
    filterset_class = ApartmentDetailsFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        
        if isinstance(request.data, list):
            instances = ApartmentDetails.objects.bulk_create([ApartmentDetails(**item) for item in serializer.validated_data])
            serializer = self.get_serializer(instances, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
