import config
from core.utilty import util 
from core.analyser import analyser

def main():
	start_date, end_date = util.prepareDate()	
	print('Prediction Analysis')
	exchanges = config.get('exchanges') 
	for exchange in exchanges:
		analyser.start(exchange, end_date)
		break
if __name__ == '__main__':
	main()
	