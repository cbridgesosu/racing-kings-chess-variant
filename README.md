# racing-kings-chess-variant
A chess variant with custom rules where players race their king to the back row.

## Classes

### 1. `ChessVar`
The `ChessVar` class handles the game logic. It manages the state of the game, the players' turns, and determines when the game is over. It includes:
- **Board Setup**: Initializes the board with pieces for both players.
- **Piece Movement**: Handles the logic for making moves, checking if a move is valid, and switching turns.
- **Game State**: Determines if the game is unfinished, if a player has won, or if there is a tie.

### 2. `ChessBoard`
The `ChessBoard` class defines the game board. It contains:
- **Spaces**: Each space on the board is an instance of `BoardSpace`. The board is represented as an 8x8 grid.
- **Linking Spaces**: Each space is linked to its neighboring spaces (up, down, left, right, diagonals).

### 3. `BoardSpace`
The `BoardSpace` class defines the individual spaces on the chessboard. Each space holds:
- **Position**: The position is defined by its row and column indexes and an algebraic label (e.g., `a1`, `h8`).
- **Piece**: Each space can hold a chess piece, or be empty.
- **Neighbors**: Spaces are linked to adjacent spaces in all directions (vertical, horizontal, diagonal).

### 4. `Piece`
The `Piece` class is a base class for all chess pieces. It includes:
- **Color**: The color of the piece (either `WHITE` or `BLACK`).
- **Position**: The position of the piece on the board.
- **Movement**: Each piece class (like `King`, `Knight`, etc.) overrides the `moves` method to specify its valid movements.

### 5. `King`, `Knight`, `Rook`, `Bishop`
These classes represent specific chess pieces, inheriting from the `Piece` class. Each piece has:
- **Name**: A method to return the name for display (e.g., `wK` for White King).
- **Valid Moves**: A `moves` method that returns a list of valid moves based on the piece's movement rules.
- **Special Conditions**: For the King, an additional check for whether the King is in check is implemented.

## Game Flow
1. **Setup**: When the game starts, the board is populated with pieces for both players.
2. **Turns**: Players alternate making moves. The game checks for valid moves and updates the board.
3. **Victory**: The game ends when one player wins (the other player's king is checkmated), or a tie occurs.
4. **Check and Checkmate**: The King class checks whether the king is in check after every move.

## Example Usage

```python
# Initialize the chess game
game = ChessVar()

# Make a move: Player moves from "a2" to "a4"
game.make_move("a2", "a4")

# Print the board
game.print_board()

# Get the current game state
print(game.get_game_state())
