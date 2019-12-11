#!/usr/bin/env python

import sys

def repeat(s, exclaim):
    """
    Returns the string 's' repeated 3 times.
    If exclaim is true, add exclamation marks.
    """
    result = s * 3
    if exclaim:
        result = result + "!!!"
    return result

def main():
    welcome = "Hello there " + sys.argv[1]
    print(repeat(welcome, True))

    # command line args ar in sys.argv[1], sys.argv[2] ....
    # sys.argv[0] is the script name itself and can be ignored


if __name__ == "__main__":
    main()