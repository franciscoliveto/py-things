import math
import sys

def input_number(prompt):
    sn = input(prompt)
    if sn.isnumeric():
        return int(sn)
    try:
        n = float(sn)
    except ValueError:
        raise
    return n


try:
    x = input_number('Enter number x: ')
except ValueError:
    print('not a valid number')
    sys.exit(1)
try:
    y = input_number('Enter number y: ')
except ValueError:
    print('not a valid number')
    sys.exit(1)

power = x**y
log = math.log2(x)
print('x**y = %f' % power)
print('log2(x) = %f' % log)
