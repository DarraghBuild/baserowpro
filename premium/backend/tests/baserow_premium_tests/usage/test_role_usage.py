import pytest
from baserow_premium.license.models import License, LicenseUser
from baserow_premium.usage.handler import PremiumUsageHandler
from baserow_premium_tests.license.test_license_handler import VALID_TWO_SEAT_LICENSE


@pytest.mark.django_db
def test_periodic_job_doesnt_change_seats_taken_for_premium_group(data_fixture):
    user = data_fixture.create_user()
    group = data_fixture.create_group(user=user)
    database = data_fixture.create_database_application(group=group)

    license_object = License.objects.create(license=VALID_TWO_SEAT_LICENSE.decode())
    LicenseUser.objects.create(license=license_object, user=user)

    assert group.seats_taken is None

    PremiumUsageHandler().calculate_per_group_seats_taken()

    group.refresh_from_db()
    assert group.seats_taken is None


@pytest.mark.django_db
def test_periodic_job_doesnt_change_seats_taken_for_free_group(data_fixture):
    user = data_fixture.create_user()
    group = data_fixture.create_group(user=user)
    database = data_fixture.create_database_application(group=group)

    assert group.seats_taken is None

    PremiumUsageHandler().calculate_per_group_seats_taken()

    group.refresh_from_db()
    assert group.seats_taken is None
