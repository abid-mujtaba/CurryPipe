# Python: Proposal for piping iterables

`map`, `filter`, and `reduce` are powerful tools in the functional programming paradigm.
They allow us to construct pipelines of data transformations.

## A Toy Example

Let us consider a toy example.

1. Start with a list of numbers (iterable): `[1, 2, 3, 4, 5, 6]`.
1. Filter out the even numbers.
1. Convert the remaining numbers to their squares.
1. Multiply all of the numbers together.

### Current Approach

If done in one go:

``` python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

result = reduce(
    lambda x, y: x * y, map(lambda z: z * z, filter(lambda n: n % 2, numbers)), 1
)

assert result == 225
```

(the `1` at the end of the `reduce()` is used redundantly for illustrative purposes).

Not very readable.
One should split this up to improve readability.

``` python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

odd_numbers = filter(lambda x: x % 2, numbers)
squared_numbers = map(lambda x: x * x, odd_numbers)

result = reduce(lambda x, y: x * y, squared_numbers, 1)

assert result == 225
```

### Proposed approach

In the functional programming paradimg this sequence of tranformations is
often referred to as a transformation pipeline [1][transformation-pipelines].

[transformation-pipelines]: https://freecontent.manning.com/function-pipelines-for-mapping-complex-transformations/

In Unix the successive tranformation of output via a chain of utilities is
carried out via the pipe (`|`) character.

The proposal is to allow Python to do the same:

``` python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

result = numbers | filter(lambda x: x % 2) | map(lambda x: x * x) | reduce(lambda x, y: x * y, 0)

assert result == 225
```

Since this essentially assumes that `filter`, `map`, and `reduce` can be curried
(the `reduce` use case is strictly currying from both ends)
an alternate and more readable implementation would be:

``` python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

pick_odd = filter(lambda x: x % 2)
square = map(lambda x: x * x)
product = reduce(lambda x, y: x * y, 1)

result = numbers | pick_odd | square | product

assert result == 225
```

### Possible implementation

Replace `map`, `filter`, and `reduce` with a function that
returns different objects based on the presence or absence of an iterable in
the second argument.

If an iterable is passed in the function behaves as is.
Existing code is left completely unimpacted.

If an iterable is **not** passed in the function returns an object that
stores the first argument (the transforming function)
and has `__call__` and `__ror__` implemented to support currying and piping.

Such an implementation is shown in [curried_map_filter_reduce.py](./curried_map_filter_reduce.py)
with associated [tests](./tests/test_curried_map_filter_reduce.py) showing how
it can be used.
