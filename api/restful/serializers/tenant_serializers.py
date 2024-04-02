from rest_framework import serializers

from api.models import Tenant

class TenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tenant
        fields = "__all__"
