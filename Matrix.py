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

		matrix.values[3][0] = x
		matrix.values[3][1] = y
		matrix.values[3][2] = z

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
		matrix.values[2][1] = -sine
		matrix.values[1][2] = sine
		matrix.values[2][2] = cosine

		return matrix

	@classmethod
	def rotateY(self, angle):
		matrix = Matrix.identity_matrix()
		cosine = math.cos(angle)
		sine = math.sin(angle)

		matrix.values[0][0] = cosine
		matrix.values[2][0] = sine
		matrix.values[0][2] = -sine
		matrix.values[2][2] = cosine
		
		return matrix

	@classmethod
	def rotateZ(self, angle):
		matrix = Matrix.identity_matrix()
		cosine = math.cos(angle)
		sine = math.sin(angle)	
	
		matrix.values[0][0] = cosine
		matrix.values[1][0] = -sine
		matrix.values[0][1] = sine
		matrix.values[1][1] = cosine

		return matrix

	@classmethod
	def look_at(self, camera_position, camera_target, camera_up):
		zaxis = (camera_position - camera_target).normalized()
		xaxis = (camera_up.cross(zaxis)).normalized()
		yaxis = zaxis.cross(xaxis)

		matrix = Matrix()
		matrix.values = [[xaxis.x, yaxis.x, zaxis.x, 0.0],
				 [xaxis.y, yaxis.y, zaxis.y, 0.0],
				 [xaxis.z, yaxis.z, zaxis.z, 0.0],
				 [-xaxis.dot(camera_position), -yaxis.dot(camera_position), -zaxis.dot(camera_position), 1.0]]
		return matrix


	@classmethod
	def perspective(self, fov, aspect_ratio, znear, zfar):
		matrix = Matrix.identity_matrix()
		top = math.tan(fov/2.0) * znear
		right = top * aspect_ratio
		
		matrix.values[0][0] = znear/right
		matrix.values[1][1] = znear/top
		matrix.values[2][2] = -(zfar + znear)/(zfar - znear)
		matrix.values[3][2] = -2.0*zfar*znear/(zfar - znear)
		matrix.values[2][3] = -1.0
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
		x = point.x * self.values[0][0] + point.y * self.values[1][0] + point.z * self.values[2][0] + self.values[3][0]
		y = point.x * self.values[0][1] + point.y * self.values[1][1] + point.z * self.values[2][1] + self.values[3][1]
		z = point.x * self.values[0][2] + point.y * self.values[1][2] + point.z * self.values[2][2] + self.values[3][2]
		t = point.x * self.values[0][3] + point.y * self.values[1][3] + point.z * self.values[2][3] + self.values[3][3]
		
		return Vector(x/t, y/t, z/t)

	def transformVector(self, vector):
		x = vector.x * self.values[0][0] + vector.y * self.values[1][0] + vector.z * self.values[2][0]
		y = vector.x * self.values[0][1] + vector.y * self.values[1][1] + vector.z * self.values[2][1] 
		z = vector.x * self.values[0][2] + vector.y * self.values[1][2] + vector.z * self.values[2][2] 

		return Vector(x, y, z)

	def det3(self,a,b,c,d,e,f,g,h,i):
	    return a*e*i + d*h*c + g*b*f - g*e*c - d*b*i - a*h*f;

	def inverse(self):
		det  = self.values[0][0] * self.det3(self.values[1][1], self.values[1][2], self.values[1][3], self.values[2][1], self.values[2][2], self.values[2][3], self.values[3][1], self.values[3][2], self.values[3][3])
		det -= self.values[0][1] * self.det3(self.values[1][0], self.values[1][2], self.values[1][3], self.values[2][0], self.values[2][2], self.values[2][3], self.values[3][0], self.values[3][2], self.values[3][3])
		det += self.values[0][2] * self.det3(self.values[1][0], self.values[1][1], self.values[1][3], self.values[2][0], self.values[2][1], self.values[2][3], self.values[3][0], self.values[3][1], self.values[3][3])
		det -= self.values[0][3] * self.det3(self.values[1][0], self.values[1][1], self.values[1][2], self.values[2][0], self.values[2][1], self.values[2][2], self.values[3][0], self.values[3][1], self.values[3][2])

		inverse = Matrix.zero_matrix()

		inverse.values[0][0] =  self.det3(self.values[1][1], self.values[1][2], self.values[1][3], self.values[2][1], self.values[2][2], self.values[2][3], self.values[3][1], self.values[3][2], self.values[3][3]) / det
		inverse.values[0][1] = -self.det3(self.values[0][1], self.values[0][2], self.values[0][3], self.values[2][1], self.values[2][2], self.values[2][3], self.values[3][1], self.values[3][2], self.values[3][3]) / det
		inverse.values[0][2] =  self.det3(self.values[0][1], self.values[0][2], self.values[0][3], self.values[1][1], self.values[1][2], self.values[1][3], self.values[3][1], self.values[3][2], self.values[3][3]) / det
		inverse.values[0][3] = -self.det3(self.values[0][1], self.values[0][2], self.values[0][3], self.values[1][1], self.values[1][2], self.values[1][3], self.values[2][1], self.values[2][2], self.values[2][3]) / det

		inverse.values[1][0] = -self.det3(self.values[1][0], self.values[1][2], self.values[1][3], self.values[2][0], self.values[2][2], self.values[2][3], self.values[3][0], self.values[3][2], self.values[3][3]) / det
		inverse.values[1][1] =  self.det3(self.values[0][0], self.values[0][2], self.values[0][3], self.values[2][0], self.values[2][2], self.values[2][3], self.values[3][0], self.values[3][2], self.values[3][3]) / det
		inverse.values[1][2] = -self.det3(self.values[0][0], self.values[0][2], self.values[0][3], self.values[1][0], self.values[1][2], self.values[1][3], self.values[3][0], self.values[3][2], self.values[3][3]) / det
		inverse.values[1][3] =  self.det3(self.values[0][0], self.values[0][2], self.values[0][3], self.values[1][0], self.values[1][2], self.values[1][3], self.values[2][0], self.values[2][2], self.values[2][3]) / det

		inverse.values[2][0] =  self.det3(self.values[1][0], self.values[1][1], self.values[1][3], self.values[2][0], self.values[2][1], self.values[2][3], self.values[3][0], self.values[3][1], self.values[3][3]) / det
		inverse.values[2][1] = -self.det3(self.values[0][0], self.values[0][1], self.values[0][3], self.values[2][0], self.values[2][1], self.values[2][3], self.values[3][0], self.values[3][1], self.values[3][3]) / det
		inverse.values[2][2] =  self.det3(self.values[0][0], self.values[0][1], self.values[0][3], self.values[1][0], self.values[1][1], self.values[1][3], self.values[3][0], self.values[3][1], self.values[3][3]) / det
		inverse.values[2][3] = -self.det3(self.values[0][0], self.values[0][1], self.values[0][3], self.values[1][0], self.values[1][1], self.values[1][3], self.values[2][0], self.values[2][1], self.values[2][3]) / det

		inverse.values[3][0] = -self.det3(self.values[1][0], self.values[1][1], self.values[1][2], self.values[2][0], self.values[2][1], self.values[2][2], self.values[3][0], self.values[3][1], self.values[3][2]) / det
		inverse.values[3][1] =  self.det3(self.values[0][0], self.values[0][1], self.values[0][2], self.values[2][0], self.values[2][1], self.values[2][2], self.values[3][0], self.values[3][1], self.values[3][2]) / det
		inverse.values[3][2] = -self.det3(self.values[0][0], self.values[0][1], self.values[0][2], self.values[1][0], self.values[1][1], self.values[1][2], self.values[3][0], self.values[3][1], self.values[3][2]) / det
		inverse.values[3][3] =  self.det3(self.values[0][0], self.values[0][1], self.values[0][2], self.values[1][0], self.values[1][1], self.values[1][2], self.values[2][0], self.values[2][1], self.values[2][2]) / det

		return inverse
