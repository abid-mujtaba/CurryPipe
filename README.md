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

In the functional programming paradigm this sequence of transformations is
often referred to as a transformation pipeline [[1][transformation-pipelines]].

In Unix the successive transformation of output via a chain of utilities is
carried out via the pipe (`|`) character.

The proposal is to allow Python to do the same:

``` python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

result = numbers | filter(lambda x: x % 2) | map(lambda x: x * x) | reduce(lambda x, y: x * y, 0)

assert result == 225
```

Since this essentially assumes that `filter`, `map`, and `reduce` can be
partially applied (the `reduce` use case is strictly partial application from both ends)
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

This syntax keeps the intent of the original `map`, `filter`, `reduce` while
providing reusable (partially applied) transformations and
a pipe-based syntax which is familiar and more easily grokkable.

### Possible implementation

Replace `map`, `filter`, and `reduce` with a function that
returns different objects based on the presence or absence of an iterable in
the second argument.

If an iterable is passed in the function behaves as is.
Existing code is left completely unimpacted.

If an iterable is **not** passed in the function returns an object that
stores the first argument (the transforming function)
and has `__call__` and `__ror__` implemented to support partial application and piping.

Such an implementation is shown in [piped_map_filter_reduce.py](./piped_map_filter_reduce.py)
with associated [tests](./tests/test_piped_map_filter_reduce.py) showing how
it can be used.

### Existing approaches

#### `toolz`

The [toolz](https://pypi.org/project/toolz/) library implements
curried versions of `map`, `filter`, and `reduce` and
a `toolz.compose` function that can compose functions:

``` python
from toolz import compose
from toolz.curried import map, filter, reduce

numbers = [1, 2, 3, 4, 5, 6]

pick_odd = filter(lambda x: x % 2)
square = map(lambda x: x * x)
product = reduce(lambda x, y: x * y)

transform = compose(product, square, pick_odd)

result = transform(numbers)
```

Notice the reverse order of invocation in the call to `compose()` which is
a little counter-intuitive and reduces readability.
Replacing built-in constructs (`map`, `filter`, `reduce`) with
the library's versions can lead to confusion.

#### `pipe`

The [pipe](https://pypi.org/project/pipe/) library supports the use of
the pipe `|` character but it achieves this by implementing
a large number of new functions:

``` python
from pipe import select, where

sum(range(100) | select(lambda x: x ** 2) | where(lambda x: x < 100))
```

The library does have a `map` (an alias for `select`) but
no explicit `filter` (use `where`) or `reduce`.
The library provides functionality that goes significantly beyond general usage.
It's objective is to provide shell-like functionality, for example providing
`tee`, `tail`, `uniq`, etc.

[transformation-pipelines]: https://freecontent.manning.com/function-pipelines-for-mapping-complex-transformations/
