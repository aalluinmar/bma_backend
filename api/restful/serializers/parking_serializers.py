import re
from decimal import Decimal

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import ParkingDetails, LeaseDetails
from api.constants.constants import default_parking_fees


class ParkingDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for ParkingDetails model.
    """
    parking_fee = serializers.JSONField(
        default=default_parking_fees(),
        help_text="Parking fees for the parking spot."
    )
    lease_agreement_number = serializers.CharField(
        required=False,
        help_text="Lease agreement number for the apartment."
    )

    def validate(self, data):
        apartment_number = data.get("apartment_number", None)
        building_number = data.get("building_number", None)
        lease_agreement_number = data.get("lease_agreement_number", None)

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
            # Validate the parking status for the parking spot
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
            elif lease_agreement_number:
                raise ValidationError(
                    {
                        "lease_agreement_number": [
                            "Cannot reserve parking spot without booking the apartment."
                        ]
                    }
                )

        # Validate the parking fee fields
        elif data.get("parking_fee", None):
            # Check if the user is admin to update/create the parking fees
            if self.context.get("request", {}).user.is_admin:
                # Validate the parking fees fields existance
                if data.get("parking_fee", {}).get("covered", None) is None:
                    raise ValidationError({"parking_fee": "Covered parking fee is required."})
                if data.get("parking_fee", {}).get("uncovered", None) is None:
                    raise ValidationError({"parking_fee": "Uncovered parking fee is required."})
                if data.get("parking_fee", {}).get("garage", None) is None:
                    raise ValidationError({"parking_fee": "Garage parking fee is required."})

                # Validate the parking fee for the parking spot (decimal with 2 decimal points)
                if not all(
                    re.match(r'^\d+(\.\d{2})?$', str(data.get("parking_fee", {}).get(parking_type, None)))
                    for parking_type in ["covered", "uncovered", "garage"]
                ):
                    raise ValidationError({
                        "parking_fee": [
                            "Parking fee must be a decimal value with exactly 2 numbers after the decimal point. (Eg: 0.00)"
                        ]
                    })
                # Validate the parking fee for the parking spot (greater than 0 and less than 1000)
                if not all(
                    0 <= Decimal(data.get("parking_fee", {}).get(parking_type, 0)) < 1000
                    for parking_type in ["covered", "uncovered", "garage"]
                ):
                    raise ValidationError({
                        "parking_fee": [
                            "Parking fee must be greater than 0 and less than 1000."
                        ]
                    })

            # Raise error if the user is not admin and tries to update/create the parking fees
            elif (
                    hasattr(self, "context") and self.context.get("request", {}).method in ["PUT", "PATCH"]
                    and (not self.context.get("request", {}).user.is_admin)
                    and hasattr(self.instance, "parking_fee") and self.instance.parking_fee != data.get("parking_fee", {})
                ):
                raise ValidationError("Only admin users can update/create parking fees.")

        # Validate the number of reserved parking spots for the apartment
        elif (hasattr(self, "context") and self.context.get("request", {}).method in ["PUT", "PATCH"]) and apartment_number:

            # Assign parking spot for the apartment only if the lease_agreement_number exists in the database
            if not lease_agreement_number:
                raise ValidationError({"lease_agreement_number": "Lease agreement number is required."})
            if not LeaseDetails.objects.filter(agreement_number=lease_agreement_number).exists():
                raise ValidationError({"lease_agreement_number": "Lease agreement number does not exist."})

            # Validate the number of reserved parking spots for the apartment
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

        # Raise error if the apartment number is not provided for reserved or occupied parking spot
        elif (not apartment_number and data.get("parking_status", "") in ["reserved", "occupied"]):
            raise ValidationError(
                {
                    "apartment_number": [
                        "Cannot reserve or occupy parking spot without booking the apartment."
                    ]
                }
            )

        return data

    class Meta:
        model = ParkingDetails
        exclude = ["audit_status"]
        extra_kwargs = {"apartment_number": {"required": False}}
