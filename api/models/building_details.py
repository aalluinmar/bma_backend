from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django_countries.fields import CountryField
from localflavor.us.models import USStateField, USZipCodeField

from api.models import Audit


class BuildingDetails(Audit):
    """
    Community Building details.
    """
    building_number = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r"^[1-9][0-9]*$",
                message="Building number must be a valid integer with at least two digits.",
                code="invalid_building_number"
            )
        ],
        primary_key=True,
        help_text="Enter the Building Number. It must be a valid integer with at least two digits."
    )
    street_name = models.CharField(max_length=100, help_text="Enter the Street Name")
    city = models.CharField(max_length=25, help_text="Enter Current City")
    state = USStateField(help_text="Please select your State")
    country = CountryField(
        blank_label="(Select Country)",
        help_text="Please select your Country"
    )
    zip_code = USZipCodeField(
        help_text="Enter your ZIP code in the format XXXXX or XXXXX-XXXX.",
        validators=[
        RegexValidator(
                regex=r"^\d{5}(?:-\d{4})?$",
                message="Enter a valid ZIP code in the format XXXXX or XXXXX-XXXX."
            )
        ]
    )
    no_of_floors = models.PositiveIntegerField(help_text="Enter the Number of Floors")
    is_constructed = models.BooleanField(default=False, help_text="Choose True if building constructed")
    constructed_on = models.DateField(
        null=True,
        blank=True,
        help_text="Enter the Date of Construction"
    )
