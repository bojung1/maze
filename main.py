from tkinter import Tk, BOTH, Canvas
import time
import random

class Window():
	def __init__ (self, width, height, title="Title"):
		self.__root = Tk() 
		self.__root.title(title) 
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


"""
    (x1,y1) +------+ (x2,y1)
            |      |
            |      |
    (x1,y2) +------+ (x2,y2)
"""


class Cell():
	def __init__(self, win, x1 = None, y1 = None, x2 = None, y2 = None):
		self.has_left_wall = True
		self.has_right_wall = True
		self.has_top_wall = True 
		self.has_bottom_wall = True 
		self._x1 = x1
		self._x2 = x2
		self._y1 = y1
		self._y2 = y2
		self._visited = False
		self._win = win  

	def draw(self, x1, y1, x2, y2):
		if self._win is not None:
			bwal = Line(Point(x1, y2), Point(x2, y2))
			twal = Line(Point(x1, y1), Point(x2, y1))
			rwal = Line(Point(x2, y1), Point(x2, y2))
			lwal = Line(Point(x1, y1), Point(x1, y2))

			if self.has_bottom_wall:				
				self._win.draw_line(bwal, "black")
			else: 
				self._win.draw_line(bwal, "white")

			if self.has_top_wall:				
				self._win.draw_line(twal, "black")
			else:
				self._win.draw_line(twal, "white")

			if self.has_right_wall:
				self._win.draw_line(rwal, "black")
			else:
				self._win.draw_line(rwal, "white")

			if self.has_left_wall:
				self._win.draw_line(lwal, "black")
			else:
				self._win.draw_line(lwal, "white")


	def draw_move(self, to_cell, undo = False):
		if undo == True:
			color = "gray"
		else: 
			color = "red" 

		midx = abs(self._x1 + self._x2) // 2 
		midy = abs(self._y1 + self._y2) // 2

		tomidx = abs(to_cell._x1 + to_cell._x2) // 2
		tomidy = abs(to_cell._y1 + to_cell._y2) // 2

		# offset the position of the undo lines slightly to keep the red ones visible
		# this might break or look ugly on cells < 3 width 

		if undo == True:
			midx += 1
			midy += 1
			tomidx += 1
			tomidy += 1 


		sp = Point(midx, midy)
		dp = Point(tomidx, tomidy)

		moveline = Line(sp, dp)
		self._win.draw_line(moveline, color)



class Maze():
	def __init__(
		self,
		x1,
		y1,
		num_rows,
		num_cols,
		cell_size_x,
		cell_size_y,
		win = None,
		seed = None,
	):
		self.x1 = x1
		self.y1 = y1 
		self.num_rows = num_rows
		self.num_cols = num_cols
		self.cell_size_x = cell_size_x
		self.cell_size_y = cell_size_y
		self._win = win 
		
		if seed is not None:
			self._seed = random.seed(seed)

		self._create_cells() 


	def _create_cells(self): 
		# This method should fill a self._cells list with lists of cells. 
		# Each top-level list is a column of Cell objects. Once the matrix is populated 
		# it should call its _draw_cell() method on each Cell.
		self._cells = []
		for a in range(0, self.num_cols):
			templist = []
			for b in range(0, self.num_rows):
				templist.append(Cell(self._win))
			self._cells.append(templist)

		for c in range(0,len(self._cells)):
			for d in range(0,len(self._cells[c])):
				self._draw_cell(c,d) 

		self._break_entrance_and_exit()
		self._break_walls_r(0,0)
		self._reset_cells_visited()


	# i is the column (x axis)
	# j is the row (y axis)
	#you have to do some math in order to get it to draw at the right place
	def _draw_cell(self, i, j):

		xpos = self.x1 + (i * self.cell_size_x)
		ypos = self.y1 + (j * self.cell_size_y)
		xpos2 = xpos + self.cell_size_x
		ypos2 = ypos + self.cell_size_y

		self._cells[i][j]._x1 = xpos
		self._cells[i][j]._y1 = ypos 
		self._cells[i][j]._x2 = xpos2
		self._cells[i][j]._y2 = ypos2


		self._cells[i][j].draw(xpos, ypos, xpos2, ypos2)
		self._animate()

	def _animate(self):
		if self._win is None:
			return 
		self._win.redraw()
		time.sleep(0.05)


	def _break_entrance_and_exit(self):
		#entrance always at top left (upper wall) 
		#exit always at bottom right (bottom wall)
		entx = 0
		enty = 0

		exx = self.num_cols-1
		exy = self.num_rows-1

		self._cells[entx][enty].has_top_wall = False
		self._draw_cell(entx,enty)
		
		self._cells[exx][exy].has_bottom_wall = False
		self._draw_cell(exx, exy)

	def _break_walls_r(self, i, j):
		self._cells[i][j]._visited = True
		while True:

			need_visit = []
			
			left = i - 1
			right = i + 1
			up = j - 1
			down = j + 1

			if left >= 0:
				if self._cells[left][j]._visited == False:
					need_visit.append((left, j))
			if right < self.num_cols:
				if self._cells[right][j]._visited == False:
					need_visit.append((right,j))
			if up >= 0:
				if self._cells[i][up]._visited == False:
					need_visit.append((i, up))
			if down < self.num_rows:
				if self._cells[i][down]._visited == False: 
					need_visit.append((i,down))

			if need_visit == []:
				self._draw_cell(i,j)
				return

			rand_dir = random.randrange(0,len(need_visit))
			
			#this is a tuple 
			dest_cell = need_visit[rand_dir] 

			#figure out which direction it was, because the list of possible moves is not always 4
			#then remove the walls 
			dx = i - dest_cell[0]
			dy = j - dest_cell[1] 

			# in theory, only one of these should ever be picked per iteration. 
			if dx == 1:
				# go left
				self._cells[i][j].has_left_wall = False
				self._cells[dest_cell[0]][dest_cell[1]].has_right_wall = False 
			elif dx == -1:
				# go right 
				self._cells[i][j].has_right_wall = False
				self._cells[dest_cell[0]][dest_cell[1]].has_left_wall = False 
			elif dy == 1:
				# go up 
				self._cells[i][j].has_top_wall = False
				self._cells[dest_cell[0]][dest_cell[1]].has_bottom_wall = False 
			elif dy == -1:
				# go down 
				self._cells[i][j].has_bottom_wall = False
				self._cells[dest_cell[0]][dest_cell[1]].has_top_wall = False 

			self._break_walls_r(dest_cell[0],dest_cell[1])



	def _reset_cells_visited(self):
		for a in range(0, self.num_cols):
			for b in range(0, self.num_rows):
				self._cells[a][b]._visited = False 



	def solve(self):
		return self._solve_r(0, 0)


	def _solve_r(self, i, j):
		self._animate()
		self._cells[i][j]._visited = True
		if i == (self.num_cols - 1) and j == (self.num_rows - 1):
			return True 

		#in a positional list the indices are: (clockwise)
		#0 is up
		#1 is right
		#2 is down
		#3 is left 

		# fucking exclusionary upper bound in ranges 

		#[up, right, down, left]
		val_dirs = [True, True, True, True]

		for a in range (0, 4):
			match a:
				case 0:
					#check up 
					if j > 0 and self._cells[i][j].has_top_wall == False and self._cells[i][j-1]._visited == False:
						val_dirs[0] = True
					else: 
						val_dirs[0] = False
				case 1:
					#check right
					if i < self.num_cols - 1 and self._cells[i][j].has_right_wall == False and self._cells[i+1][j]._visited == False:
						val_dirs[1] = True
					else: 
						val_dirs[1] = False 
				case 2: 
					#check down 
					if j < self.num_rows - 1 and self._cells[i][j].has_bottom_wall == False and self._cells[i][j+1]._visited == False:
						val_dirs[2] = True
					else:
						val_dirs[2] = False 
				case 3: 
					#check left 
					if i > 0 and self._cells[i][j].has_left_wall == False and self._cells[i-1][j]._visited == False: 
						val_dirs[3] = True
					else:
						val_dirs[3] = False 

		# I wanted to check validity first and then actually process the moves, 
		# more duplicated code, but better visually for me. 

		for a in range(0, 4):
			match a:
				case 0:
					# go up
					if val_dirs[a] == True:
						self._cells[i][j].draw_move(self._cells[i][j-1])	
						if self._solve_r(i, j-1) == True:
							return True
						else: 
							self._cells[i][j-1].draw_move(self._cells[i][j], True)
				case 1:
					# go right 
					if val_dirs[a] == True:
						self._cells[i][j].draw_move(self._cells[i+1][j])	
						if self._solve_r(i+1, j) == True:
							return True 
						else:
							self._cells[i+1][j].draw_move(self._cells[i][j], True)
				case 2:
					# go down 
					if val_dirs[a] == True:
						self._cells[i][j].draw_move(self._cells[i][j+1])
						if self._solve_r(i, j+1) == True: 
							return True
						else:
							self._cells[i][j+1].draw_move(self._cells[i][j], True)
				case 3: 
					# go left 
					if val_dirs[a] == True:
						self._cells[i][j].draw_move(self._cells[i-1][j])
						if self._solve_r(i-1, j) == True: 
							return True
						else: 
							self._cells[i-1][j].draw_move(self._cells[i][j], True)

		return False 

# This is just here cause I like the visual divider.
# ===============================================================

def main ():
	win = Window(1024,768,"Thicc Maze Thing")


	m = Maze(100, 100, 5, 5, 25, 25, win)

	# when it's ready
	m.solve()


	# draw a smiley face... eventually. 

	p1 = Point(75,20)
	p2 = Point(75,30)
	l1 = Line(p1, p2)
	win.draw_line(l1,"black")

	p3 = Point(100,20)
	p4 = Point(100,30)
	l2 = Line(p3, p4)
	win.draw_line(l2,"black")

	p5 = Point(60,40)
	p6 = Point(60,55)
	l3 = Line(p5, p6)
	win.draw_line(l3,"black")

	p7 = Point(115,40)
	p8 = Point(115,55)
	l4 = Line(p7, p8)
	win.draw_line(l4,"black")

	p9 = Point(60,55)
	p10 = Point(115,55)
	l5 = Line(p9, p10)
	win.draw_line(l5,"black")

	win.wait_for_close()


if __name__ == "__main__":
	main()
