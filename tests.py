import unittest

from main import Maze
from main import Window

class Tests(unittest.TestCase):
	def test_maze_create_cells(self):
		num_cols = 12
		num_rows = 10
		m1 = Maze(0,0, num_rows, num_cols, 10, 10)
		self.assertEqual(
			len(m1._cells),
			num_cols,
		)

		self.assertEqual(
			len(m1._cells[0]),
				num_rows,
		)

	def test_maze_create_cells_5x5_size20_visual(self):
		num_cols = 5
		num_rows = 5
		cs_x = 20
		cs_y = 20 
		win = Window("800", "600")
		m1 = Maze(100 , 100, num_rows, num_cols, cs_x, cs_y, win)
		self.assertEqual(
			len(m1._cells),
			num_cols,
		)

		self.assertEqual(
			len(m1._cells[0]),
				num_rows,
		)


	
	def test_init_walls_edges_maze(self):
		m = Maze(50, 50, 3, 3, 10, 10)

		self.assertTrue(m._cells[0][0].has_left_wall)
		self.assertTrue(m._cells[2][0].has_right_wall)
		self.assertTrue(m._cells[0][2].has_bottom_wall)
		self.assertTrue(m._cells[1][0].has_top_wall)


	def test_cell_pos(self):
		cs_x = 10
		cs_y = 15
		# x pos, y pos, numcol, numrow, csizex, csizey, win(optional)
		m = Maze(5, 10, 2, 2, cs_x, cs_y)

		self.assertEqual(m._cells[0][0]._x1, 5)
		self.assertEqual(m._cells[0][0]._y1, 10)

		self.assertEqual(m._cells[1][0]._x1, 5 + cs_x)
		self.assertEqual(m._cells[1][0]._y1, 10)

		self.assertEqual(m._cells[0][1]._x1, 5)
		self.assertEqual(m._cells[0][1]._y1, 10 + cs_y)


	def test_ent_exit_walls_5x5_size20(self):
		num_cols = 5
		num_rows = 5
		fin_col = num_cols-1
		fin_row = num_rows-1
		cs_x = 20
		cs_y = 20 
		m = Maze(10,10,num_cols,num_rows,cs_x,cs_y)

		self.assertEqual(m._cells[0][0].has_top_wall, False)
		self.assertEqual(m._cells[fin_col][fin_row].has_bottom_wall, False)


	def test_maze_visited_state_post_create(self):
		num_cols = 5
		num_rows = 5
		cs_x = 20
		cs_y = 20 
		m = Maze(10,10,num_cols,num_rows,cs_x,cs_y)

		self.assertEqual(m._cells[2][2]._visited, False)
		self.assertEqual(m._cells[4][4]._visited, False)
		self.assertEqual(m._cells[1][3]._visited, False)



if __name__ == "__main__":
	unittest.main()


