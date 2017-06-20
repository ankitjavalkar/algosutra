"""
Write a function find(input string, search string, start location) that takes three inputs

Input string: the input string

Search string: the substring that one needs to search

Location: the position in input string from where you need to start search

Output:

-1 if search string was not found in start string

Otherwise Position of first occurrence of the search string in input string

Example 1:

Input String = "googly doogly do"

Search string = "oog"

Location = 0

Output = 1

Example 2:

Input String = "googly doogly do"

Search string = "oog"

Location = 2
"""

from __future__ import print_function

if __name__=="__main__":
	ip_str = "googly doogly do"
	sr_str = "oog"
	loc = 0
	print (ip_str.find(sr_str, loc))