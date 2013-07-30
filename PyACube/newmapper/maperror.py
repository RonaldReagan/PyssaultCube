class MapError(Exception):
	"""
		Simple error used by the map parser.
	"""
	def __init__(self, message):
		self.message = message
	def __str__(self):
		return repr(self.message)