import datetime

MODULE = "2"
TERMINAL_NAME = "alibaba"


def now_time():
	"""

	Returns:
	"""
	curr_time = datetime.datetime.now()
	return curr_time.strftime("%Y-%m-%d")


def phone(module):
	"""

	Args:
		module: 模式

	Returns:
	"""
	if module == "1":
		return "188520011314"
	else:
		return "0532-81910921"
