"""Implement currying and pipes for functional tools."""


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
