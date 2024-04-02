from django.db import models
from django.core.validators import MinValueValidator

from api.models.audit import Audit
from api.models.building_details import BuildingDetails


class ApartmentDetails(Audit):
    """
    Apartment and its amenities in a Building.
    """
    apartment_number = models.AutoField(
        primary_key=True, unique=True,
        help_text="Auto-incremented unique identifier for the apartment."
    )
    building_number = models.ForeignKey(
        BuildingDetails,
        on_delete=models.CASCADE,
        to_field="building_number",  # Point to the "building_number" field in BuildingDetails
        related_name="apartments",
        help_text="The building in which the apartment is located."
    )
    price = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],  # Minimum value set to $1
        help_text="Enter the Price of the Apartment."
    )
    description = models.TextField(
        max_length=500, help_text="Description of the apartment."
    )
    is_available = models.BooleanField(
        default=True, help_text="Indicates whether the apartment is available for rent."
    )
    dishwasher = models.BooleanField(
        default=False, help_text="Indicates whether the apartment has a dishwasher."
    )
    microwave = models.BooleanField(
        default=False, help_text="Indicates whether the apartment has a microwave."
    )
    carpet = models.BooleanField(
        default=False, help_text="Indicates whether the apartment has carpet flooring."
    )
    refrigerator = models.BooleanField(
        default=False, help_text="Indicates whether the apartment has a refrigerator."
    )
    air_condition = models.BooleanField(
        default=False, help_text="Indicates whether the apartment has a Air Conditioner."
    )
    bedrooms = models.PositiveIntegerField(
        default=0, help_text="Number of bedrooms in the apartment."
    )
    bathrooms = models.PositiveIntegerField(
        default=1, help_text="Number of bathrooms in the apartment."
    )
    closets = models.PositiveIntegerField(
        default=1, help_text="Number of closets in the apartment."
    )
    floor_number = models.PositiveIntegerField(
        help_text="Floor number of the apartment."
    )
    no_of_occupants = models.PositiveIntegerField(
        default=1, help_text="Number of occupants allowed in the apartment."
    )
    stove = models.CharField(
        max_length=10,
        choices=[
            ("Electric", "Electric"),
            ("Gas", "Gas"),
        ],
        help_text="Type of stove in the apartment."
    )
    laundry = models.CharField(
        max_length=13,
        choices=[
            ("in_unit", "In Unit"),
            ("floor", "Floor"),
            ("building", "Building"),
            ("not_available", "Not Available")
        ],
        help_text="Location of laundry facilities in or near the apartment."
    )
    pets = models.BooleanField(
        default=False, help_text="Indicates whether pets are allowed in the apartment."
    )
    smoking = models.BooleanField(
        default=False, help_text="Indicates whether smoking is allowed in the apartment."
    )

    class Meta:
        ordering = ["apartment_number"]

    def save(self, *args, **kwargs):
        if not self.apartment_number:  # If apartment number is not set
            # Get the count of existing apartments on the same floor
            existing_apartments_count = ApartmentDetails.objects.filter(
                building_number=self.building_number,
                floor_number=self.floor_number
            ).count()

            # Generate the apartment number based on floor number and existing count
            self.apartment_number = self.floor_number * 100 + existing_apartments_count + 1

        super().save(*args, **kwargs)
