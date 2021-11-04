"""Test the new types in the pipes module."""

import pytest

from pipes import efilter, emap, ereduce


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


def test_emap_pipe_with_curry():
    """First create a curried emap and then use it with a pipe."""
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


def test_efilter_pipe_with_curry():
    """First created a curried efilter and then use it with a pipe."""
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


def test_currried_efilter_and_emap():
    """Test combination of curried efilter and emap."""
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


def test_curried_ereduce():
    """Test curried ereduce."""
    # GIVEN
    numbers = [1, 2, 3, 4]
    initial = 13
    accumulate = ereduce(lambda x, y: x + y, initializer=initial)

    # WHEN
    result = accumulate(numbers)

    # THEN
    assert result == 23
