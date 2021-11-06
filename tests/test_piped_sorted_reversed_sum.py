"""Test the piped versions of sum, sorted, and reversed."""

import pytest

from piped_sorted_reversed_sum import ereversed, esorted, esum


def test_esum_with_pipe():
    """Test esum with piped iterable."""
    # GIVEN
    numbers = [1, 2, 3, 4]

    # WHEN
    result = numbers | esum

    # THEN
    assert result == 10


def test_curried_esum_with_start():
    """Test curried esum (extended sum)."""
    # GIVEN
    numbers = [1, 2, 3, 4]
    add = esum(start=13)

    # WHEN
    result = add(numbers)

    # THEN
    assert result == 23


def test_esum_with_pipe_with_start():
    """Test esum with piped iterable."""
    # GIVEN
    numbers = [1, 2, 3, 4]

    # WHEN
    result = numbers | esum(start=13)

    # THEN
    assert result == 23


def test_curried_esum_with_pipe_with_start():
    """Test curried esum with piped iterable."""
    # WHEN
    numbers = [1, 2, 3, 4]
    add = esum(start=13)

    # WHEN
    result = numbers | add

    # THEN
    assert result == 23


def test_esorted_with_pipe():
    """Test esorted with piped iterable."""
    # GIVEN
    numbers = [4, 1, 3, 2]

    # WHEN
    result = numbers | esorted

    # THEN
    assert result == [1, 2, 3, 4]


def test_curried_esorted_with_key():
    """Test curried esorted (extended sorted) with a key specified."""
    # GIVEN
    numbers = [4, 1, 3, 2]
    reverse_sort = esorted(key=lambda x: -x)

    # WHEN
    result = reverse_sort(numbers)

    # THEN
    assert result == [4, 3, 2, 1]


def test_esorted_with_pipe_with_key():
    """Test esorted with piped iterable."""
    # GIVEN
    numbers = [4, 1, 3, 2]

    # WHEN
    result = numbers | esorted(key=lambda x: -x)

    # THEN
    assert result == [4, 3, 2, 1]


def test_curried_esorted_with_pipe_with_key():
    """Test curried esorted with piped iterable."""
    # WHEN
    numbers = [4, 1, 3, 2]
    reverse_sort = esorted(key=lambda x: -x)

    # WHEN
    result = numbers | reverse_sort

    # THEN
    assert result == [4, 3, 2, 1]


def test_ereversed_with_piped_sequence():
    """Test ereversed with piped sequence."""
    # GIVEN
    numbers = [1, 2, 3]

    # WHEN
    result = numbers | ereversed

    # THEN
    assert next(result) == 3
    assert next(result) == 2
    assert next(result) == 1

    with pytest.raises(StopIteration):
        next(result)


def test_invalid_ereversed_with_piped_generator():
    """Test that ereversed failed when a generator is piped in."""
    # GIVEN
    numbers = (x for x in range(3))

    # THEN
    with pytest.raises(TypeError, match="'generator' object is not reversible"):
        # WHEN
        numbers | ereversed
