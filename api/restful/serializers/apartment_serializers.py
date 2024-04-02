from rest_framework import serializers

from api.models import ApartmentDetails

class ApartmentDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApartmentDetails
        exclude = ["audit_status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
