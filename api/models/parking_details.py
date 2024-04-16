
from django.db import models
from django.db.models import JSONField
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from api.models import Audit, BuildingDetails, ApartmentDetails
from api.constants.constants import default_parking_fees


def validate_parking_fees(value):
    if set(value.keys()) != set(default_parking_fees().keys()) or len(value) != len(default_parking_fees()):
        raise ValidationError("Only the default keys are allowed for parking fees.")


class ParkingDetails(Audit):
    """
    Parking information associated with an Apartment.
    """
    # Primary Key
    parking_number = models.AutoField(
        primary_key=True,
        help_text="Unique ID for the parking space."
    )

    # Foreign Key
    building_number = models.ForeignKey(
        BuildingDetails,
        on_delete=models.CASCADE,
        to_field="building_number",  # Use building_number as the foreign key
        related_name="parking_spaces",
        help_text="Building associated with the parking space."
    )
    apartment_number = models.ForeignKey(
        ApartmentDetails,
        on_delete=models.CASCADE,
        to_field="apartment_number",  # Use apartment_number as the foreign key
        related_name="parking_spaces",
        null=True,  # Optional field
        blank=True,
        help_text="Apartment associated with the parking space.",
    )

    # Parking Details
    parking_type = models.CharField(
        max_length=10,
        choices=[
            ("covered", "Covered"),
            ("uncovered", "Uncovered"),
            ("garage", "Garage"),
        ],
        help_text="Type of parking space (e.g., covered, uncovered, garage)."
    )
    parking_status = models.CharField(
        max_length=20,
        choices=[
            ("available", "Available"),
            ("reserved", "Reserved"),
            ("occupied", "Occupied"),
            ("maintenance", "Maintenance"),
        ],
        default="available",
        help_text="Status of the parking space."
    )

    # Store fees associated with the parking type
    parking_fee = JSONField(
        default=default_parking_fees,
        validators=[validate_parking_fees],
        help_text="JSON field to store fees associated with the parking space type. " +
            f"Eg: Dictionary of covered, uncovered, garage fees. {(default_parking_fees())}"
    )

    class Meta:
        verbose_name = "Parking"
        verbose_name_plural = "Parking Spaces"
        ordering = ["parking_number", "building_number", "apartment_number"]
        unique_together = ("parking_number", "building_number", "apartment_number")
