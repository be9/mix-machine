MEM_SIZE = 4000	# memory size in words

class Memory:
	def __init__(self):
		pass
	
	def set(self, addr, val):
		pass
	
	def get(self, addr):
		pass
	
	def set_range(self, addr_b, addr_e, values):
		pass
	
	def get_range(self, addr_b, addr_e):
		pass
	
	def lock_range(self, addr_b, addr_e):
		pass
	
	def unlock_range(self, addr_b, addr_e):
		pass
	
	def unlock_all(self):
		pass
		
	def fill(self, val):
		pass 