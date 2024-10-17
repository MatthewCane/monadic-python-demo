from typing import TypeVar, Any, Callable


class Maybe:
    T = TypeVar("T")

    def __init__(self, value: T):
        """A functor with additional Pythonic features and error handling.

        Instanciated with an initial internal state which is then operated
        on using the `bind()` method and returned with the `resolve_as()` method.

        Examples:
            Gets the square root of 5 and returns the result as
            `result` and any exceptions that occur as `err`:
            `result, err = Maybe(5).bind(sqrt).resolve_as(int)`

        """
        self.value = value

    def bind(self, func: Callable, *args, **kwargs):
        """Performs the func on the internal state.

        Returns a new instance of Maybe with the func
        having been run with the internal state as the
        first argument.

        Optionally takes args and kwargs wich will be
        passed as additional arguments to func.
        """
        # If the contents of value is an exception an error
        # has occurred further up the chain. In this case,
        # just pass the exception back down.
        if isinstance(self.value, Exception):
            return Maybe(self.value)

        # In a try-except block to catch exceptions, call
        # the passed function with the current state and
        # any additional args. No matter the result, return
        # a new Maybe with the result or caught exception.
        try:
            return Maybe(func(self.value, *args, **kwargs))
        except Exception as e:
            return Maybe(e)

    def resolve_as(self, return_type: T) -> tuple[T | None, Exception | None]:
        """Resolve the value of the internal state.

        Returns a tuple in two possible states:
            (value, None) if in success state
            (None, Exception) if in error state

        Will optionally cast the value to return_type
        if the type is not Any or None.
        """
        # If the internal state is an exception, return
        # the error state
        if isinstance(self.value, Exception):
            return (None, self.value)

        # If the value is not an error, try to cast self.value
        # to the given type if the type argument is not
        # typing.Any or not passed at all (None)
        if return_type not in [Any, None]:
            try:
                self.value = return_type(self.value)
            # If the cast fails, return the error state
            # with the exception
            except Exception as e:
                return (None, e)

        # Return the success state
        return (self.value, None)
