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
		self.data = data=numpy.array(numpy.ndarray((height,width)),dtype=int)
		self.width = width
		self.height = height
		self.root = Tk()
		self.frame = Frame(self.root, width=self.width, height=self.height)
		self.frame.pack()
		self.canvas = Canvas(self.frame, width=self.width, height=self.height)
		self.canvas.place(x=-2,y=-2)

		self.camera_position = Vector(0.0, 0.0, 1.0)
		self.camera_target = Vector(0.0, 0.0, 0.0)
		self.camera_up = Vector(0.0, 1.0, 0.0)
		
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

	def plotPoint(self, x, y):
		if x >= 0 and y >= 0 and x < self.width and y < self.height:
			self.data[y][x] = 255
			
	def plotLine(self, p0, p1):
		x0 = int(self.width - ((p0.x * self.width/2) + self.width/2))
		y0 = int(self.height - ((p0.y * self.height/2) + self.height/2))
		x1 = int(self.width - ((p1.x * self.width/2) + self.width/2))
		y1 = int(self.height - ((p1.y * self.height/2) + self.height/2))
		
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
				



	def plotScanLine(y, p1, p2, p3, p4):
		gradient1 = ((y - p1.y) / (p2.y - p1.y)) if (p1.y != p2.y) else 1
		gradient2 = ((y - p3.y) / (p4.y - p3.y)) if (p3.y != p4.y) else 1

		
		
	def plotTriangle(self, triangle):
		if triangle.p1.y > triangle.p2.y:
			temp = triangle.p2
			triangle.p2 = triangle.p1
			p1 = temp

		if triangle.p2.y > triangle.p3.y:
			temp = triangle.p2
			triangle.p2 = triangle.p3
			triangle.p3 = temp

		if triangle.p1.y > triangle.p2.y:
			temp = triangle.p2
			triangle.p2 = triangle.p1
			p1 = temp

		dP1P2 = 0
		dP1P3 = 0

		if triangle.p2.y - triangle.p1.y > 0:
			dP1P2 = (triangle.p2.x - triangle.p1.x) / (triangle.p2.y - triangle.p1.y)
		else:
			dP1P2 = 0

		if triangle.p3.y - triangle.p1.y > 0:
			dP1P3 = (triangle.p3.x - triangle.p1.x) / (triangle.p3.y - triangle.p1.y)
		else:
			dP1P3 = 0

		y1 = int(self.height - ((triangle.p1.y * self.height/2) + self.height/2))
		y2 = int(self.height - ((triangle.p2.y * self.height/2) + self.height/2))
		y3 = int(self.height - ((triangle.p3.y * self.height/2) + self.height/2))
		
		if dP1P2 > dP1P3:
			for y in range(y1, y3):
				if (y < y2):
					plotScanLine(y, y1, y3, y1, y2)
				else:
					plotScanLine(y, y1, y3, y2, y3)
		else:
			for y in range(y1, y3):
				if (y < y2):
					plotScanLine(y, y1, y2, y1, y3)
				else:
					plotScanLine(y, y2, y3, y1, y3)
			
	def drawTriangle(self,triangle):
		self.plotLine(triangle.p1, triangle.p2)
		self.plotLine(triangle.p1, triangle.p3)
		self.plotLine(triangle.p2, triangle.p3)
		#self.plotPoint(triangle.p1.x, triangle.p1.y)
		#self.plotPoint(triangle.p2.x, triangle.p2.y)
		#self.plotPoint(triangle.p3.x, triangle.p3.y)

	def project(self, point):
		x = (point.x * float(self.width) + float(self.width) / 2.0)
		y = (-point.y * float(self.height) + float(self.height) / 2.0)
		return Vector(x, y,0.0)
												 
	def loop(self):
		global data
		self.im=Image.fromstring('L', (self.data.shape[1],\
				self.data.shape[0]), self.data.astype('b').tostring())
		self.photo = ImageTk.PhotoImage(image=self.im)
		self.canvas.create_image(0,0,image=self.photo,anchor=NW)
		self.root.update()
		self.times+=1
		if self.times%33==0:
			print("%.02f FPS"%(self.times/(time.clock()-self.timestart)))

		self.data = data=numpy.array(numpy.ndarray((self.height, self.width)),dtype=int)
		self.angle += 0.1

		view_matrix = Matrix.look_at_lh(self.camera_position, self.camera_target, self.camera_up)
		projection_matrix = Matrix.perspective_rh(640.0, 480.0, -1.0, 1.0)
		m = view_matrix * projection_matrix
		v = Vector(0.5,1.0,0.0)
		v = m.transformPoint(v)
		print(self.project(v))
		for t in self.triangles:
			self.drawTriangle(t * Matrix.rotateY(self.angle))         
		self.root.after(0, self.loop)
		


def main():
	x = mainWindow(WIDTH, HEIGHT)
	
if __name__ == "__main__":
	main()


