import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

class Players(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = " "

BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Players(label= "X", color= 'orange'),
    Players(label='O', color= 'yellow'),
)


class TicTacToe:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self.players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self.players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        cols = [list(col) for col in zip(*rows)]
        diagonals = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(cols))]
        return rows + cols + [diagonals, second_diagonal]
    
    def toggle_player(self):
        self.current_player = next(self._players)

    def is_valid_move(self, move):
        row, col = move.row, move.col
        move_not_played =  self._current_moves[row][col].label == " "
        no_winner = not self._has_winner
        return move_not_played and no_winner

    def is_game_over(self, move):
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[n][m].label for n, m in combo)
            is_winner = (len(results) == 1) and (' ' not in results)
            if is_winner:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        return self._has_winner
    
    def is_tie(self):
        no_winner = not self._has_winner
        all_moves_played = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(all_moves_played)
    
    def reset(self):
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

class Board(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic Tac Toe")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()


    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        options_menu = tk.Menu(master=menu_bar)
        options_menu.add_command(label="New Game", command=self._new_game)
        options_menu.add_separator()
        options_menu.add_command(label="Quit", command=quit)
        menu_bar.add_cascade(label="Options", menu=options_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text=f"{self._game.current_player.label}'s turn",
            font=font.Font(size=24),
        )
        self.display.pack()
    
    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1)
            self.columnconfigure(row, weight=1)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text=" ",
                    font=font.Font(size=24),
                    width=3,
                    height=2,
                )
                self._cells[button] = (row, col)
                button.grid(row=row, column=col, sticky="nsew")
                button.bind("<Enter>", self.play)

    def play(self, event):
        clicked_button = event.widget
        row, col = self._cells[clicked_button]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_button)
            self._game.is_game_over(move)
            if self._game.is_tie():
                self._update_display(text="It's a tie!")
            elif self._game.has_winner():
                self._highlight_winning_combo()
                msg = f"{self._game.current_player.label} won!"
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                self._update_display(
                    f"{self._game.current_player.label}'s turn"
                )

    def _update_button(self, clicked_button):
        clicked_button.config(text=self._game.current_player.label)
        clicked_button.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display['text'] = msg
        self.display['fg'] = color

    def _highlight_winning_combo(self):
        for button, coordinates in self._cells.items():
            row, col = coordinates
            if (row, col) in self._game.winner_combo:
                button.config(bg="green")

    def _new_game(self):
        self._game.reset_game()
        self._update_display(msg= 'Reset Ready!')
        for button in self._cells.keys():
            button.config(highlightbackground="blue")
            button.config(text=" ")
            button.config(fg="black")

def main():
    game = TicTacToe()
    board = Board(game)
    board.mainloop()


if __name__ == "__main__":
    main()



        