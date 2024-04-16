from django.db import transaction

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
            # Collect unique building and floor combinations from the data
            building_floor_combinations = {(item['building_number'], item['floor_number']) for item in serializer.validated_data}
            
            # Calculate apartment numbers for each building and floor combination
            apartment_numbers = {}
            for building_number, floor_number in building_floor_combinations:
                existing_apartments_count = ApartmentDetails.objects.filter(
                    building_number=building_number,
                    floor_number=floor_number
                ).count()
                apartment_numbers[(building_number, floor_number)] = existing_apartments_count
            
            # Use transaction.atomic() to ensure atomicity when bulk creating instances
            with transaction.atomic():
                instances = []
                for item in serializer.validated_data:
                    building_number = item['building_number']
                    floor_number = item['floor_number']
                    existing_apartments_count = apartment_numbers[(building_number, floor_number)]
                    apartment_number = floor_number * 100 + existing_apartments_count + 1
                    apartment_numbers[(building_number, floor_number)] += 1  # Update count for next apartment
                    item['apartment_number'] = apartment_number
                    instances.append(ApartmentDetails(**item))
                instances = ApartmentDetails.objects.bulk_create(instances)
            
            serializer = self.get_serializer(instances, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
