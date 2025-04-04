import time
from typing import List, Tuple

def read_board(filename: str) -> List[List[int]]:
    """
    Read a board from a file.
    
    Args:
        filename: Path to the file containing the board.
        
    Returns:
        2D list of integers representing the board.
    """
    try:
        with open(filename, 'r') as file:
            # Wczytaj pierwszą linię z wymiarami
            w, k = map(int, file.readline().split())
            
            # Wczytaj planszę
            board = []
            for _ in range(w):
                # Wczytaj linię, podziel na liczby i przekonwertuj na int
                row = list(map(int, file.readline().split()))
                if len(row) != k:
                    raise ValueError("Nieprawidłowa liczba elementów w wierszu")
                board.append(row)
            
            # Sprawdź czy jest dokładnie jedno zero
            zero_count = sum(row.count(0) for row in board)
            if zero_count != 1:
                raise ValueError("Układanka musi zawierać dokładnie jedno pole puste (0)")
                
            return board
            
    except FileNotFoundError:
        print(f"Błąd: Plik '{filename}' nie został znaleziony")
        return None
    except ValueError as e:
        print(f"Błąd: {str(e)}")
        return None

def write_solution_file(solution_path: List[Tuple[int, int]], initial_empty_pos: Tuple[int, int], filename: str):
    """
    Write the solution to a file.
    
    Args:
        solution_path: List of positions representing the solution path.
        initial_empty_pos: Initial position of the empty space.
        filename: Path to the file where the solution should be saved.
    """
    # Generate solution path as sequence of moves
    moves_sequence = []
    if solution_path:
        prev_pos = initial_empty_pos
        for curr_pos in solution_path:
            # Determine direction of move
            if curr_pos[0] < prev_pos[0]:  # Moving up
                moves_sequence.append('U')
            elif curr_pos[0] > prev_pos[0]:  # Moving down
                moves_sequence.append('D')
            elif curr_pos[1] < prev_pos[1]:  # Moving left
                moves_sequence.append('L')
            elif curr_pos[1] > prev_pos[1]:  # Moving right
                moves_sequence.append('R')
            prev_pos = curr_pos
    
    # Write solution file
    with open(filename, 'w') as f:
        if moves_sequence:
            f.write(f"{len(moves_sequence)}\n")
            f.write("".join(moves_sequence))
        else:
            f.write("-1")
    
    return moves_sequence

def write_info_file(moves_sequence: List[str], visited_count: int, processed_count: int, 
                   max_depth: int, duration_ms: float, filename: str):
    """
    Write the additional information to a file.
    
    Args:
        moves_sequence: List of moves in the solution.
        visited_count: Number of states visited.
        processed_count: Number of states processed.
        max_depth: Maximum recursion depth reached.
        duration_ms: Duration of the search in milliseconds.
        filename: Path to the file where the info should be saved.
    """
    with open(filename, 'w') as f:
        f.write(f"{len(moves_sequence) if moves_sequence else -1}\n")
        f.write(f"{visited_count}\n")
        f.write(f"{processed_count}\n")
        f.write(f"{max_depth}\n")
        f.write(f"{duration_ms:.3f}")

def time_execution(func):
    """
    Decorator to measure execution time.
    
    Args:
        func: The function to measure.
    
    Returns:
        A wrapper function that measures the execution time of func.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000  # Convert to milliseconds
        return result, duration_ms
    return wrapper

def print_search_summary(solution_found: bool, solution_path: List[str] = None, 
                         visited_count: int = 0, processed_count: int = 0, 
                         max_depth: int = 0, duration_ms: float = 0):
    """
    Print a summary of the search process.
    
    Args:
        solution_found: Whether a solution was found.
        solution_path: The path to the solution.
        visited_count: Number of states visited.
        processed_count: Number of states processed.
        max_depth: Maximum recursion depth reached.
        duration_ms: Duration of the search in milliseconds.
    """
    print("\n" + "=" * 40)
    if solution_found:
        print(f"Puzzle solved!")
        print(f"Solution length: {len(solution_path)}")
        print(f"Solution path: {''.join(solution_path)}")
    else:
        print(f"No solution found.")
    
    print(f"\nSearch statistics:")
    print(f"States visited: {visited_count}")
    print(f"States processed: {processed_count}")
    print(f"Maximum depth: {max_depth}")
    print(f"Duration: {duration_ms:.3f} ms")