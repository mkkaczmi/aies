from collections import deque
from typing import List, Tuple, Set, Optional, Callable
from board import Board
import heapq

class SearchMethod:
    def __init__(self, search_strategy: str):
        self.search_strategy = search_strategy.upper()
        self.visited_count = 0      # Number of states visited (added to visited set)
        self.processed_count = 0    # Number of states processed (popped from queue/stack)
        self.max_depth = 0          # Maximum recursion depth reached
    
    def bfs(self, initial_board: Board) -> Tuple[Optional[Board], List[Tuple[int, int]]]:
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
    
    def hamming_distance(self, board: Board) -> int:
        distance = 0
        expected_value = 1
        
        for i in range(board.height):
            for j in range(board.width):
                if i == board.height - 1 and j == board.width - 1:
                    # Last position should be empty
                    if not board.get_element(i, j).is_empty():
                        distance += 1
                else:
                    if board.get_element(i, j).value != expected_value:
                        distance += 1
                    expected_value += 1
        
        return distance
    
    def manhattan_distance(self, board: Board) -> int:
        distance = 0
        
        for i in range(board.height):
            for j in range(board.width):
                value = board.get_element(i, j).value
                if value == 0:  # Skip empty tile
                    continue
                
                # Calculate expected position for this value
                expected_row = (value - 1) // board.width
                expected_col = (value - 1) % board.width
                
                # Add Manhattan distance for this tile
                distance += abs(i - expected_row) + abs(j - expected_col)
        
        return distance
    
    def a_star(self, initial_board: Board) -> Tuple[Optional[Board], List[Tuple[int, int]]]:
        # Determine which heuristic to use
        if self.search_strategy.lower() == "manh":
            heuristic = self.manhattan_distance
        elif self.search_strategy.lower() == "hamm":
            heuristic = self.hamming_distance
        else:
            raise ValueError("A* search requires 'manh' or 'hamm' as search strategy")
        
        # Initialize priority queue with (f_score, counter, board, path, g_score)
        # counter is used to break ties when f_scores are equal
        initial_f_score = heuristic(initial_board)
        counter = 0
        priority_queue = [(initial_f_score, counter, initial_board, [], 0)]
        heapq.heapify(priority_queue)
        
        # Track visited states and their g_scores
        visited = {initial_board.get_state_key(): 0}
        self.visited_count = 1
        self.processed_count = 0
        self.max_depth = 0
        
        while priority_queue:
            f_score, _, current_board, path, g_score = heapq.heappop(priority_queue)
            self.processed_count += 1
            self.max_depth = max(self.max_depth, len(path))
            
            # Debug printing (optional)
            if self.processed_count % 1000 == 0:
                print(f"Processed {self.processed_count} states, current depth: {len(path)}")
            
            if current_board.is_solved():
                return current_board, path
            
            possible_moves = current_board.get_possible_moves("LRUD")  # Use all directions for A*
            
            for new_empty_pos in possible_moves:
                new_board = current_board.make_move(new_empty_pos)
                new_state = new_board.get_state_key()
                new_g_score = g_score + 1
                
                # Only explore if this path is better than any previous path to this state
                if new_state not in visited or new_g_score < visited[new_state]:
                    visited[new_state] = new_g_score
                    self.visited_count += 1
                    
                    # Calculate f_score for the new state
                    new_f_score = new_g_score + heuristic(new_board)
                    
                    # Increment counter to ensure unique ordering
                    counter += 1
                    
                    # Add to priority queue with counter to break ties
                    heapq.heappush(priority_queue, (new_f_score, counter, new_board, path + [new_empty_pos], new_g_score))
        
        return None, []

