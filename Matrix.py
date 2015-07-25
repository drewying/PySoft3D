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
	def look_at_lh(self, camera_position, camera_target, camera_up):
		zaxis = (camera_target - camera_position).normalized()
		xaxis = camera_up.cross(zaxis).normalized()
		yaxis = zaxis.cross(xaxis)
		
		matrix = Matrix()
		matrix.values = [[xaxis.x, yaxis.x, zaxis.x, -xaxis.x],
				 [xaxis.y, yaxis.y, zaxis.y, -yaxis.y],
				 [xaxis.z, yaxis.z, zaxis.z, -zaxis.z],
				 [xaxis.dot(camera_position) * -1, yaxis.dot(camera_position) * -1, zaxis.dot(camera_position) * -1, 1.0]]
		return matrix

	@classmethod
	def look_at_rh(self, camera_position, camera_target, camera_up):
		zaxis = (camera_position - camera_target).normalized()
		xaxis = camera_up.cross(zaxis).normalized()
		yaxis = zaxis.cross(xaxis)
		
		matrix = Matrix()
		matrix.values = [[xaxis.x, yaxis.x, zaxis.x, -xaxis.x],
				 [xaxis.y, yaxis.y, zaxis.y, -yaxis.y],
				 [xaxis.z, yaxis.z, zaxis.z, -zaxis.z],
				 [xaxis.dot(camera_position) * -1, yaxis.dot(camera_position) * -1, zaxis.dot(camera_position) * -1, 1.0]]
		return matrix

	@classmethod
	def perspective_fov_lh(self, fov, aspect_ratio, znear, zfar):
		matrix = Matrix()
		height = cot(fov/2.0)
		width = height * aspect_ratio
		
		matrix.values = [[width, 0.0, 0.0, 0.0],
				 [0.0, height, 0.0, 0.0],
				 [0.0, 0.0, zfar/(zfar-znear), 1.0],
				 [0.0, 0.0, -znear*zfar/(zfar-znear), 0.0]]
		return matrix

	@classmethod
	def perspective_fov_rh(self, fov, aspect_ratio, znear, zfar):
		matrix = Matrix()
		height = cot(fov/2.0)
		width = height * aspect_ratio
		
		matrix.values = [[width, 0.0, 0.0, 0.0],
				 [0.0, height, 0.0, 0.0],
				 [0.0, 0.0, zfar/(znear-zfar), -1.0],
				 [0.0, 0.0, znear*zfar/(znear-zfar), 0.0]]
		return matrix

	@classmethod
	def perspective_rh(self, width, height, znear, zfar):
		matrix = Matrix()
		
		matrix.values = [[2.0 * znear/width, 0.0, 0.0, 0.0],
				 [0.0, 2.0*znear/height, 0.0, 0.0],
				 [0.0, 0.0, zfar/(znear-zfar), -1.0],
				 [0.0, 0.0, znear*zfar/(znear-zfar), 0.0]]
		return matrix

	@classmethod
	def perspective_lh(self, width, height, znear, zfar):
		matrix = Matrix()
		
		matrix.values = [[2.0 * znear/width, 0.0, 0.0, 0.0],
				 [0.0, 2.0*znear/height, 0.0, 0.0],
				 [0.0, 0.0, zfar/(zfar-znear), 1.0],
				 [0.0, 0.0, znear*zfar/(znear-zfar), 0.0]]
		return matrix
	
	def __mul__(self, matrix):
		return_matrix = Matrix.zero_matrix()
		for i in range(4):
			for j in range(4):
				sum = 0.0
				for k in range(4):
					sum += self.values[i][k] * matrix.values[k][j]
				return_matrix.values[i][j] = sum
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
		

