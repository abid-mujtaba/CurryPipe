"""Test the new types in the pipes module."""

import pytest

from pipes import efilter, emap, ereduce, esorted, esum


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


def test_ereduce_with_pipe():
    """Test use of ereduce with a pipe."""
    # GIVEN
    numbers = [1, 2, 3, 4]
    initial = 13

    # WHEN
    result = numbers | ereduce(lambda x, y: x + y, initializer=initial)

    # THEN
    assert result == 23


def test_curried_ereduce_withPipe():
    """Test curried ereduce with a pipe."""
    # GIVEN
    numbers = [1, 2, 3, 4]
    initial = 13
    accumulate = ereduce(lambda x, y: x + y, initializer=initial)

    # WHEN
    result = numbers | accumulate

    # THEN
    assert result == 23


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
