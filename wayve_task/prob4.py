"""
Program 4:

Given a start date and end date, calculate the number of days between those two dates. Do consider

leap years.

Example:

sd = 2012,1,1 ed = 2012,2,28 days = 58

sd = 2012,1,1 ed = 2012,3,1 days = 60

sd = 2011,6,30 ed = 2012,6,30 days = 366

sd = 2011,1,1 ed = 2012,8,8 days = 585

sd = 1900,1,1 ed = 1999,12,31 days = 36523
"""

from __future__ import print_function

class UserDate(object):
	"""
	Assumption: The date is provided as a ```string``` in the form '2012,1,1' (yyyy,mm,dd)
	"""
	def __init__(self, d):
		self.year, self.month, self.day = map(lambda x: int(x), d.split(','))

	def is_leap(self):
		if self.year % 100 == 0:
			return True if self.year % 400 == 0 else False
		elif self.year % 4 == 0:
			return True
		else:
			return False

	def months_to_days(self):
		days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]

		return sum(days_in_month[0:self.month]) + 1 if self.is_leap and self.month >= 2 else \
			sum(days_in_month[0:self.month])

	def total_days(self):
		return ((self.year - 1)*365) + self.months_to_days() + self.day

if __name__=="__main__":
	# sd = '2012,1,1'
	# ed = '2012,2,28'

	# sd = '2012,1,1'
	# ed = '2012,3,1'

	sd = '2011,6,3'
	ed = '2012,6,30'
	st_dt = UserDate(sd)
	ed_dt = UserDate(ed)
	print (ed_dt.total_days() - st_dt.total_days())