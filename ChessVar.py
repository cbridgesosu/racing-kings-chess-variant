"""
Racing Kings - A Chess Variant

This file contains the core implementation for the Racing Kings chess variant, including classes
that define the game board, pieces, and game rules. The objective of Racing Kings is for each
player's king to reach the first row of the opposing player's side of the board.

Classes:
- Piece: Base class for all chess pieces (King, Rook, Bishop, Knight).
- King: Class for the King piece, with specific movement logic and check detection.
- Rook: Class for the Rook piece, with movement logic for horizontal and vertical paths.
- Bishop: Class for the Bishop piece, with movement logic for diagonal paths.
- Knight: Class for the Knight piece, with movement logic for an "L" shape.
- ChessBoard: Class that manages the board, spaces, and piece placement.
- ChessVar: Class to manage the Racing Kings variant game state, including player turns,
  piece movement, and game conditions.

Usage:
- Instantiate the ChessVar class to begin a game.
- Use the make_move method to move pieces on the board.
- Check game state via the get_game_state method, which will return the result ("WHITE_WON", "BLACK_WON", "TIE", "UNFINISHED").

Notes:
- The game logic assumes an 8x8 board, with pieces starting in a specific arrangement.
- The 'king' must reach the opposite player's first row to win the game.
- The game uses a turn-based system where players alternate between "WHITE" and "BLACK".

Author: Chris Bridges
Date: 2/17/2025

"""


class ChessVar:
    """Class to define a chess variant board game with board, pieces, and game control."""
    def __init__(self):
        # Initialize the game with an empty chess board, set last turn as False, no winner yet, and the game state as unfinished
        self._board = ChessBoard()
        self._last_turn = False
        self._game_won = False
        self._turn = "WHITE"  # The starting player is white
        self._game_state = "UNFINISHED"

        # Create chess pieces for both players
        self._pieces = {"WHITE": self.gen_pieces("WHITE"), "BLACK": self.gen_pieces("BLACK")}

        # Populate the board with the pieces for each color
        for color in self._pieces:
            for piece in self._pieces[color]:
                position = self._pieces[color][piece].get_position()
                position.set_piece(self._pieces[color][piece])

    def gen_pieces(self, color):
        """Generates the starting set of chess pieces for a player color."""
        # Define starting locations based on player color
        if color == "WHITE":
            location = ["a1", "a2", "b1", "b2", "c1", "c2"]
        else:
            location = ["h1", "h2", "g1", "g2", "f1", "f2"]

        # Create pieces for the color and assign them to respective starting positions
        king = King(color, self._board.get_spaces()[location[0]])
        rook = Rook(color, self._board.get_spaces()[location[1]])
        bishop_1 = Bishop(color, self._board.get_spaces()[location[2]])
        bishop_2 = Bishop(color, self._board.get_spaces()[location[3]])
        knight_1 = Knight(color, self._board.get_spaces()[location[4]])
        knight_2 = Knight(color, self._board.get_spaces()[location[5]])

        # Return a dictionary of the pieces for the player
        pieces = {"king": king,
                  "rook": rook,
                  "bishop_1": bishop_1,
                  "bishop_2": bishop_2,
                  "knight_1": knight_1,
                  "knight_2": knight_2,
                  }

        return pieces

    def get_game_state(self):
        """Returns the current state of a game."""
        return self._game_state

    def update_game_state(self):
        """Updates the current status of the game based upon the most recent valid player move."""
        # Check the positions of both kings (white and black)
        black = self._pieces["BLACK"]["king"].get_position().get_label()
        white = self._pieces["WHITE"]["king"].get_position().get_label()

        # If white's king reaches the last row, the game may be won
        if self._board.get_spaces()[white].get_row_index() == 0 and self._board.get_spaces()[black].get_row_index() != 0:
            if self._last_turn:
                self._game_won = True
                self._game_state = "WHITE_WON"
                return "WHITE_WON"
            else:
                self._last_turn = True
            return "UNFINISHED"
        # If both kings reach the last row, the game is a tie
        elif self._board.get_spaces()[white].get_row_index() == 0 and self._board.get_spaces()[black].get_row_index() == 0:
            self._game_state = "TIE"
            return "TIE"
        # If black's king reaches the last row, black wins
        elif self._board.get_spaces()[black].get_row_index() == 0:
            self._game_won = True
            self._game_state = "BLACK_WON"
            return "BLACK_WON"
        else:
            return "UNFINISHED"

    def make_move(self, start, end):
        """Moves a piece from the start location to end location and captures enemy piece if possible."""
        start = self._board.get_spaces()[start]  # Get the starting position
        player_piece = start.get_piece()  # Get the piece at the starting position
        destination = self._board.get_spaces()[end]  # Get the destination position
        opponent_piece = destination.get_piece()  # Get the piece at the destination position

        # Ensure the piece belongs to the current player
        if player_piece:
            if player_piece.get_color() != self._turn:
                return False  # Return false if it is not the current player's turn

        if self._game_won:
            return False  # Game is over

        if not player_piece:
            return False  # No piece to move

        if opponent_piece:
            if player_piece.get_color() == opponent_piece.get_color():
                return False  # Can't capture own piece

            moves = player_piece.moves(start)  # Get the valid moves for the piece
            if destination in moves:  # If the move is valid, make the move
                player_piece.set_position(destination)
                destination.set_piece(player_piece)
                start.set_piece(None)  # Remove the piece from the starting position

                # Check for check after the move for both players
                if self._pieces["WHITE"]["king"].is_check(self._pieces):
                    player_piece.set_position(start)
                    destination.set_piece(opponent_piece)
                    start.set_piece(player_piece)
                    return False
                if self._pieces["BLACK"]["king"].is_check(self._pieces):
                    player_piece.set_position(start)
                    destination.set_piece(opponent_piece)
                    start.set_piece(player_piece)
                    return False

                self.update_game_state()  # Update the game state
                self.change_turn()  # Change the turn
                return True  # Move was successful
            return False  # Move was invalid

        if not opponent_piece:
            moves = player_piece.moves(start)  # Get the valid moves for the piece
            if destination in moves:  # If the move is valid, make the move
                player_piece.set_position(destination)
                destination.set_piece(player_piece)
                start.set_piece(None)  # Remove the piece from the starting position

                # Check for check after the move for both players
                if self._pieces["WHITE"]["king"].is_check(self._pieces):
                    player_piece.set_position(start)
                    destination.set_piece(opponent_piece)
                    start.set_piece(player_piece)
                    return False
                if self._pieces["BLACK"]["king"].is_check(self._pieces):
                    player_piece.set_position(start)
                    destination.set_piece(opponent_piece)
                    start.set_piece(player_piece)
                    return False

                self.update_game_state()  # Update the game state
                self.change_turn()  # Change the turn
                return True  # Move was successful
            return False  # Move was invalid

    def change_turn(self):
        """Updates the turn from the current to opposing player color."""
        if self._turn == "WHITE":
            self._turn = "BLACK"
        else:
            self._turn = "WHITE"

    def print_board(self):
        """Displays the current game board layout."""
        rows = [8, 7, 6, 5, 4, 3, 2, 1]  # Row numbers for the chessboard
        columns = ["a", "b", "c", "d", "e", "f", "g", "h"]  # Column letters for the chessboard
        self._spaces = {}

        # Iterate through each row and column to print the board layout
        for row in rows:
            print("|", end="")
            for column in columns:
                if self._board.get_spaces()[f"{column}{row}"].get_piece():
                    name = self._board.get_spaces()[f"{column}{row}"].get_piece().get_name()
                    print(f"{name}" + "|", end="")
                else:
                    print(f"  " + "|", end="")
            print()
        print()  # Print a newline for better readability


class ChessBoard:
    """Creates game board with space references to be used by the ChessVar class."""
    def __init__(self):
        # Initialize the rows and columns of the board
        rows = [8, 7, 6, 5, 4, 3, 2, 1]
        columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self._spaces = {}

        # Create board game spaces (all 64 spaces) and map each space label to a BoardSpace object
        for r_index, row in enumerate(rows):
            for c_index, column in enumerate(columns):
                label = f"{column}{row}"
                self._spaces[label] = BoardSpace(r_index, c_index, label)

        # Link the spaces to each other in all 8 possible directions (up, down, left, right, etc.)
        for space in self._spaces:
            space = self._spaces[space]  # Get the current space object
            r_index = space.get_row_index()
            c_index = space.get_col_index()

            # Link to the space below
            if r_index < 7:
                space.set_down(self._spaces[f"{columns[c_index]}{rows[r_index + 1]}"])

            # Link to the space to the right
            if c_index < 7:
                space.set_right(self._spaces[f"{columns[c_index + 1]}{rows[r_index]}"])

            # Link to the space diagonally down-right
            if r_index < 7 and c_index < 7:
                space.set_downright(self._spaces[f"{columns[c_index + 1]}{rows[r_index + 1]}"])

            # Link to the space above
            if r_index > 0 and c_index > 0:
                space.set_up(self._spaces[f"{columns[c_index]}{rows[r_index - 1]}"])
                space.set_left(self._spaces[f"{columns[c_index - 1]}{rows[r_index]}"])
                space.set_upleft(self._spaces[f"{columns[c_index - 1]}{rows[r_index - 1]}"])

            # Link to the space above-left
            if r_index > 0:
                space.set_up(self._spaces[f"{columns[c_index]}{rows[r_index - 1]}"])

            # Link to the space left
            if c_index > 0:
                space.set_left(self._spaces[f"{columns[c_index - 1]}{rows[r_index]}"])

            # Link to the space diagonally up-left
            if r_index > 0 and c_index > 0:
                space.set_upleft(self._spaces[f"{columns[c_index - 1]}{rows[r_index - 1]}"])

            # Link to the space diagonally up-right
            if r_index > 0 and c_index < 7:
                space.set_upright(self._spaces[f"{columns[c_index + 1]}{rows[r_index - 1]}"])

            # Link to the space diagonally down-left
            if r_index < 7 and c_index > 0:
                space.set_downleft(self._spaces[f"{columns[c_index - 1]}{rows[r_index + 1]}"])

    def get_spaces(self):
        """Returns a dictionary of all spaces on the game board."""
        return self._spaces

class BoardSpace:
    """Creates a space object to be used by the ChessBoard class."""
    def __init__(self, row_index, column_index, label):
        # Initialize the space with row, column, and label
        self._row_index = row_index
        self._col_index = column_index
        self._label = label
        self._piece = None  # Initially, no piece is placed on this space

        # Initialize the connections to adjacent spaces (all 8 directions)
        self._up = None
        self._down = None
        self._left = None
        self._right = None
        self._upleft = None
        self._upright = None
        self._downleft = None
        self._downright = None

    # Getter methods for row index, column index, and space label
    def get_row_index(self):
        return self._row_index

    def get_col_index(self):
        return self._col_index

    def get_label(self):
        return self._label

    # Getter methods for the adjacent spaces (in all 8 directions)
    def get_up(self):
        return self._up

    def get_down(self):
        return self._down

    def get_left(self):
        return self._left

    def get_right(self):
        return self._right

    def get_upleft(self):
        return self._upleft

    def get_upright(self):
        return self._upright

    def get_downleft(self):
        return self._downleft

    def get_downright(self):
        return self._downright

    # Getter and setter methods for the piece on this space
    def get_piece(self):
        return self._piece

    def set_piece(self, piece):
        self._piece = piece

    # Setter methods for linking adjacent spaces
    def set_up(self, space):
        self._up = space

    def set_down(self, space):
        self._down = space

    def set_left(self, space):
        self._left = space

    def set_right(self, space):
        self._right = space

    def set_upleft(self, space):
        self._upleft = space

    def set_upright(self, space):
        self._upright = space

    def set_downleft(self, space):
        self._downleft = space

    def set_downright(self, space):
        self._downright = space

class Piece:
    """Creates a generic chess piece."""
    def __init__(self, color, position):
        # Initialize the piece with its color and position on the board
        self._color = color
        self._position = position

    # Getter methods for position and color of the piece
    def get_position(self):
        return self._position

    def get_color(self):
        return self._color

    # Setter method for changing the piece's position
    def set_position(self, space):
        self._position = space

class King(Piece):
    """Creates a king class piece."""
    def __init__(self, color, position):
        # Initialize the king piece with color and position
        super().__init__(color, position)
        self._name = f"{color[0]}k"  # King's name format (e.g., "wk" or "bk")

    # Getter method for king's name
    def get_name(self):
        return self._name

    # Method to return a list of valid moves for the king
    def moves(self, current_position):
        row = current_position.get_row_index()
        column = current_position.get_col_index()

        moves = []
        # Check for valid moves in all 8 directions
        if row < 7:
            moves.append(current_position.get_down())
        if row > 0:
            moves.append(current_position.get_up())
        if column > 0:
            moves.append(current_position.get_left())
        if column < 7:
            moves.append(current_position.get_right())
        if row < 7 and column > 0:
            moves.append(current_position.get_downleft())
        if row < 7 and column < 7:
            moves.append(current_position.get_downright())
        if row > 0 and column > 0:
            moves.append(current_position.get_upleft())
        if row > 0 and column < 7:
            moves.append(current_position.get_upright())

        return moves

    # Method to check if the king is in check
    def is_check(self, pieces):
        current_position = self.get_position()

        for color in pieces:
            if color != self.get_color():
                for piece in pieces[color]:
                    if current_position in pieces[color][piece].moves(pieces[color][piece].get_position()):
                        return True
        return False

class Knight(Piece):
    """Creates a knight class piece."""
    def __init__(self, color, position):
        super().__init__(color, position)
        self._name = f"{color[0]}h"

    def get_name(self):
        """Returns name of knight piece for board display."""
        return self._name

    def moves(self, current_position):
        """Returns list of current possible knight moves."""
        row = current_position.get_row_index()
        column = current_position.get_col_index()

        moves = []

        # Possible moves in all 8 directions for the knight
        if (row - 2) >= 0 and (column - 1) >= 0:
            moves.append(current_position.get_left().get_up().get_up())
        if (row - 2) >= 0 and (column + 1) <= 7:
            moves.append(current_position.get_right().get_up().get_up())
        if (row + 2) <= 7 and (column - 1) >= 0:
            moves.append(current_position.get_left().get_down().get_down())
        if (row + 2) <= 7 and (column + 1) <= 7:
            moves.append(current_position.get_right().get_down().get_down())
        if (row - 1) >= 0 and (column - 2) >= 0:
            moves.append(current_position.get_left().get_left().get_up())
        if (row - 1) >= 0 and (column + 2) <= 7:
            moves.append(current_position.get_right().get_right().get_up())
        if (row + 1) <= 7 and (column - 2) >= 0:
            moves.append(current_position.get_left().get_left().get_down())
        if (row + 1) <= 7 and (column + 2) <= 7:
            moves.append(current_position.get_right().get_right().get_down())

        return moves

class Rook(Piece):
    """Creates a rook class piece."""
    def __init__(self, color, position):
        # Initialize the rook piece with color and position
        super().__init__(color, position)
        self._name = f"{color[0]}r"  # Rook's name format (e.g., "wr" or "br")

    def get_name(self):
        """Returns name of rook for board display."""
        return self._name

    def moves(self, current_position):
        """Returns list of current possible rook moves."""
        up = current_position
        down = current_position
        left = current_position
        right = current_position

        color = self.get_color()  # Get the color of the piece

        moves = []

        # Check all 4 directions (up, down, left, right)
        # Up direction: Keep moving up until blocked or edge of board
        while up.get_up():
            if up.get_up().get_piece():
                if up.get_up().get_piece().get_color() != color:
                    moves.append(up.get_up())
                    break
                else:
                    break
            else:
                moves.append(up.get_up())
                up = up.get_up()

        # Left direction: Keep moving left until blocked or edge of board
        while left.get_left():
            if left.get_left().get_piece():
                if left.get_left().get_piece().get_color() != color:
                    moves.append(left.get_left())
                    break
                else:
                    break
            else:
                moves.append(left.get_left())
                left = left.get_left()

        # Right direction: Keep moving right until blocked or edge of board
        while right.get_right():
            if right.get_right().get_piece():
                if right.get_right().get_piece().get_color() != color:
                    moves.append(right.get_right())
                    break
                else:
                    break
            else:
                moves.append(right.get_right())
                right = right.get_right()

        # Down direction: Keep moving down until blocked or edge of board
        while down.get_down():
            if down.get_down().get_piece():
                if down.get_down().get_piece().get_color() != color:
                    moves.append(down.get_down())
                    break
                else:
                    break
            else:
                moves.append(down.get_down())
                down = down.get_down()

        return moves

class Bishop(Piece):
    """Creates a bishop class piece."""
    def __init__(self, color, position):
        # Initialize the bishop piece with color and position
        super().__init__(color, position)
        self._name = f"{color[0]}b"  # Bishop's name format (e.g., "wb" or "bb")

    def get_name(self):
        """Returns name of bishop piece for board display."""
        return self._name

    def moves(self, current_position):
        """Returns list of current possible bishop moves."""
        upleft = current_position
        upright = current_position
        downleft = current_position
        downright = current_position

        color = self.get_color()  # Get the color of the piece

        moves = []

        # Check diagonal directions (upleft, upright, downleft, downright)
        # Upleft direction: Keep moving diagonally up-left until blocked or edge of board
        while upleft.get_upleft():
            if upleft.get_upleft().get_piece():
                if upleft.get_upleft().get_piece().get_color() != color:
                    moves.append(upleft.get_upleft())
                    break
                else:
                    break
            else:
                moves.append(upleft.get_upleft())
                upleft = upleft.get_upleft()

        # Upright direction: Keep moving diagonally up-right until blocked or edge of board
        while upright.get_upright():
            if upright.get_upright().get_piece():
                if upright.get_upright().get_piece().get_color() != color:
                    moves.append(upright.get_upright())
                    break
                else:
                    break
            else:
                moves.append(upright.get_upright())
                upright = upright.get_upright()

        # Downleft direction: Keep moving diagonally down-left until blocked or edge of board
        while downleft.get_downleft():
            if downleft.get_downleft().get_piece():
                if downleft.get_downleft().get_piece().get_color() != color:
                    moves.append(downleft.get_downleft())
                    break
                else:
                    break
            else:
                moves.append(downleft.get_downleft())
                downleft = downleft.get_downleft()

        # Downright direction: Keep moving diagonally down-right until blocked or edge of board
        while downright.get_downright():
            if downright.get_downright().get_piece():
                if downright.get_downright().get_piece().get_color() != color:
                    moves.append(downright.get_downright())
                    break
                else:
                    break
            else:
                moves.append(downright.get_downright())
                downright = downright.get_downright()

        return moves

class Queen(Piece):
    """Creates a queen class piece."""
    def __init__(self, color, position):
        # Initialize the queen piece with color and position
        super().__init__(color, position)
        self._name = f"{color[0]}q"  # Queen's name format (e.g., "wq" or "bq")

    def get_name(self):
        """Returns name of queen piece for board display."""
        return self._name

    def moves(self, current_position):
        """Returns list of current possible queen moves."""
        # A queen moves both as a rook and a bishop
        rook_moves = Rook(self.get_color(), current_position).moves(current_position)
        bishop_moves = Bishop(self.get_color(), current_position).moves(current_position)

        # Combine rook and bishop moves
        return rook_moves + bishop_moves

class Pawn(Piece):
    """Creates a pawn class piece."""
    def __init__(self, color, position):
        # Initialize the pawn piece with color and position
        super().__init__(color, position)
        self._name = f"{color[0]}p"  # Pawn's name format (e.g., "wp" or "bp")

    def get_name(self):
        """Returns name of pawn piece for board display."""
        return self._name

    def moves(self, current_position):
        """Returns list of current possible pawn moves."""
        row = current_position.get_row_index()
        column = current_position.get_col_index()

        moves = []

        # Pawns move differently depending on their color
        # For white pawns (move upwards)
        if self.get_color() == "white":
            if row < 7:  # Ensure it's within bounds
                moves.append(current_position.get_up())  # One step forward
                # If it's on the starting row, it can move two steps
                if row == 1:
                    moves.append(current_position.get_up().get_up())

        # For black pawns (move downwards)
        elif self.get_color() == "black":
            if row > 0:  # Ensure it's within bounds
                moves.append(current_position.get_down())  # One step forward
                # If it's on the starting row, it can move two steps
                if row == 6:
                    moves.append(current_position.get_down().get_down())

        return moves

def main():
    game = ChessVar()
    game.get_game_state()

    game.print_board()
    game.make_move("a2", "a8")
    game.print_board()

    game.make_move("h2", "h8")
    game.print_board()

    game.make_move("a1", "a2")
    game.print_board()

    game.make_move("h1", "h2")
    game.print_board()

    game.make_move("a2", "a3")
    game.print_board()

    game.make_move("h2", "h3")
    game.print_board()

    game.make_move("a3", "a4")
    game.print_board()

    game.make_move("h3", "h4")
    game.print_board()

    game.make_move("a4", "a5")
    game.print_board()

    game.make_move("h4", "h5")
    game.print_board()

    game.make_move("a5", "a6")
    game.print_board()

    game.make_move("h5", "h6")
    game.print_board()

    game.make_move("a6", "a7")
    game.print_board()

    game.make_move("h6", "h7")
    game.print_board()

    game.make_move("a8", "b8")
    game.print_board()

    game.make_move("h8", "g8")
    game.print_board()

    game.make_move("b2", "a3")
    game.print_board()

    game.make_move("g2", "h3")
    game.print_board()

    print(game.get_game_state())

    game.make_move("g2", "h3")
    game.print_board()

    game.make_move("a7", "a6")
    game.print_board()

    print(game.get_game_state())

    game.make_move("h7", "h8")
    game.print_board()

    print(game.get_game_state())

if __name__ == "__main__":
    main()