from datetime import timedelta

import pytest

from baserow.contrib.database.api.fields.serializers import DurationSerializer


@pytest.mark.parametrize(
    "duration_format,user_input,saved_value",
    [
        ("h:mm", 3660, 3660),
        ("h:mm:ss", 3661, 3661),
        ("h:mm:ss.s", 3661.1, 3661.1),
        ("h:mm:ss.ss", 3661.12, 3661.12),
        ("h:mm:ss.sss", 3661.123, 3661.123),
        # TODO: input 3660.xxx for h:mm
        # TODO: test 3661 should be 3660 if the format is h:mm
    ],
)
def test_duration_serializer_to_internal_value(
    data_fixture, duration_format, user_input, saved_value
):
    """
    Tests that for the Duration Serializer, the value is always serialized as
    seconds for the database for every duration format.
    """

    serializer = DurationSerializer(duration_format=duration_format)

    assert (
        serializer.to_internal_value(serializer.to_internal_value(user_input))
        == saved_value
    )


@pytest.mark.parametrize(
    "duration_format,user_input,returned_value",
    [
        ("h:mm", 3660, 3660),
        ("h:mm:ss", 3661, 3661),
        ("h:mm:ss.s", 3661.1, 3661.1),
        ("h:mm:ss.ss", 3661.12, 3661.12),
        ("h:mm:ss.sss", 3661.123, 3661.123),
    ],
)
def test_duration_serializer_to_representation(
    data_fixture, duration_format, user_input, returned_value
):
    # TODO: check rounding and falsy cases
    """
    Tests that for the Duration Serializer, the representation is returned in
    seconds from the database for every duration format.
    """

    serializer = DurationSerializer(duration_format=duration_format)

    assert serializer.to_representation(timedelta(seconds=user_input)) == returned_value
