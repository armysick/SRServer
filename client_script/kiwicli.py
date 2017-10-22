import arrow
import sys
import numpy as np
import scipy as sp
import scipy.stats
import requests

class ClientScript:
	collected_measures = []
	log_file = None

	@classmethod
	def main_loop(cls):
		i = 0
		# Limit maximum tries to 200
		while (i < 200):
			for x in range(0,5):
				cls.kiwi_post()
			if cls.test_confidence_interval():
				break
		
		
		mean, lower, upper = cls.mean_confidence_interval(cls.collected_measures)
		print 'Total measures: {}'.format(len(cls.collected_measures))
		print 'Mean : {} || Lower bound : {} || Upper bound : {}'.format(mean, lower, upper)
		if cls.log_file is not None:
			with open(cls.log_file, 'w+') as f:
				f.write('Total measures: {}'.format(len(cls.collected_measures)))
				f.write('Mean : {} || Lower bound : {} || Upper bound : {}'.format(mean, lower, upper))
				f.write(str(cls.collected_measures))
		
	@classmethod
	def kiwi_post(cls, number=10):
		before_request_time = arrow.utcnow()
		r = requests.post('http://145.239.155.5/naturalsum/{}'.format(number))
		after_request_time = arrow.utcnow()
		# Time for the request to complete
		time_difference = after_request_time - before_request_time
		
		cls.collected_measures.append(time_difference.total_seconds())
		

	@classmethod
	def test_confidence_interval(cls):
		media, lim_inf, lim_sup = cls.mean_confidence_interval(cls.collected_measures)
		# Try until 5 % variation from Mean
		if lim_inf < media - 0.05*media:
			return False
		return True
		
	@classmethod
	def mean_confidence_interval(cls, data, confidence=0.95):
		a = 1.0*np.array(data)
		n = len(a)
		m, se = np.mean(a), scipy.stats.sem(a)
		h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
		return m, m-h, m+h
	

if len(sys.argv) > 1:
	ClientScript.log_file = sys.argv[1]
ClientScript.main_loop()