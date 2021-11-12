"""Test the piped versions of map, filter, reduce."""

import pytest

from piped_map_filter_reduce import emap, efilter, ereduce


def test_emap_partial_application():
    """Test the use of the extended-map (emap) function for partial application."""
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


def test_emap_pipe_with_partial_application():
    """First create a partially applied emap and then use it with a pipe."""
    # GIVEN
    numbers = [1, 2, 3]
    square = emap(lambda x: x * x)

    # WHEN
    squares = numbers | square

    # THEN
    assert type(squares) is map

    assert next(squares) == 1
    assert next(squares) == 4
    assert next(squares) == 9

    with pytest.raises(StopIteration):
        next(squares)


def test_efilter_partial_application():
    """Test the use of extended-filter (efilter) with partial application."""
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


def test_efilter_pipe_with_partial_application():
    """First created a partially applied efilter and then use it with a pipe."""
    # GIVEN
    numbers = [1, 2, 3, 4, 5, 6]
    pick_odd = efilter(lambda x: x % 2)

    # WHEN
    odds = numbers | pick_odd

    # THEN
    assert type(odds) is filter

    assert next(odds) == 1
    assert next(odds) == 3
    assert next(odds) == 5

    with pytest.raises(StopIteration):
        next(odds)


def test_efilter_and_emap():
    """Test combination of efilter and emap."""
    # GIVEN
    numbers = [1, 2, 3, 4, 5, 6]

    # WHEN
    odd_squares = numbers | emap(lambda x: x*x) | efilter(lambda x: x % 2)

    # THEN
    assert type(odd_squares) is filter

    assert next(odd_squares) == 1
    assert next(odd_squares) == 9
    assert next(odd_squares) == 25

    with pytest.raises(StopIteration):
        next(odd_squares)


def test_emap_and_efilter():
    """Test combination of emap and efilter."""
    # GIVEN
    numbers = [1, 2, 3, 4, 5, 6]

    # WHEN
    odd_squares = numbers | efilter(lambda x: x % 2) | emap(lambda x: x * x)

    # THEN
    assert type(odd_squares) is map

    assert next(odd_squares) == 1
    assert next(odd_squares) == 9
    assert next(odd_squares) == 25

    with pytest.raises(StopIteration):
        next(odd_squares)


def test_partially_applied_efilter_and_emap():
    """Test combination of partial applied efilter and emap."""
    # GIVEN
    numbers = [1, 2, 3, 4, 5, 6]
    square = emap(lambda x: x * x)
    pick_odd = efilter(lambda x: x % 2)

    # WHEN
    odd_squares = numbers | square | pick_odd

    # THEN
    assert type(odd_squares) is filter

    assert next(odd_squares) == 1
    assert next(odd_squares) == 9
    assert next(odd_squares) == 25

    with pytest.raises(StopIteration):
        next(odd_squares)


def test_emap_and_efilter():
    """Test combination of emap and efilter."""
    # GIVEN
    numbers = [1, 2, 3, 4, 5, 6]
    square = emap(lambda x: x * x)
    pick_odd = efilter(lambda x: x % 2)

    # WHEN
    odd_squares = numbers | pick_odd | square

    # THEN
    assert type(odd_squares) is map

    assert next(odd_squares) == 1
    assert next(odd_squares) == 9
    assert next(odd_squares) == 25

    with pytest.raises(StopIteration):
        next(odd_squares)


def test_partially_applied_ereduce():
    """Test partially applied ereduce."""
    # GIVEN
    numbers = [1, 2, 3, 4]
    initial = 13
    accumulate = ereduce(lambda x, y: x + y, initial)

    # WHEN
    result = accumulate(numbers)

    # THEN
    assert result == 23


def test_ereduce_with_pipe():
    """Test use of ereduce with a pipe."""
    # GIVEN
    numbers = [1, 2, 3, 4]
    initial = 13

    # WHEN
    result = numbers | ereduce(lambda x, y: x + y, initial)

    # THEN
    assert result == 23


def test_partially_applied_ereduce_withPipe():
    """Test partially applied ereduce with a pipe."""
    # GIVEN
    numbers = [1, 2, 3, 4]
    initial = 13
    accumulate = ereduce(lambda x, y: x + y, initial)

    # WHEN
    result = numbers | accumulate

    # THEN
    assert result == 23
