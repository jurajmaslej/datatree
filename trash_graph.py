def monthly(self):
		"""
		determine if payment runs monthly
		"""
		pass
	
	def euqal_sum(self):
		"""
		salary should be approximately equal through whole year, maybe some exception for benefits
		"""
		pass
	
	def create_nodes(self):
		for acc in self.accounts_set:
			self.accounts_dict[acc] = self.Node(acc)
			
	def fill_nodes(self):
		for i in self.edges_dict.values():
			
			
	def duplicity(self):
		from_to = dict()
		self.accounts_set = dict()
		for line in self.data:
			if 8000 < line[2] < 70000:
				key = line[1] + '#' + line[3]
				from_to[line[1] + '#' + line[3]] = 0
		print(len(from_to))


############### STATISTICS #######

				#income_norm = np.array(self.normalize_data(income_list))
				#print(income_norm)
				#income_norm_mean = np.mean(income_norm)
				#err = sum(np.absolute(income_norm - income_norm_mean))/len(income_norm)
#################