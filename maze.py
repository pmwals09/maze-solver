from cell import Cell
from point import Point
import time
import random


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = random.seed(seed)
        self._create_cells()

    def _create_cells(self):
        self._cells = []
        for colIdx in range(self.num_cols):
            row = []
            for rowIdx in range(self.num_rows):
                cell_x = self.x1 + (rowIdx * self.cell_size_x)
                cell_y = self.y1 + (colIdx * self.cell_size_y)
                start_point = Point(cell_x, cell_y)
                end_point = Point(
                    cell_x + self.cell_size_x,
                    cell_y + self.cell_size_y
                )
                row.append(Cell(start_point, end_point, self.win))
            self._cells.append(row)
        if self.win:
            for row in range(self.num_rows):
                for col in range(self.num_cols):
                    self._draw_cell(row, col)
            self._break_entrance_and_exit()
            self._break_walls_r(0, 0)
            self._reset_cells_visited()

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        cell.draw("black")
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_rows - 1][self.num_cols -
                                       1].has_bottom_wall = False
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)

    def _break_walls_r(self, i, j):
        curr = self._cells[i][j]
        curr.visited = True
        while True:
            to_visit = []
            if i > 0:
                c = self._cells[i - 1][j]
                if not c.visited:
                    to_visit.append((i - 1, j))
            if i < self.num_rows - 1:
                c = self._cells[i + 1][j]
                if not c.visited:
                    to_visit.append((i + 1, j))
            if j > 0:
                c = self._cells[i][j - 1]
                if not c.visited:
                    to_visit.append((i, j - 1))
            if j < self.num_cols - 1:
                c = self._cells[i][j + 1]
                if not c.visited:
                    to_visit.append((i, j + 1))
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            next = to_visit[random.randrange(len(to_visit))]
            # how to know which wall to break?
            if next[0] == i and next[1] == j - 1:
                curr.has_left_wall = False
                self._cells[next[0]][next[1]].has_right_wall = False
            if next[0] == i and next[1] == j + 1:
                curr.has_right_wall = False
                self._cells[next[0]][next[1]].has_left_wall = False
            if next[0] == i - 1 and next[1] == j:
                curr.has_top_wall = False
                self._cells[next[0]][next[1]].has_bottom_wall = False
            if next[0] == i + 1 and next[1] == j:
                curr.has_bottom_wall = False
                self._cells[next[0]][next[1]].has_top_wall = False
            self._break_walls_r(*next)

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        curr = self._cells[i][j]
        curr.visited = True
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True
        if not curr.has_top_wall and i > 0:
            next = self._cells[i - 1][j]
            if not next.visited:
                curr.draw_move(next)
                res = self._solve_r(i - 1, j)
                if res:
                    return True
                else:
                    curr.draw_move(next, undo=True)
        if not curr.has_right_wall and j < self.num_cols - 1:
            next = self._cells[i][j + 1]
            if not next.visited:
                curr.draw_move(next)
                res = self._solve_r(i, j + 1)
                if res:
                    return True
                else:
                    curr.draw_move(next, undo=True)
        if not curr.has_bottom_wall and i < self.num_rows - 1:
            next = self._cells[i + 1][j]
            if not next.visited:
                curr.draw_move(next)
                res = self._solve_r(i + 1, j)
                if res:
                    return True
                else:
                    curr.draw_move(next, undo=True)
        if not curr.has_left_wall and j > 0:
            next = self._cells[i][j - 1]
            if not next.visited:
                curr.draw_move(next)
                res = self._solve_r(i, j - 1)
                if res:
                    return True
                else:
                    curr.draw_move(next, undo=True)
        return False
