import math
from mpmath import *
from Vector import *

class Matrix:	

	@classmethod
	def zero_matrix(self):
		matrix = Matrix()
		matrix.values = [[0.0, 0.0, 0.0, 0.0],
				 [0.0, 0.0, 0.0, 0.0],
				 [0.0, 0.0, 0.0, 0.0],
				 [0.0, 0.0, 0.0, 0.0]]
		return matrix

	@classmethod	
	def identity_matrix(self):
		matrix = Matrix()
		matrix.values = [[1.0, 0.0, 0.0, 0.0],
				 [0.0, 1.0, 0.0, 0.0],
				 [0.0, 0.0, 1.0, 0.0],
				 [0.0, 0.0, 0.0, 1.0]]
		return matrix
	
	@classmethod
	def translate(self, x, y, z):
		matrix = Matrix.identity_matrix()

		matrix.values[0][3] = x
		matrix.values[1][3] = y
		matrix.values[2][3] = z

		return matrix
	
	@classmethod
	def scale(self, x, y, z):
		matrix = Matrix.zero_matrix()
		matrix.values[0][0] = x
		matrix.values[1][1] = y
		matrix.values[2][2] = z
		matrix.values[3][3] = 0.0  		
	
	@classmethod
	def rotateX(self, angle):
		matrix = Matrix.identity_matrix()
		cosine = math.cos(angle)
		sine = math.sin(angle)
		
		matrix.values[1][1] = cosine
		matrix.values[1][2] = -sine
		matrix.values[2][1] = sine
		matrix.values[2][2] = cosine

		return matrix

	@classmethod
	def rotateY(self, angle):
		matrix = Matrix.identity_matrix()
		cosine = math.cos(angle)
		sine = math.sin(angle)

		matrix.values[0][0] = cosine
		matrix.values[0][2] = sine
		matrix.values[2][0] = -sine
		matrix.values[2][2] = cosine
		
		return matrix

	@classmethod
	def rotateZ(self, angle):
		matrix = Matrix.identity_matrix()
		cosine = math.cos(angle)
		sine = math.sin(angle)	
	
		matrix.values[0][0] = cosine
		matrix.values[0][1] = -sine
		matrix.values[1][0] = sine
		matrix.values[1][1] = cosine

		return matrix

	@classmethod
	def look_at(self, camera_position, camera_target, camera_up):
		n = (camera_position - camera_target).normalized()
		u = (camera_up.cross(n)).normalized()
		v = (n.cross(u)).normalized()

		matrix = Matrix()
		matrix.values = [[u.x, v.x, n.x, -camera_position.x],
				 [u.y, v.y, n.y, -camera_position.y],
				 [u.z, v.z, n.z, -camera_position.z],
				 [0.0, 0.0, 0.0, 1.0]]
		return matrix


	@classmethod
	def perspective(self, fov, aspect_ratio, znear, zfar):
		matrix = Matrix.identity_matrix()
		top = math.tan(fov/2.0) * znear
		right = top * aspect_ratio
		
		matrix.values[0][0] = znear/right
		matrix.values[1][1] = znear/top
		matrix.values[2][2] = -(zfar + znear)/(zfar - znear)
		matrix.values[2][3] = -2.0*zfar*znear/(zfar - znear)
		matrix.values[3][2] = -1.0
		matrix.values[3][3] = 0.0
		
		return matrix

	
	def __mul__(self, matrix):
		return_matrix = Matrix.zero_matrix()
		for i in range(4):
			for j in range(4):
				for k in range(4):
					return_matrix.values[i][j] += self.values[i][k] * matrix.values[k][j]
		return return_matrix

	def transformPoint(self, point):
		x = point.x * self.values[0][0] + point.y * self.values[0][1] + point.z * self.values[0][2] + self.values[0][3]
		y = point.x * self.values[1][0] + point.y * self.values[1][1] + point.z * self.values[1][2] + self.values[1][3]
		z = point.x * self.values[2][0] + point.y * self.values[2][1] + point.z * self.values[2][2] + self.values[2][3]
		t = point.x * self.values[3][0] + point.y * self.values[3][1] + point.z * self.values[3][2] + self.values[3][3]
		
		return Vector(x/t, y/t, z/t)

	def transformVector(self, vector):
		x = vector.x * self.values[0][0] + vector.y * self.values[0][1] + vector.z * self.values[0][2]
		y = vector.x * self.values[1][0] + vector.y * self.values[1][1] + vector.z * self.values[1][2] 
		z = vector.x * self.values[2][0] + vector.y * self.values[2][1] + vector.z * self.values[2][2] 

		return Vector(x, y, z)
		

