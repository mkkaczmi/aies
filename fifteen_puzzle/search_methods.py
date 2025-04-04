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
        self.moves_count = 0
        self.empty_moves_count = 0
    
    def bfs(self, initial_board: Board) -> Optional[Board]:
        """Breadth-First Search implementation"""
        queue = deque([(initial_board, [])])
        visited = set([initial_board.get_state_key()])
        
        while queue:
            current_board, path = queue.popleft()
            self.moves_count += 1
            
            # Debug printing
            if self.moves_count % 100 == 0:
                print(f"Exploring state #{self.moves_count}")
                print(current_board)
                print("-" * 40)
            
            if current_board.is_solved():
                return current_board
            
            possible_moves = current_board.get_possible_moves(self.search_strategy)
            print(f"Possible moves from {current_board.empty_position}: {possible_moves}")
            
            for new_empty_pos in possible_moves:
                new_board = current_board.make_move(new_empty_pos)
                new_state = new_board.get_state_key()
                
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_board, path + [new_empty_pos]))
                    self.empty_moves_count += 1
                    
                    # Debug printing
                    print(f"New state found (move empty to {new_empty_pos}):")
                    print(new_board)
                    print("-" * 20)
        
        return None
    
    def dfs(self, initial_board: Board, depth_limit: int = 100) -> Optional[Board]:
        """Depth-First Search implementation with depth limit"""
        stack = [(initial_board, 0)]
        visited = set([initial_board.get_state_key()])
        
        while stack:
            current_board, depth = stack.pop()
            self.moves_count += 1
            
            if current_board.is_solved():
                return current_board
            
            if depth >= depth_limit:
                continue
            
            # Reverse the moves to match the search strategy order when popping from stack
            possible_moves = current_board.get_possible_moves(self.search_strategy)
            for new_empty_pos in reversed(possible_moves):
                new_board = current_board.make_move(new_empty_pos)
                new_state = new_board.get_state_key()
                
                if new_state not in visited:
                    visited.add(new_state)
                    stack.append((new_board, depth + 1))
                    self.empty_moves_count += 1
        
        return None
