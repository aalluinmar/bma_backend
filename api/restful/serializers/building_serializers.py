from rest_framework import serializers

from api.models import BuildingDetails

class BuildingDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuildingDetails
        exclude = ["audit_status"]
