"""
Problem 2:

You are given an array of n+2 elements. All elements of the array are in range 1 to n. And all

elements occur once except two numbers which occur twice. Find the two repeating numbers.

For example, array = {4, 2, 4, 5, 2, 3, 1} and n = 5

The above array has n + 2 = 7 elements with all elements occurring once except 2 and 4 which occur

twice. So the output should be 4 2.
"""

from __future__ import print_function

def find_duplicate(array):
	dlist = []
	for i, elem in enumerate(array):
		if elem in array[0:i]:
			dlist.append(elem)
	print(*dlist)

if __name__=="__main__":
	array = [4, 2, 4, 5, 2, 3, 1]
	find_duplicate(array)