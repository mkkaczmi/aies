class PuzzleElement:
    def __init__(self, value: int):
        self.value = value
    
    def is_empty(self) -> bool:
        return self.value == 0
    
    def __str__(self) -> str:
        return str(self.value) if not self.is_empty() else " "

class Board:
    def __init__(self, elements: list[list[int]]):
        self.height = len(elements)
        self.width = len(elements[0])
        
        # Validate input dimensions
        if not all(len(row) == self.width for row in elements):
            raise ValueError("All rows must have the same length")
            
        # Create board with PuzzleElements
        self.board = []
        self.empty_position = None
        
        for i, row in enumerate(elements):
            board_row = []
            for j, value in enumerate(row):
                element = PuzzleElement(value)
                board_row.append(element)
                if element.is_empty():
                    self.empty_position = (i, j)
            self.board.append(board_row)
            
        if self.empty_position is None:
            raise ValueError("Board must contain exactly one empty space (0)")
    
    def get_element(self, row: int, col: int) -> PuzzleElement:
        return self.board[row][col]
    
    def __str__(self) -> str:
        result = []
        for row in self.board:
            row_str = " ".join(str(element).rjust(2) for element in row)
            result.append(row_str)
        return "\n".join(result)
    
    def get_possible_moves(self, search_strategy: str = "LRUD") -> list[tuple[int, int]]:
        empty_row, empty_col = self.empty_position
        possible_moves = []
        
        # Define all possible moves
        all_moves = {
            'L': (empty_row, empty_col - 1),  # Left
            'R': (empty_row, empty_col + 1),  # Right
            'U': (empty_row - 1, empty_col),  # Up
            'D': (empty_row + 1, empty_col)   # Down
        }
        
        # Add moves in the order specified by the search strategy
        for direction in search_strategy.upper():
            if direction in all_moves:
                new_row, new_col = all_moves[direction]
                # Check if the move is valid (within board boundaries)
                if 0 <= new_row < self.height and 0 <= new_col < self.width:
                    possible_moves.append((new_row, new_col))
        
        return possible_moves
    
    def make_move(self, new_empty_pos: tuple[int, int]) -> 'Board':
        empty_row, empty_col = self.empty_position
        new_row, new_col = new_empty_pos
        
        # Create a deep copy of the board
        new_elements = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if i == empty_row and j == empty_col:
                    # This is the old empty position, should now contain the value from the new position
                    row.append(self.get_element(new_row, new_col).value)
                elif i == new_row and j == new_col:
                    # This is the new empty position
                    row.append(0)
                else:
                    # Keep the original value
                    row.append(self.get_element(i, j).value)
            new_elements.append(row)
        
        return Board(new_elements)
    
    def is_solved(self) -> bool:
        expected_value = 1
        for i in range(self.height):
            for j in range(self.width):
                if i == self.height - 1 and j == self.width - 1:
                    # Last position should be empty
                    if not self.get_element(i, j).is_empty():
                        return False
                else:
                    if self.get_element(i, j).value != expected_value:
                        return False
                    expected_value += 1
        return True
    
    def get_state_key(self) -> str:
        return str(self) 