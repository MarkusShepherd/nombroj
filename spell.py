# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import itertools
import sys

units = ['nulo', 'unu', 'du', 'tri', 'kvar', 'kvin', 'ses', 'sep', 'ok', 'naŭ', 'dek', 'cent']
fragments = ['mil', 'bil', 'tril', 'kvadril', 'kvintil', 'sekstil', 'septil', 'oktil', 'nonil', 'dekil']
highs = ['mil'] + list(itertools.chain.from_iterable((v + 'iono', v + 'iardo') for v in fragments))

def eo(n):
	if n < 0:
		return 'minus ' + eo(-n)

	if n <= 10:
		return units[n]

	if n < 100:
		ten, unit = divmod(n, 10)
		r = units[10]
		if unit:
			r += ' ' + units[unit]
		return r if ten == 1 else units[ten] + r

	if n < 1000:
		hun, ten = divmod(n, 100)
		r = units[11]
		if ten:
			r += ' ' + eo(ten)
		return r if hun == 1 else units[hun] + r

	exp = 0
	high, low = divmod(n, 1000)
	r = eo(low) if low else ''

	while high:
		high, low = divmod(high, 1000)
		if low:
			r = highs[exp] + ('j' if exp and low > 1 else '') + ((' ' + r) if r else '')
			if low > 1:
				r = eo(low) + ' ' + r
		exp += 1

	return r

if __name__ == '__main__':
	for n in sys.argv[1:]:
		n = int(n)
		print('{:10d}: "{}"'.format(n, eo(n)))
