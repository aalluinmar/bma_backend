import re
from django.core.exceptions import ValidationError

from rest_framework import serializers
from django.core.validators import MinValueValidator

from api.models import LeaseDetails, Tenant, UserData, ApartmentDetails
from api.constants import constants as constants


class TenantSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        help_text="First name of the tenant."
    )
    last_name = serializers.CharField(
        help_text="Last name of the tenant."
    )
    email = serializers.EmailField(
        help_text="Email address of the tenant."
    )
    application_fee = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.00)],
        help_text="Application fee charged."
    )

    class Meta:
        ref_name = "TenantInput"


class BookApartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for LeaseDetails model.
    """
    fees = serializers.JSONField(
        default=constants.default_fees(),
        help_text="Fees for the lease.",
    )
    discounts = serializers.JSONField(
        default=constants.default_discounts(),
        help_text="Discounts for the lease.",
    )
    tenants_list = TenantSerializer(
        many=True,
        help_text="List of tenants for the lease."
    )

    def validate_tenants_list(self, value):
        for tenant_data in value:
            # Check if all mandatory fields are provided
            if not all(field in tenant_data for field in ["first_name", "last_name", "email", "application_fee"]):
                raise ValidationError({
                    "tenants_list": "Each tenant must have 'first_name', 'last_name', 'email', and 'application_fee' fields."
                })

            # Check if the user exists and is active
            email = tenant_data["email"]
            if not UserData.objects.filter(email=email, is_active=True).exists():
                raise ValidationError(f"User with email {email} does not exist or is not active.")

            # Check if the user is already an active tenant in another apartment
            if Tenant.objects.filter(user__email=email, is_active=True).exists():
                raise ValidationError(
                    f"User with email {email} is already an active tenant in another apartment."
                )

        return value

    def decimal_validator(self, validation_key, sub_key_type, sub_key_value):
        if re.match(r'^\d+(\.\d{2})?$', str(sub_key_value)):
            raise ValidationError([
                    f"Invalid value `{sub_key_value}` for fee type `{sub_key_type}`. Value must be a decimal."
                ]
            )
        return sub_key_value

    def validate_fees(self, value):
        for fee_type, fee_value in value.items():
            self.decimal_validator("fees", fee_type, fee_value)
        return value

    def validate_discounts(self, value):
        for discount_type, discount_value in value.items():
            self.decimal_validator("discounts", discount_type, discount_value)
        return value

    def validate(self, data):
        print(data)
        # Validate the provided apartment number
        apartment_number = data.get("apartment_number", None)
        if not ApartmentDetails.objects.filter(apartment_number=apartment_number.apartment_number, is_available=True).exists():
            raise ValidationError({
                "apartment_number": f"The provided apartment is not available."
            })
        # Validate the rent amount against the price field for the apartment
        rent_amount = data.get("rent_amount")
        if not ApartmentDetails.objects.filter(price=rent_amount).exists():
            raise ValidationError({
                "rent_amount": f"The provided rent amount does not match the price for the apartment."
            })

        return data

    def create(self, validated_data):
        """
        Create a lease for the tenant(s).
        """
        tenants_list = list()
        tenants_data = validated_data.pop("tenants_list")
        # from dateutil.relativedelta import relativedelta
        # end_date = validated_data.get("start_date") + relativedelta(months=validated_data.get("duration"))
        # validated_data["end_date"] = end_date
        # from datetime import datetime
        # print(validated_data, "------------------", end_date)
        lease = LeaseDetails.objects.create(**validated_data)

        for tenant_data in tenants_data:
            user = UserData.objects.get(email=tenant_data["email"])
            obj = {
                "lease": lease,
                "user": user,
                "is_active": True,
                "move_in_date": lease.start_date,
                "move_out_date": lease.end_date,
                "application_fee": tenant_data["application_fee"],
            }
            tenant = Tenant.objects.create(**obj)
            tenant.first_name = tenant_data["first_name"]
            tenant.last_name = tenant_data["last_name"]
            tenant.email = tenant_data["email"]
            # Update the user as a tenant
            user.is_tenant = True
            user.save()
            tenants_list.append(tenant)

        # Set the apartment as unavailable
        apartment_number = validated_data["apartment_number"]
        apartment = ApartmentDetails.objects.get(apartment_number=apartment_number.apartment_number)
        apartment.is_available = False
        apartment.save()

        # Return the lease response
        lease.tenants_list = tenants_list
        return lease

    class Meta:
        model = LeaseDetails
        exclude = ["audit_status"]
        read_only_fields = [
            "id", "end_date", "lease_status", "lease_break_flag", "lease_break_date", "lease_break_reason"
        ]
