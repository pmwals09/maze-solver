from line import Line
from point import Point


class Cell:
    def __init__(self, p1, p2, win=None):
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_left_wall = True
        self.__p1 = p1
        self.__p2 = p2
        self.__win = win
        self.visited = False

    def draw(self, fill_color):
        original_fill_color = fill_color

        line = Line(self.__p1, Point(self.__p2.x, self.__p1.y))
        if not self.has_top_wall:
            fill_color = "white"
        self.__win.draw_line(line, fill_color)

        fill_color = original_fill_color
        line = Line(Point(self.__p2.x, self.__p1.y), self.__p2)
        if not self.has_right_wall:
            fill_color = "white"
        self.__win.draw_line(line, fill_color)

        fill_color = original_fill_color
        line = Line(self.__p2, Point(self.__p1.x, self.__p2.y))
        if not self.has_bottom_wall:
            fill_color = "white"
        self.__win.draw_line(line, fill_color)

        fill_color = original_fill_color
        line = Line(Point(self.__p1.x, self.__p2.y), self.__p1)
        if not self.has_left_wall:
            fill_color = "white"
        self.__win.draw_line(line, fill_color)

    def draw_move(self, to_cell, undo=False):
        if undo:
            fill_color = "gray"
        else:
            fill_color = "red"
        mid_x = (self.__p1.x + self.__p2.x) / 2
        mid_y = (self.__p1.y + self.__p2.y) / 2
        start_point = Point(mid_x, mid_y)
        mid_x = (to_cell.__p1.x + to_cell.__p2.x) / 2
        mid_y = (to_cell.__p1.y + to_cell.__p2.y) / 2
        end_point = Point(mid_x, mid_y)
        line = Line(start_point, end_point)
        self.__win.draw_line(line, fill_color)
