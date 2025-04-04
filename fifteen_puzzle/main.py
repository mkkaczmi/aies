import sys
from helpers import (
    read_board, write_solution_file, write_info_file, 
    time_execution, print_search_summary
)
from board import Board
from search_methods import SearchMethod

@time_execution
def run_search(board: Board, search_method_name: str, search_strategy: str):
    """
    Run the specified search method on the given board.
    
    Args:
        board: Initial board state
        search_method_name: 'bfs' or 'dfs'
        search_strategy: String of letters representing search order
    
    Returns:
        Tuple of (solution board, solution path)
    """
    search_method = SearchMethod(search_strategy)
    
    # Choose search method based on input
    if search_method_name.lower() == 'bfs':
        solution, solution_path = search_method.bfs(board)
    elif search_method_name.lower() == 'dfs':
        # DFS has a minimum depth limit of 20
        solution, solution_path = search_method.dfs(board)
    else:
        raise ValueError(f"Unknown search method: {search_method_name}")
    
    return solution, solution_path, search_method

def solve_puzzle(board: Board, search_method_name: str, search_strategy: str, 
                solution_file: str, info_file: str):
    """
    Solve the puzzle using the specified search method and strategy
    
    Args:
        board: Initial board state
        search_method_name: 'bfs' or 'dfs'
        search_strategy: String of letters representing search order
        solution_file: Path to file where solution should be saved
        info_file: Path to file where additional information should be saved
    """
    print(f"Initial board state:")
    print(board)
    print(f"Empty position: {board.empty_position}")
    print(f"\nRunning {search_method_name.upper()} with strategy: {search_strategy}")
    
    if search_method_name.lower() == 'dfs':
        print("Note: DFS has a minimum depth limit of 20")
    
    print("=" * 40)
    
    # Run search and measure time
    (solution, solution_path, search_method), duration_ms = run_search(board, search_method_name, search_strategy)
    
    # Generate solution file
    moves_sequence = write_solution_file(solution_path, board.empty_position, solution_file)
    
    # Generate additional information file
    write_info_file(
        moves_sequence, 
        search_method.visited_count, 
        search_method.processed_count, 
        search_method.max_depth, 
        duration_ms, 
        info_file
    )
    
    # Print summary
    print_search_summary(
        solution is not None,
        moves_sequence,
        search_method.visited_count,
        search_method.processed_count,
        search_method.max_depth,
        duration_ms
    )

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) != 6:
        print("Usage: python main.py <search_method> <search_strategy> <input_file> <solution_file> <info_file>")
        print("  search_method: 'bfs' or 'dfs'")
        print("  search_strategy: e.g., 'LRUD' for Left-Right-Up-Down")
        print("  input_file: path to file containing initial board state")
        print("  solution_file: path to file where solution will be saved")
        print("  info_file: path to file where additional information will be saved")
        sys.exit(1)
    
    search_method = sys.argv[1]
    search_strategy = sys.argv[2]
    input_file = sys.argv[3]
    solution_file = sys.argv[4]
    info_file = sys.argv[5]
    
    # Check if search method is valid
    if search_method.lower() not in ['bfs', 'dfs']:
        print(f"Invalid search method: {search_method}")
        print("Valid methods are 'bfs' and 'dfs'")
        sys.exit(1)
    
    # Read board from input file
    try:
        initial_state = read_board(input_file)
        board = Board(initial_state)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)
    
    # Solve puzzle and generate output files
    solve_puzzle(board, search_method, search_strategy, solution_file, info_file)
