class MapError(Exception):
	"""
		Simple error used by the map parser.
	"""
	def __init__(self, message):
		self.message = message
	def __str__(self):
		return repr(self.message)

class MapVersionError(Exception):
	"""
		Simple error to indicate a n
	"""
	def __init__(self, version):
		self.version = version
	def __str__(self):
		return "Invalid map version %d"%self.version