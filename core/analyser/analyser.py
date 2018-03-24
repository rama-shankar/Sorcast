import pandas as pd
import numpy as np
import config
from core.utilty import util 


def start(args):
	date = util.get_date_from_string(args.date)
	#print(args)
	for exchange in args.exchange:
		#print("(%s)(%s)/(%s)/(%s)/(%s)/(%s)" %(exchange,exchange,exchange,exchange,exchange,exchange))
		_start(exchange, date, args.max, args.range, between=args.between, symbol=args.symbol)	
		#print("(%s)__-(%s)(%s)(%s)\(%s)-__\(%s)"%(exchange,exchange,exchange,exchange,exchange,exchange))

def _start(exchange, date, max, range, **kwargs):
	print("<h4>Result for %s</h4>" %(exchange))	
	_file = config.get("%s_result" %(exchange.lower())) + "//" + date.strftime('%d_%b_%Y') + ".csv"
	if(util.is_file_exist(_file)):
		frame = pd.read_csv( _file,index_col=None, header=0)		
		#frame.set_index('SYMBOL', inplace=True)
		for top in range:
			if(top == -1):
				break;
			printAnalysis(frame, max, top)
		between = kwargs.get('between')
		if between is not None:
			printTopBetween(frame, max, between[0], between[1])
		
		symbol = kwargs.get('symbol')
		if symbol is not None:
			printSelected(frame, symbol)
	else:
		print('Not Have predition for data', date)
		
	
def printAnalysis(frame, max, top):
	if(top == 0):
		printTop(frame, max)
	else:
		printTopUnder(frame, max, top)	
	
def printSelected(frame, _list):
	#df[df['A'].isin([3, 6])]
	qry = frame['SYMBOL'].isin(_list)
	print("<h5>SYMBOL</h5>")
	printFrame(frame[qry])
	print("<h5>SYMBOL</h5>")
	
def printTop(frame, max):
	print("<h5>TOP ERNER</h5>")
	printFrame(frame.nlargest(max, 'DIFF_VALUE').sort_values(['DIFF_VALUE', 'LAST_VALUE'],ascending=False))
	#print("<h5>TOP ERNER</h5>")
	
def printTopUnder(frame, max, top):
	print("<h5>TOP under  %s</h5>" %(top))
	qry1 = frame['LAST_VALUE'] <= top	
	printFrame(frame[qry1].nlargest(max, 'DIFF_VALUE').sort_values(['PREDICTED_SHARE'],ascending=[False]))
	#print("<h5>TOP Under %s</h5>" %(top))
	
def printTopBetween(frame, max, left, right):	
	print("<h5>TOP under  %s-%s</h5>" %(left, right))
	qry1 = (frame['LAST_VALUE'] >= left) & (frame['LAST_VALUE'] <= right)
	printFrame(frame[qry1].nlargest(max, 'DIFF_VALUE').sort_values(['PREDICTED_SHARE'],ascending=[False]))
	#print("<h5>TOP Under %s-%s</h5>" %(left, right))
	
def printFrame(frame):
	frame = frame.set_index('SYMBOL')		
	print(frame)