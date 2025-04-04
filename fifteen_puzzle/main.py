from helpers import read_board

class PuzzleElement:
    def __init__(self, value: int):
        self.value = value
    
    def is_empty(self) -> bool:
        """Check if the element is an empty space (represented by 0)"""
        return self.value == 0
    
    def __str__(self) -> str:
        """String representation of the element"""
        return str(self.value) if not self.is_empty() else " "

class Board:
    def __init__(self, elements: list[list[int]]):
        """Initialize board from 2D array of integers"""
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
        """Get element at specified position"""
        return self.board[row][col]
    
    def __str__(self) -> str:
        """String representation of the board"""
        result = []
        for row in self.board:
            row_str = " ".join(str(element).rjust(2) for element in row)
            result.append(row_str)
        return "\n".join(result)

# Example usage:
if __name__ == "__main__":
    # Example board initialization
    initial_state = read_board("example_input.txt")
    print(initial_state)
    
    board = Board(initial_state)
    print("Initial board state:")
    print(board)
