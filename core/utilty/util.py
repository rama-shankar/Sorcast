import calendar, datetime
import csv, os
import config as conf
import time
import requests, zipfile, io


def prepareDate():
	end_date = datetime.date.today()
	cyear = end_date.year
	start_date = datetime.datetime(cyear - 3, 1,1).date()	
	#end_date = datetime.datetime(cyear - 3, 1,31).date()	
	return start_date, end_date
	
def get_date_from_string(date_string):
	if date_string is not None: 
		return datetime.datetime.strptime(date_string, "%Y-%m-%d")
	return datetime.date.today()
	
def prepare_nse_file_name(date):
	year = date.year
	month = calendar.month_abbr[date.month].upper()
	day = date.strftime('%d')
	filename = conf.get('nse_file_name') % (day, month, year)
	return filename
	
def prepare_bse_file_name(date):
	date_string = date.strftime("%d%m%y")
	filename = conf.get('bse_file_name') % (date_string)
	return filename
	
def write_result(exchange, _result, date):
	keys = _result[0].keys()	
	filename = conf.get("%s_result" %(exchange.lower())) + "/" + date.strftime('%d_%b_%Y') + ".csv"	
	with open(filename, 'w' , newline='') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(_result)
	

	
def is_file_exist(_file):	
	if not os.path.isfile(_file): 
		return False
	return True


def request_and_extract(url, data_folder):
	s = requests.Session()
	s.headers.update({'referer':'https://www.nseindia.com/'})
	r = s.get(url)
	if r.status_code == 200 and is_valid_content(r.headers['Content-Type']):
		z = zipfile.ZipFile(io.BytesIO(r.content))
		z.extractall(data_folder)
		return True
	return False
	
def is_valid_content(content_type):
	valid_list = ['application/zip', 'application/x-zip-compressed']
	status = content_type in valid_list	
	return status
	
def get_exchange_file(exchange, date):
	base = conf.get('%s_data' % (exchange))
	if exchange == 'nse':
		return base + "/" + prepare_nse_file_name(date)
	if exchange == 'bse':
		return base + "/" + prepare_bse_file_name(date)
	
class StopWatch:
	def __init__(self):
		self.start = time.time()
	
	def done(self):
		return str(int(time.time() - self.start))
		