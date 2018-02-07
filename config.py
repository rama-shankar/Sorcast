import os
import logging

root_path = os.path.dirname(os.path.abspath(__file__))
__config = {
	"exchanges": ['NSE', 'BSE'],
    "nse_url": 'https://www.nseindia.com/content/historical/EQUITIES/%s/%s/%s.%s',
	"nse_file_name": 'cm%s%s%sbhav.csv',
	"nse_data": root_path + '\\DATA\\NSE',
	"nse_result": root_path + '\\RESULT\\NSE',
	"bse_url": 'http://www.bseindia.com/download/BhavCopy/Equity/%s.%s',
	"bse_file_name": 'EQ%s.CSV',
	"bse_data": root_path + '\\DATA\\BSE',
	"bse_result": root_path + '\\RESULT\\BSE'
}
def configure():	
	configure_log()
	
def configure_log():
	logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
	rootLogger = logging.getLogger()
	rootLogger.setLevel(logging.DEBUG)
	fileHandler = logging.FileHandler("{}.log".format("Sorcast"))
	fileHandler.setFormatter(logFormatter)
	rootLogger.addHandler(fileHandler)

	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(logFormatter)
	rootLogger.addHandler(consoleHandler)
	
def get_nsc_file_location():
	print(__config)
	return __config.nse_data;

def get_nsc_result_location():	
	return __config.nse_result;
	
def get(key):
	return __config[key]