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
