
class Vector:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def length(self):
		return math.sqrt(x * x + y * y + z * z)
