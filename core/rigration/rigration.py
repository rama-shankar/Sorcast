from core.utilty.util import StopWatch
from core.rigration.NseRegration import NseRegration
from core.rigration.BseRegration import BseRegration

def start(exchange, start_date, end_date):
	print("starting regration for %s from = %s To = %s" %(exchange, start_date, end_date))
	sw = StopWatch()
	reg = None
	if exchange == 'NSE':
		reg = NseRegration(start_date, end_date)
	elif exchange == 'BSE':
		reg = BseRegration(start_date, end_date)
	result, date = reg.start()
	time_taken = sw.done()
	print("Ending regration for %s from = %s To = %s in %s seconds" %(exchange, start_date, end_date, time_taken))
	return result, date