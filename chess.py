import tkinter as tk
from tkinter import messagebox

# Main Chess Game Application
class ChessGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess Game")
        self.geometry("640x640")
        
        self.selected_piece = None
        self.turn = "white"  # White starts the game
        self.squares = {}    # Dictionary to store squares
        
        self.create_board()
        self.setup_pieces()
    
    def create_board(self):
        colors = ["#DDB88C", "#A66D4F"]  # Chessboard colors
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                square = tk.Label(self, bg=color, width=8, height=4, font=("Arial", 24, "bold"))
                square.grid(row=row, column=col, sticky="nsew")
                self.squares[(row, col)] = square
                square.bind("<Button-1>", lambda event, r=row, c=col: self.select_square(r, c))
        
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)
    
    def setup_pieces(self):
        self.pieces = {}
        
        # Symbols for each piece (Unicode chess characters)
        self.piece_icons = {
            "wp": "♙", "wr": "♖", "wn": "♘", "wb": "♗", "wq": "♕", "wk": "♔",
            "bp": "♟", "br": "♜", "bn": "♞", "bb": "♝", "bq": "♛", "bk": "♚"
        }
        
        # Initial positions
        initial_positions = {
            "wp": [(1, col) for col in range(8)],
            "bp": [(6, col) for col in range(8)],
            "wr": [(0, 0), (0, 7)], "br": [(7, 0), (7, 7)],
            "wn": [(0, 1), (0, 6)], "bn": [(7, 1), (7, 6)],
            "wb": [(0, 2), (0, 5)], "bb": [(7, 2), (7, 5)],
            "wq": [(0, 3)], "bq": [(7, 3)],
            "wk": [(0, 4)], "bk": [(7, 4)]
        }
        
        # Place pieces on the board
        for piece, positions in initial_positions.items():
            for row, col in positions:
                self.add_piece(piece, row, col)
    
    def add_piece(self, piece, row, col):
        self.pieces[(row, col)] = piece
        self.squares[(row, col)].config(text=self.piece_icons[piece], fg="black" if piece[0] == "b" else "white")
    
    def select_square(self, row, col):
        if self.selected_piece:
            if self.move_piece(self.selected_piece, (row, col)):
                self.selected_piece = None
            else:
                messagebox.showwarning("Invalid Move", "This move is not allowed.")
        else:
            piece = self.pieces.get((row, col))
            if piece and ((self.turn == "white" and piece[0] == "w") or (self.turn == "black" and piece[0] == "b")):
                self.selected_piece = (row, col)
    
    def move_piece(self, start, end):
        start_piece = self.pieces.get(start)
        if not start_piece or not self.is_valid_move(start, end, start_piece):
            return False
        
        # Move piece
        self.pieces[end] = self.pieces.pop(start)
        self.squares[start].config(text="")
        self.squares[end].config(text=self.piece_icons[start_piece], fg="black" if start_piece[0] == "b" else "white")
        
        # Change turn
        self.turn = "black" if self.turn == "white" else "white"
        return True
    
    def is_valid_move(self, start, end, piece):
        # Basic move validation
        start_row, start_col = start
        end_row, end_col = end
        piece_type = piece[1]
        
        if piece[0] == "w" and end_row >= start_row:  # White moves up
            return False
        if piece[0] == "b" and end_row <= start_row:  # Black moves down
            return False
        
        if piece_type == "p":  # Pawn movement
            if abs(start_row - end_row) == 1 and start_col == end_col and (end not in self.pieces):
                return True  # Move forward
            if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1 and (end in self.pieces):
                return True  # Capture diagonally
            
        elif piece_type == "r":  # Rook movement
            if start_row == end_row or start_col == end_col:
                return not self.is_blocked(start, end)
        
        elif piece_type == "n":  # Knight movement
            if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]:
                return True
        
        elif piece_type == "b":  # Bishop movement
            if abs(start_row - end_row) == abs(start_col - end_col):
                return not self.is_blocked(start, end)
        
        elif piece_type == "q":  # Queen movement
            if (start_row == end_row or start_col == end_col) or (abs(start_row - end_row) == abs(start_col - end_col)):
                return not self.is_blocked(start, end)
        
        elif piece_type == "k":  # King movement
            if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
                return True
        
        return False
    
    def is_blocked(self, start, end):
        """ Check if there are pieces in the path from start to end """
        start_row, start_col = start
        end_row, end_col = end
        step_row = (end_row - start_row) // max(1, abs(end_row - start_row)) if start_row != end_row else 0
        step_col = (end_col - start_col) // max(1, abs(end_col - start_col)) if start_col != end_col else 0
        curr_row, curr_col = start_row + step_row, start_col + step_col
        
        while (curr_row, curr_col) != (end_row, end_col):
            if (curr_row, curr_col) in self.pieces:
                return True
            curr_row += step_row
            curr_col += step_col
        return False

# Run the application
if __name__ == "__main__":
    app = ChessGame()
    app.mainloop()
