from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

from api.models import UserData
from api.restful.serializers import UserSerializer, UserLoginSerializer
from api.restful.viewsets.base_filter_viewsets import BaseFilterViewSet
from api.filters import UsersFilter

from bma_backend.permissions import UserPermissions


class UsersViewSet(BaseFilterViewSet):
    """
    CRUD Operations for listing/creating/deleting/updating users.
    """
    queryset = UserData.objects.all().order_by("id")
    serializer_class = UserSerializer
    lookup_field = "id"
    permission_classes = [UserPermissions]
    filterset_class = UsersFilter

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
