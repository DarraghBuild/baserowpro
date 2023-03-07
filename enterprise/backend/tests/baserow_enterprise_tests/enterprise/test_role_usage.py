import pytest
from baserow_premium.license.models import License, LicenseUser
from baserow_premium.usage.handler import PremiumUsageHandler
from baserow_premium_tests.license.test_license_handler import VALID_TWO_SEAT_LICENSE


@pytest.fixture(autouse=True)
def enable_enterprise_and_roles_for_all_tests_here(enable_enterprise, synced_roles):
    pass


VALID_TWO_PREMIUM_SEAT_LICENSE = (
    # id: "2", instance_id: "1"
    b"eyJ2ZXJzaW9uIjogMSwgImlkIjogIjIiLCAidmFsaWRfZnJvbSI6ICIyMDIxLTA4LTI5VDE5OjUzOjM3"
    b"LjA5MjMwMyIsICJ2YWxpZF90aHJvdWdoIjogIjIwMjEtMDktMjlUMTk6NTM6MzcuMDkyMzAzIiwgInBy"
    b"b2R1Y3RfY29kZSI6ICJwcmVtaXVtIiwgInNlYXRzIjogMiwgImlzc3VlZF9vbiI6ICIyMDIxLTA4LTI5"
    b"VDE5OjUzOjM3LjA5MjMwMyIsICJpc3N1ZWRfdG9fZW1haWwiOiAiYnJhbUBiYXNlcm93LmlvIiwgImlz"
    b"c3VlZF90b19uYW1lIjogIkJyYW0iLCAiaW5zdGFuY2VfaWQiOiAiMSJ9.d41tB1kx69gw-9xDrRI0kER"
    b"KDUtR-P6yRM3ufKZ_XRDewVCBAniCLe9-ce7TKabnMedE2cqHjYVLlI66Dfa5oH8fGswnyC16c9ZHlOU"
    b"jQ5CpHTorZm6eyCXaP6MDdhstCNKdDrZns3qvVMAqDpmxS8wmiG9Y6gZjvBGXZWeoCraF1SVcUnFBBlf"
    b"UemfGSQUwPitVlxJ6GWN-hzi7b1GZqWJKDb2YYJ0T30VMJeNO7oi6YHMUOH33041FU79DSET2A2NNEFu"
    b"e-jnCcw5NFpH-zGzBDv1wpR3DFmJa78KwGbj0Kdzim85AUzi1xGRlIyxxTdTkVy2B-08lPaoG8Q62bw="
    b"="
)


@pytest.mark.django_db
def test_periodic_job_updates_group_seat_usage_for_active_enterprise(data_fixture):
    user = data_fixture.create_user()
    user2 = data_fixture.create_user()
    group = data_fixture.create_group(
        custom_permissions=[(user, "ADMIN"), (user2, "VIEWER")]
    )

    assert group.seats_taken is None

    PremiumUsageHandler().calculate_per_group_seats_taken()

    group.refresh_from_db()
    assert group.seats_taken == 1


@pytest.mark.django_db
def test_periodic_job_updates_group_seat_usage_for_active_enterprise_and_premium(
    data_fixture,
):
    user = data_fixture.create_user()
    user2 = data_fixture.create_user()
    group = data_fixture.create_group(
        custom_permissions=[(user, "ADMIN"), (user2, "VIEWER")]
    )
    license_object = License.objects.create(license=VALID_TWO_SEAT_LICENSE.decode())
    LicenseUser.objects.create(license=license_object, user=user)

    assert group.seats_taken is None

    PremiumUsageHandler().calculate_per_group_seats_taken()

    group.refresh_from_db()
    assert group.seats_taken == 1


@pytest.mark.django_db
def test_periodic_job_updates_group_seat_usage_for_active_enterprise_and_premium(
    data_fixture,
):
    user = data_fixture.create_user()
    user2 = data_fixture.create_user()
    group = data_fixture.create_group(
        custom_permissions=[(user, "ADMIN"), (user2, "VIEWER")]
    )
    license_object = License.objects.create(license=VALID_TWO_SEAT_LICENSE.decode())
    LicenseUser.objects.create(license=license_object, user=user)

    assert group.seats_taken is None

    PremiumUsageHandler().calculate_per_group_seats_taken()

    group.refresh_from_db()
    assert group.seats_taken == 1
