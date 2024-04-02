
from django_filters import rest_framework as filters
from api.models import ApartmentDetails, BuildingDetails, UserData, ParkingDetails
from api.constants import constants as constants
from rest_framework.exceptions import ValidationError


def filter_boolean_field(queryset, name, value):
    """
    Check provided field's value as Boolean value.
    """
    if value is None:
        return queryset
    elif value in [True, False]:
        return queryset.filter(**{name:value})
    elif value.lower() == 'true':
        return queryset.filter(**{name: True})
    elif value.lower() == 'false':
        return queryset.filter(**{name: False})
    elif type(value) is str:
        raise ValidationError({name: "Value must be a boolean (True or False)."})
    else:
        return queryset.none()  # Return an empty queryset for invalid values


class ApartmentDetailsFilter(filters.FilterSet):

    """
    Below fields type is BooleanField but here we added it as CharFilter
    in order to call the filter_boolean_field method to avoid unnecessary values.
    """

    is_available = filters.CharFilter(
        field_name="is_available", label="Apartment Availability", method="filter_boolean_field"
    )
    dishwasher = filters.CharFilter(
        field_name="dishwasher", method="filter_boolean_field", label="Diswasher Availability"
    )
    microwave = filters.CharFilter(
        field_name="microwave", method="filter_boolean_field", label="Microwave Availability"
    )
    carpet = filters.CharFilter(
        field_name="carpet", method="filter_boolean_field", label="Carpet Availability"
    )
    refrigerator = filters.CharFilter(
        field_name="refrigerator", method="filter_boolean_field", label="Refrigerator Availability"
    )
    air_condition = filters.CharFilter(
        field_name="air_condition", method="filter_boolean_field", label="Air Condition Availability"
    )
    pets = filters.CharFilter(
        field_name="pets", method="filter_boolean_field", label="Pets Availability"
    )
    smoking = filters.CharFilter(
        field_name="smoking", method="filter_boolean_field", label="Smoking Availability"
    )

    def filter_boolean_field(self, queryset, name, value):
        return filter_boolean_field(queryset, name, value)

    class Meta:
        model = ApartmentDetails
        fields = {
            "apartment_number": constants.EXACT_FIELD_TYPE_FILTER,
            "building_number": constants.EXACT_FIELD_TYPE_FILTER,
            "price": constants.NUMBER_TYPE_FILTER,
            "bedrooms": constants.NUMBER_TYPE_FILTER,
            "bathrooms": constants.NUMBER_TYPE_FILTER,
            "closets": constants.NUMBER_TYPE_FILTER,
            "floor_number": constants.NUMBER_TYPE_FILTER,
            "no_of_occupants": constants.NUMBER_TYPE_FILTER,
            "stove": constants.EXACT_FIELD_TYPE_FILTER,
            "laundry": constants.EXACT_FIELD_TYPE_FILTER,
        }


class BuildingDetailsFilter(filters.FilterSet):

    """
    Below fields type is BooleanField but here we added it as CharFilter
    in order to call the filter_boolean_field method to avoid unnecessary values.
    """

    is_constructed = filters.CharFilter(
        field_name="is_constructed", method="filter_boolean_field", label="Building Availability"
    )

    def filter_boolean_field(self, queryset, name, value):
        return filter_boolean_field(queryset, name, value)

    class Meta:
        model = BuildingDetails
        fields = {
            "building_number": constants.EXACT_FIELD_TYPE_FILTER,
            "street_name": constants.EXACT_FIELD_TYPE_FILTER,
            "city": constants.EXACT_FIELD_TYPE_FILTER,
            "state": constants.EXACT_FIELD_TYPE_FILTER,
            "country": constants.EXACT_FIELD_TYPE_FILTER,
            "zip_code": constants.EXACT_FIELD_TYPE_FILTER,
            "no_of_floors": constants.EXACT_FIELD_TYPE_FILTER,
            "constructed_on": constants.EXACT_FIELD_TYPE_FILTER,
        }


class UsersFilter(filters.FilterSet):

    """
    Below fields type is BooleanField but here we added it as CharFilter
    in order to call the filter_boolean_field method to avoid unnecessary values.
    """

    is_admin = filters.CharFilter(
        field_name="is_admin", method="filter_boolean_field", label="Active or Inactive Admin"
    )
    is_tenant = filters.CharFilter(
        field_name="is_tenant", method="filter_boolean_field", label="Active or Inactive Tenant"
    )
    is_active = filters.CharFilter(
        field_name="is_active", method="filter_boolean_field", label="Active or Inactive User"
    )

    def filter_boolean_field(self, queryset, name, value):
        return filter_boolean_field(queryset, name, value)

    class Meta:
        model = UserData
        fields = {
            "username": constants.EXACT_FIELD_TYPE_FILTER,
            "first_name": constants.EXACT_FIELD_TYPE_FILTER,
            "last_name": constants.EXACT_FIELD_TYPE_FILTER,
            "email": constants.EXACT_FIELD_TYPE_FILTER,
            "phone_number": constants.EXACT_FIELD_TYPE_FILTER,
            "current_address": constants.EXACT_FIELD_TYPE_FILTER,
            "city": constants.EXACT_FIELD_TYPE_FILTER,
            "state": constants.EXACT_FIELD_TYPE_FILTER,
            "country": constants.EXACT_FIELD_TYPE_FILTER,
            "zip_code": constants.EXACT_FIELD_TYPE_FILTER,
        }


class ParkingDetailsFilter(filters.FilterSet):
    """
    Below fields types required to be filtered as per the given type.
    """

    class Meta:
        model = ParkingDetails
        fields = {
            "parking_number": constants.EXACT_FIELD_TYPE_FILTER,
            "building_number": constants.EXACT_FIELD_TYPE_FILTER,
            "apartment_number": constants.EXACT_FIELD_TYPE_FILTER,
            "parking_type": constants.EXACT_FIELD_TYPE_FILTER,
            "parking_status": constants.EXACT_FIELD_TYPE_FILTER,
            "parking_fee": constants.NUMBER_TYPE_FILTER,
        }