from maybe import Maybe
from numbers import Number
from math import sqrt
from typing import Any

##################
# STRING EXAMPLE #
##################

result, err = (
    Maybe("Hello, World")  # Inital value of "Hello, World"
    .bind(str.upper)  # Apply upper to string
    .bind(str.split, ",")  # Apply split to string
    .bind(lambda x: ", ".join(x))  # Apply lambda to join split string
    .resolve_as(str)  # Resolve the value as string type
)

# Print the result if success else any error that occurs
print("String example:", result or err)

# The resolve type can be set to any to prevent type casting
result, err = Maybe("Another string").bind(len).resolve_as(Any)

print("Any example type:", type(result) or err)

###################
# NUMERIC EXAMPLE #
###################


# Define a function to use
def add(x: Number, y: Number) -> Number:
    return x + y


result, err = (
    Maybe(5)
    .bind(add, 5)  # Fuctions that need an extra argument can be done like this
    .bind(lambda x: add(x, 5))  # Or like this
    .bind(sqrt)
    .bind(pow, 4)
    .resolve_as(float)
)

print("Numeric example:", result or err)

################
# LIST EXAMPLE #
################

result, err = (
    Maybe([i + 1 for i in range(10)])
    .bind(lambda x: map(sqrt, x))
    .bind(sum)
    .resolve_as(float)
)
print("List example:", result or err)

###########################
# ERROR CATCHING EXAMPLES #
###########################

# This will raise a ZeroDivisionError
result, err = Maybe(5).bind(lambda x: x / 0).resolve_as(float)

# Catch the error
if err:
    print("An error has been caught and handled:", err)

# This will raise an exception when casting to int
result, err = Maybe("hello").resolve_as(int)

# Onelineer to print result or handle the error
print("Result:", result) if result else print("Error:", err)
