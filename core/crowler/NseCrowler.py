import calendar, datetime, sys
from multiprocessing.pool import ThreadPool

import config as conf
from core.utilty.util import StopWatch
from core.utilty.util import request_and_extract
from core.utilty.util import is_file_exist
from core.utilty.util import prepare_nse_file_name

class NseCrowler:
	
	def __init__(self, start_date=None, end_date=None):
		assert start_date is not None, "start date required"
		assert end_date is not None, "end date required"
		
		self._url =  conf.get('nse_url')
		self.data =  conf.get('nse_data')
		self.start_date, self.end_date = start_date, end_date	
		self.pool = ThreadPool(10)		
		self.counter = 0
	
		
	def load(self):			
		sw = StopWatch()
		start_date, end_date = self.start_date, self.end_date
		
		while(start_date <= end_date):		
			url, fileName = self.prepare_url_and_file_name(start_date)		
			weekday = calendar.day_abbr[start_date.weekday()]			
			file_path_on_disk =  self.data + "\%s" %(fileName) 			
			if weekday != 'Sat' and weekday != 'Sun' and not is_file_exist(file_path_on_disk) :				
				result = self.pool.apply_async(request_and_extract, args=(url, self.data))			
				if result.get() == True:
					self.counter += 1
			start_date += datetime.timedelta(days=1)		
		
		self.pool.close()
		self.pool.join()
		t1 = sw.done()
		print("Total File Loaded %s in %s seconds" %(self.counter, t1))
		
	
	def prepare_url_and_file_name(self, date):	
		year = date.year
		month = calendar.month_abbr[date.month].upper()
		day = date.strftime('%d')
		filename = prepare_nse_file_name(date)
		return self._url % (year, month, filename, 'zip'), filename
	