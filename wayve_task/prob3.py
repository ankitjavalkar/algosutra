"""
Problem 3:

Write a program to remove duplicate elements in an array.

Example:

Enter array size : 5

Enter 5 array element : 11 13 11 12 13

Original array is : 11 13 11 12 13

New array is : 11 13 12
"""

from __future__ import print_function

def remove_duplicate(array):
	unique_list = []
	for i in array:
		if i not in unique_list:
			unique_list.append(i)

	print(*unique_list)

def remove_duplicate_with_set(array):
	print(*set(array))

if __name__=="__main__":
	array = [11, 13, 11, 12, 13]
	remove_duplicate(array)
	remove_duplicate_with_set(array)