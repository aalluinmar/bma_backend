# Generated by Django 5.0.1 on 2024-04-04 23:04

import api.constants.constants
import api.models.lease_details
import api.models.parking_details
import api.utils.utils
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import localflavor.us.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingDetails',
            fields=[
                ('audit_status', models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE'), ('deleted', 'DELETED')], default='active', max_length=30)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('building_number', models.CharField(help_text='Enter the Building Number. It must be a valid integer with at least two digits.', max_length=20, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.RegexValidator(code='invalid_building_number', message='Building number must be a valid integer with at least two digits.', regex='^[1-9][0-9]*$')])),
                ('street_name', models.CharField(help_text='Enter the Street Name', max_length=100)),
                ('city', models.CharField(help_text='Enter Current City', max_length=25)),
                ('state', localflavor.us.models.USStateField(help_text='Please select your State', max_length=2)),
                ('country', django_countries.fields.CountryField(help_text='Please select your Country', max_length=2)),
                ('zip_code', localflavor.us.models.USZipCodeField(help_text='Enter your ZIP code in the format XXXXX or XXXXX-XXXX.', max_length=10, validators=[django.core.validators.RegexValidator(message='Enter a valid ZIP code in the format XXXXX or XXXXX-XXXX.', regex='^\\d{5}(?:-\\d{4})?$')])),
                ('no_of_floors', models.PositiveIntegerField(help_text='Enter the Number of Floors')),
                ('is_constructed', models.BooleanField(default=False, help_text='Choose True if building constructed')),
                ('constructed_on', models.DateField(blank=True, help_text='Enter the Date of Construction', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApartmentDetails',
            fields=[
                ('audit_status', models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE'), ('deleted', 'DELETED')], default='active', max_length=30)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('apartment_number', models.AutoField(help_text='Auto-incremented unique identifier for the apartment.', primary_key=True, serialize=False, unique=True)),
                ('price', models.DecimalField(decimal_places=2, help_text='Rent amount per month.', max_digits=10, validators=[django.core.validators.MinValueValidator(1.0)])),
                ('description', models.TextField(help_text='Description of the apartment.', max_length=500)),
                ('is_available', models.BooleanField(default=True, help_text='Indicates whether the apartment is available for rent.')),
                ('dishwasher', models.BooleanField(default=False, help_text='Indicates whether the apartment has a dishwasher.')),
                ('microwave', models.BooleanField(default=False, help_text='Indicates whether the apartment has a microwave.')),
                ('carpet', models.BooleanField(default=False, help_text='Indicates whether the apartment has carpet flooring.')),
                ('refrigerator', models.BooleanField(default=False, help_text='Indicates whether the apartment has a refrigerator.')),
                ('air_condition', models.BooleanField(default=False, help_text='Indicates whether the apartment has a Air Conditioner.')),
                ('bedrooms', models.PositiveIntegerField(default=0, help_text='Number of bedrooms in the apartment.')),
                ('bathrooms', models.PositiveIntegerField(default=1, help_text='Number of bathrooms in the apartment.')),
                ('closets', models.PositiveIntegerField(default=1, help_text='Number of closets in the apartment.')),
                ('floor_number', models.PositiveIntegerField(help_text='Floor number of the apartment.')),
                ('no_of_occupants', models.PositiveIntegerField(default=1, help_text='Number of occupants allowed in the apartment.')),
                ('stove', models.CharField(choices=[('Electric', 'Electric'), ('Gas', 'Gas')], help_text='Type of stove in the apartment.', max_length=10)),
                ('laundry', models.CharField(choices=[('in_unit', 'In Unit'), ('floor', 'Floor'), ('building', 'Building'), ('not_available', 'Not Available')], help_text='Location of laundry facilities in or near the apartment.', max_length=13)),
                ('pets', models.BooleanField(default=False, help_text='Indicates whether pets are allowed in the apartment.')),
                ('smoking', models.BooleanField(default=False, help_text='Indicates whether smoking is allowed in the apartment.')),
                ('building_number', models.ForeignKey(help_text='The building in which the apartment is located.', on_delete=django.db.models.deletion.CASCADE, related_name='apartments', to='api.buildingdetails')),
            ],
            options={
                'ordering': ['apartment_number'],
            },
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(help_text='First Name of the user', max_length=150)),
                ('last_name', models.CharField(help_text='Last Name of the user', max_length=150)),
                ('phone_number', models.CharField(help_text='Phone Number of the user, (Eg: +1 (123) 456-7890)', max_length=17, validators=[django.core.validators.RegexValidator(message='Phone number must be in the format: +1 (513) 123-7890', regex='^\\+1 \\(\\d{3}\\) \\d{3}-\\d{4}$')])),
                ('current_address', models.CharField(help_text='Current Address of the user', max_length=500)),
                ('city', models.CharField(help_text='Enter Current City', max_length=25)),
                ('state', localflavor.us.models.USStateField(help_text='Please select your state', max_length=2)),
                ('country', django_countries.fields.CountryField(help_text='Please select your country', max_length=2)),
                ('zip_code', localflavor.us.models.USZipCodeField(help_text='Please enter your ZIP code in the format XXXXX or XXXXX-XXXX.', max_length=10, validators=[django.core.validators.RegexValidator(message='Enter a valid ZIP code in the format XXXXX or XXXXX-XXXX.', regex='^\\d{5}(?:-\\d{4})?$')])),
                ('is_admin', models.BooleanField(default=False, help_text='Admin User')),
                ('is_tenant', models.BooleanField(default=False, help_text='Customer/Tenant User')),
                ('is_active', models.BooleanField(default=True, help_text='Active or Inactive User')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Timestamp when the user was created.')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the user was last modified.')),
                ('created_by', models.ForeignKey(blank=True, help_text='User who created this user.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_users', to='api.userdata')),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='LeaseDetails',
            fields=[
                ('audit_status', models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE'), ('deleted', 'DELETED')], default='active', max_length=30)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('agreement_number', models.AutoField(default=api.utils.utils.generate_unique_integer_number, editable=False, help_text='Unique 12-digit agreement number', primary_key=True, serialize=False)),
                ('start_date', models.DateField(help_text='Start date of the lease.')),
                ('end_date', models.DateField(help_text='End date of the lease.')),
                ('duration', models.PositiveSmallIntegerField(choices=[(6, '6 months'), (9, '9 months'), (12, '12 months')], help_text='Duration of the lease in months.')),
                ('rent_amount', models.DecimalField(decimal_places=2, help_text='Rent amount per month.', max_digits=10, validators=[django.core.validators.MinValueValidator(1.0)])),
                ('security_deposit', models.DecimalField(decimal_places=2, help_text='Security deposit amount.', max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('additional_charges', models.DecimalField(decimal_places=2, help_text='Additional charges.', max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('payment_schedule', models.CharField(choices=[('weekly', 'Weekly'), ('bi_weekly', 'Bi-Weekly'), ('monthly', 'Monthly')], help_text='Payment schedule for rent.', max_length=20)),
                ('lease_status', models.CharField(choices=[('not_started', 'Not Started'), ('started', 'Started'), ('completed', 'Completed'), ('transferred', 'Transferred'), ('terminated', 'Terminated')], help_text='Status of the lease.', max_length=20)),
                ('lease_notes', models.CharField(blank=True, help_text='Additional notes or comments about the lease.', max_length=1000)),
                ('lease_exemption', models.CharField(blank=True, help_text='Exemptions to the lease.', max_length=1000, null=True)),
                ('fees', models.JSONField(blank=True, default=api.constants.constants.default_fees, help_text='JSON field to store various fees associated with the lease.', null=True, validators=[api.models.lease_details.validate_default_fees])),
                ('discounts', models.JSONField(blank=True, default=api.constants.constants.default_discounts, help_text='JSON field to store various discounts associated with the lease.', null=True, validators=[api.models.lease_details.validate_default_discounts])),
                ('lease_break_flag', models.BooleanField(default=False, help_text='Indicates whether the lease was broken.')),
                ('lease_break_date', models.DateField(blank=True, help_text='Date when the lease was broken.', null=True)),
                ('lease_break_reason', models.TextField(blank=True, help_text='Reason for breaking the lease.', null=True)),
                ('apartment_number', models.ForeignKey(help_text='Apartment for the specific lease agreement.', on_delete=django.db.models.deletion.CASCADE, related_name='leases', to='api.apartmentdetails')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_%(app_label)s_%(class)s_set', to='api.userdata')),
                ('modified_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified_%(app_label)s_%(class)s_set', to='api.userdata')),
            ],
            options={
                'ordering': ['-start_date'],
                'unique_together': {('agreement_number', 'start_date')},
            },
        ),
        migrations.AddField(
            model_name='buildingdetails',
            name='created_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_%(app_label)s_%(class)s_set', to='api.userdata'),
        ),
        migrations.AddField(
            model_name='buildingdetails',
            name='modified_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified_%(app_label)s_%(class)s_set', to='api.userdata'),
        ),
        migrations.AddField(
            model_name='apartmentdetails',
            name='created_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_%(app_label)s_%(class)s_set', to='api.userdata'),
        ),
        migrations.AddField(
            model_name='apartmentdetails',
            name='modified_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified_%(app_label)s_%(class)s_set', to='api.userdata'),
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('audit_status', models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE'), ('deleted', 'DELETED')], default='active', max_length=30)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('tenant_id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID for the tenant.', primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, help_text='Indicates whether the tenant is currently active.')),
                ('move_in_date', models.DateField(help_text="Start date of the tenant's lease.")),
                ('move_out_date', models.DateField(help_text="End date of the tenant's lease.")),
                ('application_fee', models.DecimalField(decimal_places=2, help_text='Application fee charged.', max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('lease_break_flag', models.BooleanField(default=False, help_text='Indicates whether the Individual tenant lease was broken.')),
                ('lease_break_date', models.DateField(blank=True, help_text='Date when the lease was broken.', null=True)),
                ('lease_break_reason', models.TextField(blank=True, help_text='Reason for breaking the lease.', null=True)),
                ('lease_break_fee', models.DecimalField(blank=True, decimal_places=2, help_text='Fee charged for breaking the lease.', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('notes', models.TextField(blank=True, help_text='Additional notes about the tenant.', null=True)),
                ('lease', models.ForeignKey(help_text='Lease agreement associated with the tenant.', on_delete=django.db.models.deletion.CASCADE, related_name='tenants', to='api.leasedetails')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_%(app_label)s_%(class)s_set', to='api.userdata')),
                ('modified_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified_%(app_label)s_%(class)s_set', to='api.userdata')),
                ('user', models.ForeignKey(help_text='User associated with the tenant.', on_delete=django.db.models.deletion.CASCADE, to='api.userdata')),
            ],
            options={
                'unique_together': {('lease', 'user', 'move_in_date')},
            },
        ),
        migrations.CreateModel(
            name='ParkingDetails',
            fields=[
                ('audit_status', models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE'), ('deleted', 'DELETED')], default='active', max_length=30)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('parking_number', models.AutoField(help_text='Unique ID for the parking space.', primary_key=True, serialize=False)),
                ('parking_type', models.CharField(choices=[('covered', 'Covered'), ('uncovered', 'Uncovered'), ('garage', 'Garage')], help_text='Type of parking space (e.g., covered, uncovered, garage).', max_length=10)),
                ('parking_status', models.CharField(choices=[('available', 'Available'), ('reserved', 'Reserved'), ('occupied', 'Occupied'), ('maintenance', 'Maintenance')], default='available', help_text='Status of the parking space.', max_length=20)),
                ('parking_fee', models.JSONField(default=api.constants.constants.default_parking_fees, help_text="JSON field to store fees associated with the parking space type. Eg: Dictionary of covered, uncovered, garage fees. {'covered': 0.0, 'uncovered': 0.0, 'garage': 0.0}", validators=[api.models.parking_details.validate_parking_fees])),
                ('apartment_number', models.ForeignKey(blank=True, help_text='Apartment associated with the parking space.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parking_spaces', to='api.apartmentdetails')),
                ('building_number', models.ForeignKey(help_text='Building associated with the parking space.', on_delete=django.db.models.deletion.CASCADE, related_name='parking_spaces', to='api.buildingdetails')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_%(app_label)s_%(class)s_set', to='api.userdata')),
                ('modified_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='modified_%(app_label)s_%(class)s_set', to='api.userdata')),
            ],
            options={
                'verbose_name': 'Parking',
                'verbose_name_plural': 'Parking Spaces',
                'ordering': ['parking_number', 'building_number', 'apartment_number'],
                'unique_together': {('parking_number', 'building_number', 'apartment_number')},
            },
        ),
    ]
