
"""
Documentation Strings (docstring)

The first line should be always a short, concise summary of the object's purpose.
This line should begin with a capital letter and end with a period.

The second line should be blank, wisually separating the summary from 
the rest of the description. The following lines should be one or more
paragraphs describing the object's calling conventions, its side effects, etc.

"""


def my_function():
    """Do nothing, but document it.

    No, really, it doesn't do anything.
    """
    pass


print(my_function.__doc__)


"""
Function annotations are completely optional metadata information
about the types used by user-defined functions.

def f(ham, eggs='eggs'):
    pass
"""


def f(ham: str, eggs: str = 'eggs') -> str:
    print(f.__annotations__)
    print(ham, eggs)
    return ham + ' and ' + eggs


print(f('spam'))
