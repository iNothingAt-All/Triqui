from tkinter import Tk, Label, Button
from functools import partial


class TriquiBox(Button):
    def __init__(self, root, width, height):
        super().__init__(root, width=width, height=height, bg="white")
        self.config(command=self.selected)

    def selected(self, color="grey"):
        self.config(bg=color, state="disabled")

    def deselect(self):
        self.config(bg="white", state="normal")


class Triqui(Label):
    def __init__(self, root, width, height):
        super().__init__(root, width=width, height=height, bg="black")
        self._size = (width, height)
        self._winning_plays = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        self._moves = (("red", []), ("blue", []))
        self._boxs = []
        self._turn = 0

        self._fill()
        self._sort()

    def repeat(self):
        for index in range(9):
            self._boxs[index].deselect()

        self._moves = (("red", []), ("blue", []))

    def _is_winner(self, moves):
        for winning_line in self._winning_plays:
            count = 0

            for index in moves:
                if index in winning_line:
                    count += 1

                if count >= 3:
                    return True

        return False

    def _win(self, color):
        for index in range(9):
            self._boxs[index].selected(color)

    def _fill(self):
        for index in range(9):
            self._boxs.append(TriquiBox(self, self._size[0]//3, self._size[1]//3))
            self._boxs[index].config(command=partial(self._add_move, index))

    def _sort(self):
        index = 0
        for y in range(3):
            for x in range(3):
                self._boxs[index].grid(row=y, column=x)
                index += 1

    def _add_move(self, index):
        turn = self._moves[self._turn]
        turn[1].append(index)

        self._boxs[index].selected(turn[0])
        self._turn = not self._turn

        if self._is_winner(turn[1]):
            self._win(turn[0])


window = Tk()
window.resizable(False, False)
window.title("Triqui")

trike = Triqui(window, 30, 15)
trike.pack()

Button(window, text="Repeat", bg="grey", width=20, command=trike.repeat).pack()
window.mainloop()
