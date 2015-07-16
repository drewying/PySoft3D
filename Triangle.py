class Triangle:
	def __init__(self, p1, p2, p3):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3

	def __mul__(self, matrix):
		return Triangle(matrix.transformPoint(self.p1),
		                matrix.transformPoint(self.p2),
		                matrix.transformPoint(self.p3))

