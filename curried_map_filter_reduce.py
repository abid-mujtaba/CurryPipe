"""Curried versions of map, filter, and reduce."""

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


def ereduce(function, *args):
    """Extended reduce function that supports currying and pipes."""
    if args and hasattr(args[0], '__iter__'):
        return reduce(function, *args)

    return MetaCurryPipe(reduce, function, *args)
