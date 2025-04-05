from collections import deque
from typing import List, Tuple, Set, Optional, Callable
from board import Board

class SearchMethod:
    def __init__(self, search_strategy: str):
        """
        Initialize search method with a search strategy.
        
        Args:
            search_strategy: String of letters representing search order (e.g., "LRUD" for Left-Right-Up-Down)
        """
        self.search_strategy = search_strategy.upper()
        self.visited_count = 0      # Number of states visited (added to visited set)
        self.processed_count = 0    # Number of states processed (popped from queue/stack)
        self.max_depth = 0          # Maximum recursion depth reached
    
    def bfs(self, initial_board: Board) -> Tuple[Optional[Board], List[Tuple[int, int]]]:
        """
        Breadth-First Search implementation
        
        Args:
            initial_board: The starting board state
            
        Returns:
            Tuple of (solved board state or None if no solution is found, path to solution)
        """
        queue = deque([(initial_board, [], 0)])  # (board, path, depth)
        visited = set([initial_board.get_state_key()])
        self.visited_count = 1
        self.processed_count = 0
        self.max_depth = 0
        
        while queue:
            current_board, path, depth = queue.popleft()
            self.processed_count += 1
            self.max_depth = max(self.max_depth, depth)
            
            # Debug printing (optional)
            if self.processed_count % 1000 == 0:
                print(f"Processed {self.processed_count} states, current depth: {depth}")
            
            if current_board.is_solved():
                return current_board, path
            
            possible_moves = current_board.get_possible_moves(self.search_strategy)
            
            for new_empty_pos in possible_moves:
                new_board = current_board.make_move(new_empty_pos)
                new_state = new_board.get_state_key()
                
                if new_state not in visited:
                    visited.add(new_state)
                    self.visited_count += 1
                    queue.append((new_board, path + [new_empty_pos], depth + 1))
        
        return None, []
    
    def dfs(self, initial_board: Board, depth_limit: int = 50000) -> Tuple[Optional[Board], List[Tuple[int, int]]]:
        """
        Optimized Depth-First Search implementation with depth limit.
        
        Args:
            initial_board: The starting board state
            depth_limit: Maximum depth to explore (minimum 20)
            
        Returns:
            Tuple of (solved board state or None if no solution is found, path to solution)
        """
        # Ensure minimum depth limit of 20
        depth_limit = max(20, depth_limit)
        
        # Initialize stack with the initial board, its path, and depth
        stack = [(initial_board, [], 0)]  # (board, path, depth)
        
        # Use a set for visited states for efficient look-up
        visited = set([initial_board.get_state_key()])
        self.visited_count = 1
        self.processed_count = 0
        self.max_depth = 0
        
        while stack:
            current_board, path, depth = stack.pop()
            self.processed_count += 1
            self.max_depth = max(self.max_depth, depth)
            
            # Debug print for monitoring progress (optional)
            if self.processed_count % 1000 == 0:
                print(f"Processed {self.processed_count} states, current depth: {depth}")
            
            # Check if the current board is solved
            if current_board.is_solved():
                return current_board, path
            
            # If we've reached the depth limit, backtrack
            if depth >= depth_limit:
                continue
            
            # Get possible moves (no need to reverse them manually later)
            possible_moves = current_board.get_possible_moves(self.search_strategy)
            
            # Reuse the current path and only add new valid moves
            for new_empty_pos in possible_moves:
                new_board = current_board.make_move(new_empty_pos)
                new_state = new_board.get_state_key()
                
                # Only explore the new state if it's unvisited
                if new_state not in visited:
                    visited.add(new_state)
                    self.visited_count += 1
                    # Append to the stack with updated path
                    stack.append((new_board, path + [new_empty_pos], depth + 1))
        
        # No solution found within the given depth limit
        return None, []

