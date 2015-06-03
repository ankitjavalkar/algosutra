########################################
# Euler Problem No. 6
# The sum of the squares of the first ten natural numbers is,

# 12 + 22 + ... + 102 = 385
# The square of the sum of the first ten natural numbers is,

# (1 + 2 + ... + 10)^2 = 552 = 3025
# Hence the difference between the sum of the squares of the first ten natural
#  numbers and the square of the sum is 3025 - 385 = 2640.

# Find the difference between the sum of the squares of the first one hundred
#  natural numbers and the square of the sum.
########################################
# Language: Pyhton 2.7
########################################


def get_sum_square_diff(n):
    return (sum(a+1 for a in xrange(n)))**2 - sum((a+1)**2 for a in xrange(n))

if __name__ == '__main__':
    print "Sum square difference of 20 natural nos.", get_sum_square_diff(20)
