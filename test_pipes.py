"""Test the new types in the pipes module."""

import pytest

from pipes import PipedIterator, PipedList, PipedTuple
from pipes import efilter, emap


def test_pipes_in_lists():
    """Test the use of pipes with lists."""
    # GIVEN
    numbers = PipedList([1, 2, 3, 4, 5, 6])

    # WHEN
    odd_squares = numbers | (map, lambda x: x*x) | (filter, lambda x: x % 2)

    # THEN
    assert odd_squares == [1, 9, 25]


def test_pipes_in_generators():
    """Test the use of pipes with generators."""
    # GIVEN
    numbers = PipedIterator([1, 2, 3, 4, 5, 6])

    # WHEN
    odd_squares = numbers | (map, lambda x: x*x) | (filter, lambda x: x % 2)

    assert next(odd_squares) == 1
    assert next(odd_squares) == 9
    assert next(odd_squares) == 25

    with pytest.raises(StopIteration):
        next(odd_squares)


def test_piped_map():
    """Test the use of pipes with maps."""
    # GIVEN
    numbers = [1, 2, 3, 4, 5, 6]

    # WHEN
    odd_squares = numbers | PipedTuple((map, lambda x: x*x)) | PipedTuple((filter, lambda x: x % 2))

    assert next(odd_squares) == 1
    assert next(odd_squares) == 9
    assert next(odd_squares) == 25

    with pytest.raises(StopIteration):
        next(odd_squares)


def test_emap_currying():
    """Test the use of the extended-map (emap) function for currying."""
    # GIVEN
    numbers = [1, 2, 3]
    square = emap(lambda x: x * x)

    # WHEN
    squares = square(numbers)

    # THEN
    assert type(squares) is map

    assert next(squares) == 1
    assert next(squares) == 4
    assert next(squares) == 9

    with pytest.raises(StopIteration):
        next(squares)


def test_emap_pipe():
    """Test the use of the extended-map (emap) with pipes."""
    # GIVEN
    numbers = [1, 2, 3]

    # WHEN
    squares = numbers | emap(lambda x: x * x)

    # THEN
    assert type(squares) is map

    assert next(squares) == 1
    assert next(squares) == 4
    assert next(squares) == 9

    with pytest.raises(StopIteration):
        next(squares)


def test_efilter_currying():
    """Test the use of extended-filter (efilter) with currying."""
    # GIVEN
    numbers = [1, 2, 3, 4, 5, 6]
    pick_odd = efilter(lambda x: x % 2)

    # WHEN
    odds = pick_odd(numbers)

    # THEN
    assert type(odds) is filter

    assert next(odds) == 1
    assert next(odds) == 3
    assert next(odds) == 5

    with pytest.raises(StopIteration):
        next(odds)


def test_efilter_pipe():
    """Test the use of extended-filter (efilter) with pipes."""
    # GIVEN
    numbers = [1, 2, 3, 4, 5, 6]

    # WHEN
    odds = numbers | efilter(lambda x: x % 2)

    # THEN
    assert type(odds) is filter

    assert next(odds) == 1
    assert next(odds) == 3
    assert next(odds) == 5

    with pytest.raises(StopIteration):
        next(odds)

