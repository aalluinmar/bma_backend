
from django.db import models
from django.core.validators import MinValueValidator

from api.models import Audit, BuildingDetails, ApartmentDetails


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
    parking_fee = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Fee associated with the parking space."
    )

    class Meta:
        verbose_name = "Parking"
        verbose_name_plural = "Parking Spaces"
        ordering = ["parking_number", "building_number", "apartment_number"]
        unique_together = ("parking_number", "building_number", "apartment_number")
