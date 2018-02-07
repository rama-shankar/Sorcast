import logging
from core.crowler.NseCrowler import NseCrowler 
from core.crowler.BseCrowler import BseCrowler 

def load(exchange, start_date, end_date):	
	logging.info("Loading Data from {0} to {1}".format(start_date, end_date))
	if exchange == 'NSE':
		cl = NseCrowler(start_date, end_date)
	elif exchange == 'BSE':
		cl = BseCrowler(start_date, end_date)
	cl.load()	

