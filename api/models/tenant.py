import uuid

from datetime import date
from dateutil.relativedelta import relativedelta

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from api.models.audit import Audit
from api.models.lease_details import LeaseDetails

from api.models.userdata import UserData


class Tenant(Audit):
    """
    Tenant associated with a Lease.
    """
    # Use uuid as the primary key
    tenant_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="UUID for the tenant."
    )

    # Foreign keys
    lease = models.ForeignKey(
        LeaseDetails,
        on_delete=models.CASCADE,
        to_field="agreement_number",  # Use agreement_number as the foreign key
        related_name="tenants",
        help_text="Lease agreement associated with the tenant."
    )
    user = models.ForeignKey(
        UserData,
        on_delete=models.CASCADE,
        help_text="User associated with the tenant."
    )

    # Tenant Details
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether the tenant is currently active."
    )
    move_in_date = models.DateField(help_text="Start date of the tenant's lease.")
    move_out_date = models.DateField(help_text="End date of the tenant's lease.")
    application_fee = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Application fee charged."
    )

    # Lease Break Details
    lease_break_flag = models.BooleanField(
        default=False,
        help_text="Indicates whether the Individual tenant lease was broken."
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
    lease_break_fee = models.DecimalField(
        blank=True, null=True,
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Fee charged for breaking the lease."
    )

    # TODO: Notes as JSONField to store additional information with date field and description
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about the tenant."
    )

    def clean(self):
        super().clean()

        # Calculate lease duration based on LEASE_DURATION_CHOICES
        lease_duration = self.lease.duration
        if lease_duration not in [6, 9, 12]:
            raise ValidationError("Invalid lease duration.")

        # Calculate move_out_date based on move_in_date and lease_duration
        move_in_date = self.move_in_date
        move_out_date = move_in_date + relativedelta(months=lease_duration)
        # move_out_date = move_in_date + timedelta(months=lease_duration)

        # Validate move_out_date
        if move_out_date <= move_in_date:
            raise ValidationError("Invalid lease dates.")

        # Check if move_out_date is greater than lease end date in Lease model
        if move_out_date > self.lease.end_date:
            raise ValidationError("Lease end date exceeds the lease agreement end date.")

        # Check if move_out_date is less than lease start date in Lease model
        if move_out_date < self.lease.start_date:
            raise ValidationError("Lease end date is before the lease agreement start date.")

        # Check if move_out_date is less than lease start date
        if move_out_date < move_in_date:
            raise ValidationError("Lease end date is before the lease start date.")

        # Validate if the same tenants start date is not in the past
        if self.move_in_date < date.today():
            raise ValidationError("Tenant start date cannot be in the past.")

        # Validate if the same tenants end date is not in the past
        if self.move_out_date < date.today():
            raise ValidationError("Tenant end date cannot be in the past.")

        # Validate lease_break_date 
        if self.lease_break_date and self.lease_break_date < move_in_date:
            raise ValidationError("Lease break date is before the lease start date.")

        # Validate if the same lease break date is not in the past
        if self.lease_break_date and self.lease_break_date < date.today():
            raise ValidationError("Lease break date cannot be in the past.")

        # Validate if the same lease break date is not greater than the end date
        if self.lease_break_date and self.lease_break_date > self.move_out_date:
            raise ValidationError("Lease break date cannot be greater than end date.")

        # Validate if the same tenants start date is not greater than the end date
        if self.move_in_date > self.move_out_date:
            raise ValidationError("Tenant start date cannot be greater than end date.")

        # Validate if the same lease break fee is provided if lease is broken
        if self.lease_break_flag and not self.lease_break_fee:
            raise ValidationError("Lease break fee is required if lease is broken.")

        # Validate if the same lease break date is provided if lease is broken
        if self.lease_break_flag and not self.lease_break_date:
            raise ValidationError("Lease break date is required if lease is broken.")

        # Validate if the same lease break reason is provided if lease is broken
        if self.lease_break_flag and not self.lease_break_reason:
            raise ValidationError("Lease break reason is required if lease is broken.")

        # Validate if the same lease break fee is greater than 0
        if self.lease_break_fee and self.lease_break_fee <= 0:
            raise ValidationError("Lease break fee must be greater than 0.")

        # Update move_out_date
        self.move_out_date = move_out_date

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)    

    class Meta:
        unique_together = ("lease", "user", "move_in_date")
