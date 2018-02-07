from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import time, datetime
import logging, os, sys
import multiprocessing as mp
from multiprocessing.pool import ThreadPool

class SimpleRegration:	
	_frame = None
	_cframe = None
	_result = []
	def __init__(self, _frame, _cframe):
		self._frame = _frame
		self._cframe = _cframe
	
	def run(self):			
		date = self._cframe['date']		
		_cframe_dict =  self.get_cframe_dict(self._cframe['frame'])		
		pool = ThreadPool(5)
		total = len(_cframe_dict.items())
		
		for i, (symbol, symbol_data) in enumerate(_cframe_dict.items()):
			p = ((i+1) / total) * 100
			result = pool.apply_async(self.run_each, args=(p, date, symbol, symbol_data))
			self._result.append(result.get())
			#if i == 1 :
			#	break
			
		pool.close()
		pool.join()			
		
		return self._result, date
	
	
	def run_each(self, progress, date, symbol, symbol_data):
		crit_a1 = self._frame['SYMBOL'] == symbol
		_frame = self._frame[crit_a1]
		_reg = Reg(_frame, date, symbol, symbol_data)
		result = _reg.run()
		#print(index , sep=' ', end='', flush=True)
		sys.stdout.write("Progress: %d%%   \r" % (progress) )
		sys.stdout.flush()
		return result
	
	def get_cframe_dict(self, _cframe):		
		return _cframe.set_index('SYMBOL').to_dict(orient='index')
		
class Reg:
	_frame = None
	_mframe = None
	_symbol = None
	_reg = LinearRegression()
	def __init__(self, _frame,_date, _symbol, symbol_data):
		self._mframe = _frame
		self._symbol = _symbol
		self._date = _date
		self.symbol_data = symbol_data	
		
	def run(self):		
		trad_result = self.predict_trad_value()
		trad_result['PREDICTED'] = int(trad_result['PREDICTED'])		
		result = self.predict_price_value(trad_result['PREDICTED'])		
		difs =  result['PREDICTED'] - self.symbol_data['CLOSE']
		dict = {
				'SYMBOL': trad_result['SYMBOL'],
				'LAST_VALUE': "%.2f" % self.symbol_data['CLOSE'],
				'PREDICTED_VALUE': "%.2f" % result['PREDICTED'],
				'DIFF_VALUE': "%.2f" % difs,
				'PREDICTED_SHARE':trad_result['PREDICTED'],
			   }
		return dict
	def get_bid_price(self):
		close = self.symbol_data['CLOSE']
		last = self.symbol_data['LAST']
		diff = close - last
		return close + ( ( diff / close ) * 100 )
		
	def predict_trad_value(self):
		self.fit_data(['TIMESTAMP','OPEN', 'CLOSE', 'HIGH', 'TOTTRDQTY'])
		self.train_data('TOTTRDQTY')
		unixtime = int(time.mktime(self._date.timetuple()))		
		q_list = [[unixtime, self.symbol_data['OPEN'], self.symbol_data['CLOSE'], self.symbol_data['HIGH']]]
		result = self.predict(q_list, ['TIMESTAMP', 'OPEN', 'CLOSE', 'HIGH'])
		return result
	
	def predict_price_value(self, trad_value):
		self.fit_data(['TIMESTAMP','OPEN', 'CLOSE', 'TOTTRDQTY'])
		self.train_data('CLOSE')
		unixtime = int(time.mktime(self._date.timetuple()))	
		bid_price = self.get_bid_price()
		q_list = [[unixtime, bid_price, trad_value]]
		result = self.predict(q_list, ['TIMESTAMP', 'OPEN', 'TOTTRDQTY'])
		return result
	
	def fit_data(self, slice):	
		self._frame = self._mframe[slice]
		tm = pd.to_datetime(self._frame['TIMESTAMP'])		
		indexs = tm.values.astype(np.int64) // 10 ** 9		
		self._frame.loc[:,'TIMESTAMP'] =  indexs
		#print(self._frame)

	def train_data(self, label):
		labels = self._frame[label]
		self._frame = self._frame.drop([label],axis=1)
		self._reg.fit(self._frame, labels)
	
	def predict(self, q_list, columns):			
		dd = pd.DataFrame(q_list, columns=columns)		
		predicted_price = self._reg.predict(dd)		
		predicted = predicted_price[0]
		return {'SYMBOL':self._symbol, 'PREDICTED': predicted}