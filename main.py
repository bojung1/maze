from tkinter import Tk, BOTH, Canvas

class Window():
	def __init__ (self, width, height):
		self.__root = Tk() 
		self.__root.title = "Title" 
		self.__canvas = Canvas(self.__root, bg="white", height=height, width=width) 
		self.__canvas.pack(fill = BOTH, expand = 1) 
		self.__window_running = False
		self.__root.protocol("WM_DELETE_WINDOW", self.close)

	def redraw(self):
		self.__root.update_idletasks()
		self.__root.update() 

	def wait_for_close(self):
		self.__window_running = True
		while self.__window_running:
			self.redraw() 

	def close(self):
		self.__window_running = False

	def draw_line(self, line, fill_color):
		line.draw(self.__canvas, fill_color)


# x,y (0,0) is the top left of the screen
class Point():
	def __init__ (self, x, y):
		self.x = x 
		self.y = y 

class Line():
	def __init__ (self, point1, point2):
		self.p1 = point1
		self.p2 = point2

	def draw(self, canvas, fill_color):
		canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width = 2)



def main ():
	win = Window(800,600)
	p1 = Point(5,5)
	p2 = Point(10,10)
	p3 = Point(100,100)
	p4 = Point(50,50)

	l1 = Line(p1, p2)
	l2 = Line(p3, p4)

	win.draw_line(l1,"black")
	win.draw_line(l2,"red")




	win.wait_for_close()


if __name__ == "__main__":
	main()