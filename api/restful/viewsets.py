from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import UserData, BuildingDetails, ApartmentDetails
from api.restful.serializers import (
    ApartmentDetailsSerializer,
    BuildingDetailsSerializer,
    UserLoginSerializer,
    UserSerializer,
)
from bma_backend.permissions import (
    ApartmentPermissions,
    BuildingPermissions,
    UserPermissions
)


class CustomPagination(LimitOffsetPagination):
    """
    Set default pagination limit and offset value
    """
    default_limit = 10  # Set the default page size
    max_limit = 100  # Set the maximum page size
    limit_query_param = 'limit'  # Set the query parameter for limit
    offset_query_param = 'offset'  # Set the query parameter for offset


class UsersViewSet(viewsets.ModelViewSet):
    """
    CRUD Operations for listing/creating/deleting/updating users.
    """
    queryset = UserData.objects.all().order_by("id")
    serializer_class = UserSerializer
    lookup_field = "id"
    permission_classes = [UserPermissions]
    pagination_class = CustomPagination  # Enable pagination

    def get_object(self):
        """
        Gets Object for the queryset Model.
        """
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.first()  # Get the first object
        if obj is None:
            raise NotFound(detail="User not found")
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        """
        Gets the Queryset based on the given Id.
        """
        if 'id' in self.kwargs:  # If 'id' is present in URL kwargs, it's a detail view
            return UserData.objects.filter(id=self.kwargs['id'])
        else:
            return self.queryset  # Default queryset for list view


class UserLoginViewSet(viewsets.ViewSet):
    """
    Viewset for User login API.
    """
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def create(self, request):
        """
        API Call for verifying user given credentials.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class BuildingDetailsViewSet(viewsets.ModelViewSet):
    """
    CRUD Operations for listing/creating/updating building details.
    """
    queryset = BuildingDetails.objects.all().order_by("building_number")
    serializer_class = BuildingDetailsSerializer
    permission_classes = [BuildingPermissions]
    http_method_names = ["get", "post", "put", "patch"]
    pagination_class = CustomPagination  # Enable pagination


class ApartmentDetailsViewSet(viewsets.ModelViewSet):
    """
    CRUD Operations for listing/creating/updating apartment details.
    """
    queryset = ApartmentDetails.objects.all().order_by("apartment_number")
    serializer_class = ApartmentDetailsSerializer
    permission_classes = [ApartmentPermissions]
    http_method_names = ["get", "post", "put", "patch"]
    pagination_class = CustomPagination  # Enable pagination

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

