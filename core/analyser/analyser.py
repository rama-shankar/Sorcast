import pandas as pd
import numpy as np
import config
from core.utilty import util 

max = 5

def start(exchange, date):
	_file = config.get("%s_result" %(exchange.lower())) + "\\" + date.strftime('%d_%b_%Y') + ".csv"
	if(util.is_file_exist(_file)):
		printAnalysis(_file)
	else:
		print('Not Have predition for data', date)
		
	
def printAnalysis(_file):
	frame = pd.read_csv( _file,index_col=None, header=0)
	printTop(frame)
	printTopUnder100(frame)
	
	
def printTop(frame):
	print("------------TOP ERNER ----------------")
	print(frame.nlargest(max, 'DIFF_VALUE'))
	print("------------//TOP ERNER//----------------")
	
def printTopUnder100(frame):
	print("------------TOP printTopUnder100----------------")
	print(frame[frame['LAST_VALUE']<=100].nlargest(max, 'DIFF_VALUE'))
	print("------------//TOP printTopUnder100//----------------")
	
def printTopUnder200(frame):
	print("------------TOP printTopUnder200----------------")
	print(frame[frame['LAST_VALUE']<=200].nlargest(max, 'DIFF_VALUE'))
	print("------------//TOP printTopUnder200//----------------")

def printTopUnder300(frame):
	print("------------TOP printTopUnder300----------------")
	print(frame[frame['LAST_VALUE']<=200].nlargest(max, 'DIFF_VALUE'))
	print("------------//TOP printTopUnder300//----------------")