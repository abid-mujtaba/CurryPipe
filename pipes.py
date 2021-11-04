"""
Implement pipes for sequences and iterators.

Simply importing this module will patch sequences and iterators to support pipes.
"""

from typing import Any, Tuple

class PipedList(list):
    """Sub-class list to add pipes."""

    def __or__(self, rhs: Tuple[Any, Any]):
        """Apply a piped transformation to a list."""
        meta_function, function = rhs

        return PipedList(meta_function(function, self))


class PipedIterator():
    """Custom Generator class which supports pipes."""
    def __init__(self, iterator):
        """Initiate with an iterator."""
        self._iterator = iter(iterator)  # Supports both iterables and iterators

    def __iter__(self):
        """Iterators are also iterables."""
        return self

    def __next__(self):
        """Return the next value."""
        return next(self._iterator)

    def __or__(self, rhs: Tuple[any, any]):
        """Apply a piped transforation to the iterator."""
        meta_function, function = rhs

        return PipedIterator(meta_function(function, self))


class PipedTuple(tuple):
    """A sub-class of tuple that supports piping."""

    def __ror__(self, iterable):
        """Right-sided or to implement pipes."""
        if len(self) == 2 and callable(self[0]) and callable(self[1]):
            meta_function, function = self

            return meta_function(function, iterable)

        return NotImplemented


class EMap:
    """Extended Map class supporting currying and pipes."""

    def __init__(self, function):
        """Initialize with the function to be applied."""
        self.function = function

    def __call__(self, iterable) -> Any:
        return map(self.function, iterable)

    def __ror__(self, iterable):
        return self(iterable)


class CurryPipe:
    """Meta object capable of currying and supporting pipes."""

    def __init__(self, meta_function, function):
        """Initialize with the meta_function and the function it will use."""
        self.meta_function = meta_function
        self.function = function

    def __call__(self, iterable):
        """Let the meta_function apply the stored function on the iterable."""
        return self.meta_function(self.function, iterable)

    def __ror__(self, iterable):
        """If the object is on the rhs of a pipe call the object on the lhs iterable."""
        return self(iterable)


def emap(function, iterable=None):
    """Extended map function that supports currying and pipes."""
    if iterable:
        return map(function, iterable)

    return CurryPipe(map, function)


def efilter(function, iterable=None):
    """Extended filter function that supports currying and pipes."""
    if iterable:
        return filter(function, iterable)

    return CurryPipe(filter, function)
