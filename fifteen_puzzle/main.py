import sys
from helpers import (
    read_board, write_solution_file, write_info_file, 
    time_execution, print_search_summary
)
from board import Board
from search_methods import SearchMethod

@time_execution
def run_search(board: Board, search_method_name: str, search_strategy: str):
    search_method = SearchMethod(search_strategy)
    
    # Choose search method based on input
    if search_method_name.lower() == 'bfs':
        solution, solution_path = search_method.bfs(board)
    elif search_method_name.lower() == 'dfs':
        # DFS has a minimum depth limit of 20
        solution, solution_path = search_method.dfs(board, depth_limit=20)
    elif search_method_name.lower() == 'astr':
        solution, solution_path = search_method.a_star(board)
    else:
        raise ValueError(f"Unknown search method: {search_method_name}")
    
    return solution, solution_path, search_method

def solve_puzzle(board: Board, search_method_name: str, search_strategy: str, 
                solution_file: str, info_file: str):
    print(f"Initial board state:")
    print(board)
    print(f"Empty position: {board.empty_position}")
    print(f"\nRunning {search_method_name.upper()} with strategy: {search_strategy}")
    
    if search_method_name.lower() == 'dfs':
        print("Note: DFS has a minimum depth limit of 20")
    elif search_method_name.lower() == 'astr':
        if search_strategy.lower() == 'manh':
            print("Using Manhattan distance heuristic")
        elif search_strategy.lower() == 'hamm':
            print("Using Hamming distance heuristic")
    
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
        print("  search_method: 'bfs', 'dfs', or 'astr'")
        print("  search_strategy: e.g., 'LRUD' for Left-Right-Up-Down, or 'manh'/'hamm' for A*")
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
    if search_method.lower() not in ['bfs', 'dfs', 'astr']:
        print(f"Invalid search method: {search_method}")
        print("Valid methods are 'bfs', 'dfs', and 'astr'")
        sys.exit(1)
    
    # Check if search strategy is valid for A*
    if search_method.lower() == 'astr' and search_strategy.lower() not in ['manh', 'hamm']:
        print(f"Invalid search strategy for A*: {search_strategy}")
        print("Valid strategies for A* are 'manh' (Manhattan) and 'hamm' (Hamming)")
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
