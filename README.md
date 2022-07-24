# sugar-cube
A simple process communication library that ensures causal or total ordering between those.

## Classes and inner parts

Every ordering primitive is stored inside its homonimous folder inside
`order/`. Both `PartialWorker`s and `TotalWorker`s have the same class scheme,
as they both have methods for send and receive messages and, also, to
execute an abstract event at their innards. Processes communicate by using 
`Pipes()` in a _full-duplex_ channel.

## How to use the lib?

In order to ease library usage, one can utilize the `read_configs_from(...)`
function from the `parsing/` module to read a configuration file. Its
formatting must follow the primitives shown below.

> #processes \
> 3 \
> #pipes \
> 0 1 \
> 0 2 \
> 1 2

A config file _must_ have a `#processes` line accompanied by a numerical
value stating how many processes will be created, as it also _must_
have a `#pipes` line followed by the processes' numerical IDs in pairs
as those will be used to indexate a `Pipe()` dictionary.

# How to test?

Inside `tests/`, one can execute both `causal` and `total` order unit tests.
The values used for processes' counters in those tests follow the examples
shown in class by the course's professor.
