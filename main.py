from window import Window
from maze import Maze


def main():
    win = Window(800, 600)
    m = Maze(100, 100, 20, 20, 20, 20, win)
    m.solve()
    win.wait_for_close()


main()
