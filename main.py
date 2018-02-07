import config
from core.utilty import util 
from core.crowler import crowler
from core.rigration import rigration

def is_predicted (exchange, end_date):
	filename = config.get("%s_result" %(exchange.lower())) + "\\" + end_date.strftime('%d_%b_%Y') + ".csv"
	return util.is_file_exist(filename)
	
def main():	
	config.configure()
	start_date, end_date = util.prepareDate()
	print("Started program from = %s - To = %s" %(start_date, end_date))	
	exchanges = config.get('exchanges') 
	for exchange in exchanges:
		if(is_predicted(exchange, end_date)):
			print('Allready Predicted for ', exchange)
			continue
		#crowler.load(exchange, start_date, end_date)
		result, date = rigration.start(exchange, start_date, end_date)
		util.write_result(exchange, result, date)	
    
if __name__ == '__main__':
	main()
	
