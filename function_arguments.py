"""
Defining Functions
"""


def fibonacci(n):
    """
    Print a Fibonacci series up to n.
    """
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()


fibonacci(2000)

"""
Default Argument Values
"""
i = 5


def f1(arg=i):
    print(arg)


i = 6
f1()


def f(a, L=[]):
    L.append(a)
    return L


def foo(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L


foo(1)
foo(2)
foo(3)

"""
Keyword Arguments
"""


def parrot(arg1, arg2='value2', arg3='value3'):
    print(arg1)
    print(arg2)
    print(arg3)


parrot(10)          # 1 positional argument
parrot(arg1=43)     # 1 keyword argument
parrot(arg1=2000, arg3='new value')  # 2 keyword arguments
parrot(arg3='value', arg1=400)  # 2 keyword arguments
parrot(1000, 'value 2', 'value 3')  # 3 positional arguments
parrot(3000, arg3='value 3')  # 1 positional, 1 keyword

"""
Illegal calls

parrot() # required argument missing
parrot(arg1=3, 'non-value') # non-keyword argument after a keyword argument
parrot(1000, arg1=2000) # duplicate value for the same argument
parrot(unknown_keyword='who are you?') # unknown keyword argument
"""


def foo_keywords(formal='formal keyword argument', **keywords):
    print(formal)
    for kw in keywords:
        print(kw, ":", keywords[kw])


foo_keywords(formal='formal value', arg1=32, arg2='value 2')


def cheeseshop(kind, *arguments, **keywords):
    print(kind)
    for arg in arguments:
        print(arg)
    for kw in keywords:
        print(kw, ':', keywords[kw])


cheeseshop(29999, 'argument 1', 'argument 2',
           shopkeeper='Michael Pain',
           client='John Cleese',
           sketch='Cheese Shop Sketch')


def foo_args_keywords(name, last_name, *args, **kwargs):
    print(name)
    print(last_name)
    for a in args:
        print(a)
    for kw in kwargs:
        print(kw, ':', kwargs[kw])


foo_args_keywords('John', 'Wick', age=3)


"""Arbitrary Argument List"""


def arbitrary_arguments(name, last_name, *args, sep=' '):
    print(name)
    print(last_name)
    for a in args:
        print(a, end=sep)
    print()


arbitrary_arguments('John', 'Wick', 52, 'USA', 'Killer', sep='-')


def parrot2(voltage, state='a stiff', action='voom'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.", end=' ')
    print("E's", state, "!")


d = {"voltage": "four millon", "state": "bleedin' demised", "action": "VOOM"}
parrot2(**d)
