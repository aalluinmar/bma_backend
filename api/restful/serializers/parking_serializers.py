from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import ParkingDetails


class ParkingDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingDetails
        exclude = ["audit_status"]
        extra_kwargs = {"apartment_number": {"required": False}}

    def validate(self, data):
        apartment_number = data.get("apartment_number", None)
        building_number = data.get("building_number", None)

        # Validate the number of reserved parking spots for the apartment
        # Apartment field will be given only when the tenant books the apartment.
        if (hasattr(self, "context") and self.context.get("request", {}).method == "POST"):
            # This field will be given only when the tenant books the apartment
            if (apartment_number and hasattr(apartment_number, "apartment_number")):
                raise ValidationError(
                    {
                        "apartment_number": [
                            f"Cannot reserve parking spot for apartment" +
                            f" `{apartment_number.apartment_number}` before booking apartment."
                        ]
                    }
                )
            elif data.get("parking_status", "") != "available":
                raise ValidationError(
                    {
                        "parking_status": [
                            "Parking spot cannot be created with status other than `available`."
                        ]
                    }
                )
            # Validate the maximum number of parking rows allowed for a specific building
            elif building_number:
                max_parking_rows_per_building = 2 * 25 * building_number.no_of_floors
                existing_parking_rows_for_building = ParkingDetails.objects.filter(
                    building_number=building_number
                ).count()
                if existing_parking_rows_for_building >= max_parking_rows_per_building:
                    raise ValidationError(
                        f"Number of parking spaces for building `{building_number}` exceeds the maximum limit."
                    )
        elif (hasattr(self, "context") and self.context.get("request", {}).method in ["PUT", "PATCH"]) and apartment_number:
            reserved_spots_count = ParkingDetails.objects.filter(
                apartment_number=apartment_number,
                parking_status__in=["reserved", "occupied"]
            ).count()
            # Validate the maximum number of parking spots allowed for a specific apartment
            if reserved_spots_count >= 2:
                raise ValidationError(
                    {
                        "apartment_number": [
                            f"Cannot reserve more than two parking spots for apartment `{apartment_number.apartment_number}`."
                        ]
                    },
                )
            # Validate the parking status for the parking spot
            if data.get("parking_status", "") not in ["reserved", "occupied"]:
                raise ValidationError(
                    {
                        "parking_status": [
                            "Parking spot cannot be updated with status other than `reserved` or `occupied`."
                        ]
                    }
                )

        return data
