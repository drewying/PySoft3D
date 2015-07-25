from Vector import *
from Matrix import *
from Triangle import *
import math
import mpmath
from tkinter import *
import numpy
import time
from PIL import Image, ImageTk

WIDTH = 640
HEIGHT = 480


class mainWindow:

	
	

	def __init__(self, width, height):
		self.width = width
		self.height = height


		self.data = numpy.array(numpy.ndarray((self.height, self.width)),dtype=int)
		self.depth_buffer = numpy.array(numpy.ndarray((self.height,self.width)),dtype=float)
		self.root = Tk()
		self.frame = Frame(self.root, width=self.width, height=self.height)
		self.frame.pack()
		self.canvas = Canvas(self.frame, width=self.width, height=self.height)
		self.canvas.place(x=-2,y=-2)

		self.camera_position = Vector(0.0, 0.5, -5.0)
		self.camera_target = Vector(0.0, 0.0, 0.0)
		self.camera_up = Vector(0.0, 1.0, 0.0)

		view_matrix = Matrix.look_at(self.camera_position, self.camera_target, self.camera_up)
		project_matrix = Matrix.perspective(0.78, 640/480.0, -1.0, 1.0)
		self.world_matrix = project_matrix * view_matrix
		
		self.triangles = []
		self.points = []
		
		print("Reading file...")
		f = open('teapot.obj', 'r')
		for line in f:
			if line[0] == 'v':
				parts = line.split(" ")
				self.points.append(Vector(float(parts[1]), float(parts[2]), float(parts[3])))
			elif line[0] == 'f':
				parts = line.split(" ")
				index1 = int(parts[1].split("//")[0])
				index2 = int(parts[2].split("//")[0])
				index3 = int(parts[3].split("//")[0])
				
				self.triangles.append(Triangle(self.points[index1-1], self.points[index2-1], self.points[index3-1]))

		f.close()

		self.times = 1
		self.timestart=time.clock()
	
		self.angle = 0.0
		self.root.after(0, self.loop)
		self.root.mainloop()

	def plotPoint(self, x, y, color):
		if x >= 0 and y >= 0 and x < self.width and y < self.height:
			self.data[y][x] = int(color)
			
	def plotLine(self, p0, p1):
		x0 = int(p0.x) #int(self.width - ((p0.x * self.width/2) + self.width/2))
		y0 = int(p0.y) #int(self.height - ((p0.y * self.height/2) + self.height/2))
		x1 = int(p1.x) #int(self.width - ((p1.x * self.width/2) + self.width/2))
		y1 = int(p1.y) #int(self.height - ((p1.y * self.height/2) + self.height/2))
		
		dx = abs(x1 - x0)
		dy = abs(y1 - y0)
		sx = 1 if (x0 < x1) else -1
		sy = 1 if (y0 < y1) else -1
		error = dx - dy

		while True:
			self.plotPoint(x0,y0)
			if ((x0 == x1) and (y0 == y1)):
				break
			
			e2 = 2 * error
			if e2 > -dy:
				error -= dy
				x0 += sx
			if e2 < dx:
				error += dx
				y0 += sy
				

	def edgeFunction(self, a, b, c):
		return (c.x - a.x) * (b.y - a.y) - (c.y - a.y) * (b.x - a.x)

	def plotScanLine(y, p1, p2, p3, p4):
		gradient1 = ((y - p1.y) / (p2.y - p1.y)) if (p1.y != p2.y) else 1
		gradient2 = ((y - p3.y) / (p4.y - p3.y)) if (p3.y != p4.y) else 1
		
	def plotTriangle(self, triangle):
		v0 = self.project(triangle.p1)
		v1 = self.project(triangle.p2)
		v2 = self.project(triangle.p3)
		v0.z = 1.0/v0.z
		v1.z = 1.0/v1.z
		v2.z = 1.0/v2.z
		
		x_min = int(min(v0.x, v1.x, v2.x))
		x_max = int(max(v0.x, v1.x, v2.x) + 1)
		y_min = int(min(v0.y, v1.y, v2.y))
		y_max = int(max(v0.y, v1.y, v2.y) + 1)
	
		for x in range(x_min, x_max):
			for y in range(y_min, y_max):
				p = Vector(x,y,0)
				area = self.edgeFunction(v0, v1, v2)
				w0 = self.edgeFunction(v1, v2, p)
				w1 = self.edgeFunction(v2, v0, p)
				w2 = self.edgeFunction(v0, v1, p)
				if w0 >= 0 and w1 >= 0 and w2 >=0:
					w0 /= area
					w1 /= area
					w2 /= area
					z = (1.0/(v0.z * w0 + v1.z * w1 +  v2.z * w2))
					if (z < self.depth_buffer[y][x]):
						self.depth_buffer[y][x] = z
						#v0cam = self.world_matrix.transformVector(v0)
						#v1cam = self.world_matrix.transformVector(v1)
						#v2cam = self.world_matrix.transformVector(v2)

						#px = (v0cam.x/-v0cam.z) * w0 + (v1cam.x/-v1cam.z) * w1 + (v2cam.x/-v2cam.z) * w2 
						#py = (v0cam.y/-v0cam.z) * w0 + (v1cam.y/-v1cam.z) * w1 + (v2cam.y/-v2cam.z) * w2

						#p = Vector(px * z, py * z, -z)
						#pt = p.normalized() * -1
						#n = (v1cam - v0cam).cross(v2cam - v0cam).normalized()
						#self.plotPoint(x, y, 255 * max(0, n.dot(pt)))
						self.plotPoint(x,y,255)
		
		
		
			
	def drawTriangle(self,triangle):
		self.plotTriangle(triangle)
		#self.plotLine(self.project(triangle.p1), self.project(triangle.p2))
		#self.plotLine(self.project(triangle.p1), self.project(triangle.p3))
		#self.plotLine(self.project(triangle.p2), self.project(triangle.p3))


	def project(self, point):
		point = self.world_matrix.transformPoint(point)
		x = (point.x * float(self.width) + float(self.width) / 2.0)
		y = (point.y * float(self.height) + float(self.height) / 2.0)
		return Vector(x, y, -point.z)
												 
	def loop(self):
		self.data.fill(0)
		self.depth_buffer.fill(1000.0)
		self.angle += 0.1
		
		for t in self.triangles:
			self.drawTriangle(t * Matrix.rotateY(self.angle))
			
		global data
		self.im=Image.fromstring('L', (self.data.shape[1],\
				self.data.shape[0]), self.data.astype('b').tostring())
		self.photo = ImageTk.PhotoImage(image=self.im)
		self.canvas.create_image(0,0,image=self.photo,anchor=NW)
		self.root.update()
		self.times+=1
		if self.times%33==0:
			print("%.02f FPS"%(self.times/(time.clock()-self.timestart)))

		         
		self.root.after(0, self.loop)
		


def main():
	x = mainWindow(WIDTH, HEIGHT)
	
if __name__ == "__main__":
	main()


