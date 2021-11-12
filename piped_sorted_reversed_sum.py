"""Piped versions of sum, sorted, and reversed."""

from abc import ABC, abstractmethod


class PartialPipe:
    """Adding partial application and piping to functions that act over iterables."""

    def __init__(self, function, *args, **kwargs):
        """Initialize with the function to apply and its args and kwargs."""
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __call__(self, iterable, *args, **kwargs):
        updated_kwargs = {**self.kwargs, **kwargs}
        return self.function(iterable, *self.args, *args, **updated_kwargs)

    def __ror__(self, iterable):
        return self(iterable)


class FunctionPartialPipe(ABC):
    """Act as a function, allow partial application, and piping."""

    @property
    @abstractmethod
    def function(cls):
        """The core (original) function that acts on iterables."""

    def __call__(self, *args, **kwargs):
        """Object called as a function."""
        if args:
            if hasattr(args[0], '__iter__'):  # Original functionality
                return self.function(*args, **kwargs)

        return PartialPipe(self.function, *args, **kwargs)

    def __ror__(self, iterable):
        """Iterable piped into object."""
        return self.function(iterable)



class ESum(FunctionPartialPipe):
    """Class for esum objects."""

    @property
    def function(self):
        return sum


esum = ESum()


class ESorted(FunctionPartialPipe):
    """Class for esorted objects."""

    @property
    def function(self):
        return sorted


esorted = ESorted()


class EReversed(FunctionPartialPipe):
    """Class for ereversed objects."""

    @property
    def function(self):
        return reversed


ereversed = EReversed()
