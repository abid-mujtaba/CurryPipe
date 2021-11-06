"""Piped versions of sum, sorted, and reversed."""

from abc import ABC, abstractmethod


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


class EReversed(FunctionCurryPipe):
    """Class for ereversed objects."""

    def function(self):
        return reversed


ereversed = EReversed()
