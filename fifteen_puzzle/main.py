from helpers import read_board
from board import Board
from search_methods import SearchMethod

def solve_puzzle(board: Board, search_strategy: str = "LRUD"):
    """
    Solve the puzzle using BFS and print the board after each move
    
    Args:
        board: Initial board state
        search_strategy: String of letters representing search order (e.g., "LRUD" for Left-Right-Up-Down)
    """
    search_method = SearchMethod(search_strategy)
    print(f"Initial board state:")
    print(board)
    print(f"Empty position: {board.empty_position}")
    print("\nStarting search with strategy: {search_strategy}")
    print("=" * 40)
    print()
    
    # Use BFS to solve the puzzle
    solution = search_method.bfs(board)
    
    if solution:
        print("\n" + "=" * 40)
        print(f"Puzzle solved!")
        print(f"Final board state:")
        print(solution)
        print(f"\nSearch statistics:")
        print(f"Total board states explored: {search_method.moves_count}")
        print(f"Total empty space moves: {search_method.empty_moves_count}")
        print(f"Average branching factor: {search_method.empty_moves_count / search_method.moves_count:.2f}")
    else:
        print("\n" + "=" * 40)
        print(f"No solution found within the explored states.")
        print(f"\nSearch statistics:")
        print(f"Total board states explored: {search_method.moves_count}")
        print(f"Total empty space moves: {search_method.empty_moves_count}")
        print(f"Average branching factor: {search_method.empty_moves_count / search_method.moves_count:.2f}")

# Example usage:
if __name__ == "__main__":
    # Example board initialization
    initial_state = read_board("example_input.txt")
    
    board = Board(initial_state)
    solve_puzzle(board, "LRUD")
