"""Implement currying and pipes for functional tools."""

from abc import ABC, abstractmethod
from functools import reduce


class MetaCurryPipe:
    """Adding currying and piping to meta-functions (functional tools)."""

    def __init__(self, meta_function, function, *args, **kwargs):
        """Initialize with the meta_function and the function it will use."""
        self.meta_function = meta_function
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __call__(self, iterable):
        """Let the meta_function apply the stored function on the iterable."""
        return self.meta_function(self.function, iterable, *self.args, **self.kwargs)

    def __ror__(self, iterable):
        """If the object is on the rhs of a pipe call the object on the lhs iterable."""
        return self(iterable)

def emap(function, iterable=None):
    """Extended map function that supports currying and pipes."""
    if iterable:
        return map(function, iterable)

    return MetaCurryPipe(map, function)


def efilter(function, iterable=None):
    """Extended filter function that supports currying and pipes."""
    if iterable:
        return filter(function, iterable)

    return MetaCurryPipe(filter, function)


def ereduce(function, iterable=None, initializer=None):
    """Extended reduce function that supports currying and pipes."""
    if iterable:
        return reduce(function, iterable, initializer)

    return MetaCurryPipe(reduce, function, initializer)


class CurryPipe:
    """Adding currying and piping to functions that act over iterables."""

    def __init__(self, function, *args, **kwargs):
        """Initialize with the function to apply and its args and kwargs."""
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __call__(self, iterable):
        return self.function(iterable, *self.args, **self.kwargs)

    def __ror__(self, iterable):
        return self(iterable)


class FunctionCurryPipe(ABC):
    """Object capable of acting as a function, being curried, and working with a pipe."""

    @abstractmethod
    def function(cls):
        """The core (original) function that acts on iterables."""

    def __call__(self, *args, **kwargs):
        """Object called as a function."""
        function = self.function()

        if args:
            if hasattr(args[0], '__iter__'):  # Original functionality
                return function(*args, **kwargs)

        return CurryPipe(function, *args, **kwargs)

    def __ror__(self, iterable):
        """Iterable piped into object."""
        function = self.function()

        return function(iterable)



class ESum(FunctionCurryPipe):
    """Class for esum objects."""

    def function(self):
        return sum


esum = ESum()


class ESorted(FunctionCurryPipe):
    """Class for esorted objects."""

    def function(self):
        return sorted


esorted = ESorted()
