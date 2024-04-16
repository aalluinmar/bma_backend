from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.db.models import JSONField
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date

from api.models.audit import Audit
from api.models.apartment_details import ApartmentDetails
from api.utils.utils import generate_unique_integer_number
from api.constants import constants as constants
from api.constants.constants import default_fees, default_discounts
from dateutil.relativedelta import relativedelta


def validate_default_fees(value):
    if set(value.keys()) != set(constants.default_fees().keys()) or len(value) != len(constants.default_fees()):
        raise ValidationError("Only the default keys are allowed for fees.")

def validate_default_discounts(value):
    if set(value.keys()) != set(constants.default_discounts().keys()) or len(value) != len(constants.default_discounts()):
        raise ValidationError("Only the default keys are allowed for discount fees.")


class LeaseDetails(Audit):
    """
    Lease for an Apartment.
    """
    agreement_number = models.BigAutoField(
        primary_key=True,
        editable=False,
        default=generate_unique_integer_number,
        help_text="Unique 12-digit agreement number"
    )
    start_date = models.DateField(help_text="Start date of the lease.")
    end_date = models.DateField(help_text="End date of the lease.")
    duration = models.PositiveIntegerField(
        choices=constants.LEASE_DURATION_CHOICES,
        help_text="Duration of the lease in months."
    )
    rent_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(1.0)],
        help_text="Rent amount per month."
    )
    security_deposit = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Security deposit amount."
    )
    additional_charges = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Additional charges."
    )
    payment_schedule = models.CharField(
        max_length=20,
        choices=[
            ('weekly', 'Weekly'),
            ('bi_weekly', 'Bi-Weekly'),
            ('monthly', 'Monthly'),
        ],
        help_text="Payment schedule for rent."
    )
    lease_status = models.CharField(
        max_length=20,
        choices=constants.LEASE_STATUS_CHOICES,
        help_text="Status of the lease."
    )
    lease_notes = models.CharField(
        max_length=1000,
        blank=True,
        help_text="Additional notes or comments about the lease."
    )
    lease_exemption = models.CharField(
        max_length=1000,
        blank=True, null=True,
        help_text="Exemptions to the lease."
    )
    # Store various fees associated with the lease
    fees = JSONField(
        blank=True,
        null=True,
        default=default_fees,
        validators=[validate_default_fees],
        help_text="JSON field to store various fees associated with the lease."
    )

    # Store various discounts associated with the lease
    discounts = JSONField(
        blank=True,
        null=True,
        default=default_discounts,
        validators=[validate_default_discounts],
        help_text="JSON field to store various discounts associated with the lease."
    )

    # Lease Break Details
    lease_break_flag = models.BooleanField(
        default=False,
        help_text="Indicates whether the lease was broken."
    )
    lease_break_date = models.DateField(
        blank=True,
        null=True,
        help_text="Date when the lease was broken."
    )
    lease_break_reason = models.TextField(
        blank=True,
        null=True,
        help_text="Reason for breaking the lease."
    )

    # Foreign Keys
    apartment_number = models.ForeignKey(
        ApartmentDetails,
        on_delete=models.CASCADE,
        to_field="apartment_number",  # Point to the "apartment_number" field in ApartmentDetails
        related_name="leases",
        help_text="Apartment for the specific lease agreement."
    )

    def save(self, *args, **kwargs):
        # Compute end date if not provided
        if not self.end_date:
            self.end_date = self.start_date + relativedelta(months=self.duration)

        super().save(*args, **kwargs)

    def clean(self):
        # Ensure the start date is not in the past
        if self.start_date < timezone.now().date():
            raise ValidationError("Start date cannot be in the past.")

        # Ensure end date is greater than start date
        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError("End date must be after the start date.")

        # Ensure lease duration is valid
        if self.duration not in [6, 9, 12]:
            raise ValidationError("Invalid lease duration.")

        super().clean()

    class Meta:
        ordering = ["-start_date"]
        unique_together = ["agreement_number", "start_date"]
