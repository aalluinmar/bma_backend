from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
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
