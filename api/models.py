from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django_countries.fields import CountryField
from localflavor.us.models import USStateField, USZipCodeField


class UserData(AbstractUser):
    """
    Extending the customer User Model using the Django's inbuilt AbstractUser Model.
    """
    id = models.AutoField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=150, help_text="First Name of the user")
    last_name = models.CharField(max_length=150, help_text="Last Name of the user")
    phone_number = models.CharField(
        max_length=17,
        help_text="Phone Number of the user, (Eg: +1 (123) 456-7890)",
        validators=[
            RegexValidator(
                regex=r'^\+1 \(\d{3}\) \d{3}-\d{4}$',
                message='Phone number must be in the format: +1 (513) 123-7890'
            )
        ]
    )
    current_address = models.CharField(max_length=500, help_text="Current Address of the user")
    city = models.CharField(max_length=25, help_text="Enter Current City")
    state = USStateField(help_text='Please select your state')
    country = CountryField(blank_label="(select country)", help_text='Please select your country')
    zip_code = USZipCodeField(
        help_text='Please enter your ZIP code in the format XXXXX or XXXXX-XXXX.',
        validators=[
        RegexValidator(
                regex=r'^\d{5}(?:-\d{4})?$',
                message='Enter a valid ZIP code in the format XXXXX or XXXXX-XXXX.'
            )
        ]
    )
    is_admin = models.BooleanField(default=False, help_text="Admin User")
    is_tenant = models.BooleanField(default=False, help_text="Customer/Tenant User")
    is_active = models.BooleanField(default=True, help_text="Active or Inactive User")

    # Specify unique related_name attributes to resolve clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='user permissions',
    )


class BuildingDetails(models.Model):
    """
    Community Building details.
    """
    building_number = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r'^[1-9][0-9]*$',
                message='Building number must be a valid integer with at least two digits.',
                code='invalid_building_number'
            )
        ],
        primary_key=True,
        help_text="Enter the Building Number. It must be a valid integer with at least two digits."
    )
    street_name = models.CharField(max_length=100, help_text="Enter the Street Name")
    city = models.CharField(max_length=25, help_text="Enter Current City")
    state = USStateField(help_text='Please select your State')
    country = CountryField(blank_label="(Select Country)", help_text='Please select your Country')
    zip_code = USZipCodeField(
        help_text='Enter your ZIP code in the format XXXXX or XXXXX-XXXX.',
        validators=[
        RegexValidator(
                regex=r'^\d{5}(?:-\d{4})?$',
                message='Enter a valid ZIP code in the format XXXXX or XXXXX-XXXX.'
            )
        ]
    )
    no_of_floors = models.PositiveIntegerField(help_text="Enter the Number of Floors")
    is_constructed = models.BooleanField(default=False, help_text="Choose True if building constructed")


class ApartmentDetails(models.Model):
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
        to_field='building_number',  # Point to the 'building_number' field in BuildingDetails
        related_name="apartments",
        help_text="The building in which the apartment is located."
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
    floor = models.PositiveIntegerField(
        default=1, help_text="Floor number of the apartment."
    )
    no_of_occupants = models.PositiveIntegerField(
        default=1, help_text="Number of occupants allowed in the apartment."
    )
    stove = models.CharField(
        max_length=10,
        choices=[
            ('Electric', 'Electric'),
            ('Gas', 'Gas'),
        ],
        help_text="Type of stove in the apartment."
    )
    laundry = models.CharField(
        max_length=13,
        choices=[
            ('in_unit', 'In Unit'),
            ('floor', 'Floor'),
            ('building', 'Building'),
            ('not_available', 'Not Available')
        ],
        help_text="Location of laundry facilities in or near the apartment."
    )
