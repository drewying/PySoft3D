import math
class Vector:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def length(self):
		return self.x * self.x + self.y * self.y + self.z * self.z
	
	def length_sq(self):
		return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

	def normalized(self):
		length = self.length()
		scale = 1.0 / length
		return Vector(self.x * scale, self.y * scale, self.z * scale)

	def __sub__(self, right):
		return Vector(self.x - right.x, self.y - right.y, self.z - right.z)                
	
	def __str__(self):
		return "(" + str(self.y) + "," + str(self.y) + "," + str(self.z) + ")"
	def cross(self, right):
		return Vector(self.y * right.z - self.z * right.y, self.z * right.x - self.x * right.z, self.x * right.y - self.y * right.x)

	def dot(self, right):
		return self.x * right.x + self.y * right.y + self.z * right.z
