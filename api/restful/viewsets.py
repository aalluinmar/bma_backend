from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import UserData
from api.restful.serializers import UserLoginSerializer, UserSerializer
from bma_backend.permissions import IsAdminOrReadOnly

class CustomPagination(LimitOffsetPagination):
    """
    Set default pagination limit and offset value
    """
    default_limit = 10  # Set the default page size
    max_limit = 100  # Set the maximum page size
    limit_query_param = 'limit'  # Set the query parameter for limit
    offset_query_param = 'offset'  # Set the query parameter for offset


class UsersViewSet(viewsets.ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination  # Enable pagination


class UserLoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserLoginSerializer(data=request.data)
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
