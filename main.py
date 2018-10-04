import numpy as np
import datetime
from loader import Loader
from payment_process import Payment_process
from clustering import Clustering
import graph_plotting
from graph_plotting import Graph_plotting

class Main:
	
	def __init__(self):
		''' mothefucka'''
		self.l = Loader('data_for_applicants.txt')
		
	def find_salaries(self):
		pp = Payment_process(self.l)
		pp.sort_payments()
		dates_errs, income_errs, all_err = pp.process()
		pp.process_errors(dates_errs, income_errs, all_err)
		
	def clustering(self):
		cl = Clustering(self.l)
		#cl.normalize_payments()
		cl.do_clustering()
		
	def find_salaries2(self):
		pp = Payment_process(self.l)
		pp.process3()
		
	def do_graph_plotting(self):
		gg = Graph_plotting(self.l)
		#gg.monthly_salary_perc()
		gg.height_payment_salary_perc()
		gg.payment_grouped_issalary()
		gg.grouped_payment_perc_issalary()
		
m = Main()
m.find_salaries2()
#m.clustering()
m.do_graph_plotting()