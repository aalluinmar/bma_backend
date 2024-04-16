# Description: This file contains the constants used in the API.

# Constants

# List of choices for the Audit status

AUDIT_STATUS = (
    ("active", "ACTIVE"),
    ("inactive", "INACTIVE"),
    ("deleted", "DELETED"),
)

# List of choices for the lease duration
LEASE_DURATION_CHOICES = [
    (6, "6 months"),
    (9, "9 months"),
    (12, "12 months"),
]

# List of choices for the lease status
LEASE_STATUS_CHOICES = [
    ("not_started", "Not Started"),
    ("started", "Started"),
    ("completed", "Completed"),
    ("transferred", "Transferred"),
    ("terminated", "Terminated"),
]

# Filter Types

EXACT_FIELD_TYPE_FILTER = ["exact"]

NUMBER_TYPE_FILTER = ["exact", "gte", "lte"]

# Default callable for fees
def default_fees():
    return {
        "damage_fee": 0.00,
        "break_lease_fee": 0.00,
        "pets_fee": 0.00,
        "trash_fee": 0.00,
        "sewage_fee": 0.00,
        "water_fee": 0.00,
        "electricity_fee": 0.00,
        "gas_fee": 0.00,
        "internet_fee": 0.00,
        "cable_fee": 0.00,
        # "parking_fee": 0.00,
        "miscellaneous_fee": 0.00,
    }

# Default callable for discounts
def default_discounts():
    return {
        "initial_discount": 0.00,
        "break_lease_discount": 0.00,
        "extension_discount": 0.00,
    }

# Default callable for discounts
def default_parking_fees():
    return {
        "covered": 0.00,
        "uncovered": 0.00,
        "garage": 0.00,
    }
