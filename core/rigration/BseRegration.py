import pandas as pd
import numpy as np
import datetime
from core.utilty.util import get_exchange_file
from core.utilty.util import is_file_exist
from core.rigration.SimpleRegration import SimpleRegration

class BseRegration:
	
	def __init__(self, start_date, end_date):
		self.start_date, self.end_date = start_date, end_date
		self.t_frame_list = []
		self.q_frame_dict = None
		self.q_frame_column = ['SYMBOL', 'OPEN', 'CLOSE', 'HIGH', 'LAST', 'TOTTRDQTY']
		self.rename_dict = {'SC_NAME': 'SYMBOL',  'NO_TRADES':'TOTTRDQTY'}
	
	def start(self):
		t_frame = self.prepare_t_frame()
		q_frame_dict = self.prepare_q_frame_dict()		
		_simpleRegration = SimpleRegration(t_frame, q_frame_dict)
		data = _simpleRegration.run()
		return data	
		
	def prepare_t_frame(self):
		start_date, end_date = self.start_date, self.end_date
		while(start_date <= end_date):
			_file = get_exchange_file('bse', start_date)
			
			if is_file_exist(_file):
				self.add_to_t_frame_list(_file, start_date)
			start_date += datetime.timedelta(days=1)
		
		frame = pd.concat(self.t_frame_list)
		frame.reset_index()		
		frame = frame.rename(columns=self.rename_dict)		
		return frame
		
	def prepare_q_frame_dict(self):
		result = {'date':self.end_date}
		date = self.end_date
		_file = get_exchange_file('bse', date)
		while(is_file_exist(_file) == False):
			date -= datetime.timedelta(days=1)	
			_file = get_exchange_file('bse', date)
			if date == self.start_date:
				break
				
		df = pd.read_csv( _file,index_col=None, header=0)
		df = df.rename(columns=self.rename_dict)				
		result['frame'] = df[self.q_frame_column]
		return result
	
	def add_to_t_frame_list(self, _file, start_date):
		df = pd.read_csv( _file,index_col=None, header=0)
		df['TIMESTAMP'] =  start_date.strftime("%d-%b-%Y")
		self.t_frame_list.append(df)