import config
from core.utilty import util 
from core.analyser import analyser
import sys, argparse

def main():
	parser = argparse.ArgumentParser()	
	
	parser.add_argument('--date', '-d',required=True, help='Date of the prediction')
	
	parser.add_argument('--max', '-m', default=10, type=int, help='Number of rows')
	
	parser.add_argument('--exchange', '-e', default=['NSE', 'BSE'],  nargs='+')
	
	parser.add_argument('--range', '-r', default=[-1],  nargs='+' ,  type=int)
	
	parser.add_argument('--between', '-b', nargs=2,  type=int)
	
	parser.add_argument('--symbol', '-s', nargs='+')
	
	args = parser.parse_args()
	
	analyser.start(args)	
		
if __name__ == '__main__':
	main()
