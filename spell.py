# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import sys

numbers = {
    0: 'nulo',
    1: 'unu',
    2 :'du',
    3 :'tri',
    4 :'kvar',
    5 :'kvin',
    6 :'ses',
    7 :'sep',
    8 :'ok',
    9 :'naŭ',
    10 :'dek',
    100 :'cent',
    1000: 'mil',
}

fragments = ['mil', 'bil', 'tril', 'kvadril', 'kvintil', 'sekstil', 'septil', 'oktil', 'nonil', 'dekil']
for i, fragment in enumerate(fragments):
    exp = (i + 1) * 6
    numbers[10**exp] = fragment + 'iono'
    exp += 3
    numbers[10**exp] = fragment + 'iardo'

def eo(n):
    if n < 0:
        return 'minus ' + eo(-n)

    result = numbers.get(n)
    if result:
        return result

    for pos in (100, 1000):
        if n < pos:
            high, low = divmod(n, pos // 10)
            result = numbers[pos // 10]
            if low:
                result += ' ' + eo(low)
            if high > 1:
                result = numbers[high] + result
            return result

    exp = 3
    high, low = divmod(n, 1000)
    result = eo(low) if low else ''

    while high:
        high, low = divmod(high, 1000)
        if low:
            part = numbers[10**exp]
            if low > 1:
                part = eo(low) + ' ' + part
                if part.endswith('o'):
                    part += 'j'
            result = part + ' ' + result if result else part
        exp += 3

    return result

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        n = int(arg)
        print('{:13d} {}'.format(n, eo(n)))