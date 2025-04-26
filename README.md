# Artificial Intelligence and Expert Systems

This repository contains implementations of various artificial intelligence algorithms and expert systems, with a focus on search methods and problem-solving techniques.

## Project Structure

### Fifteen Puzzle Solver
The main project in this repository is a Fifteen Puzzle solver that implements various search algorithms to find solutions to the classic sliding puzzle game.

#### Directory Structure
- `fifteen_puzzle/` - Main project directory
  - `board.py` - Implementation of the Fifteen Puzzle board
  - `search_methods.py` - Various search algorithms implementation
  - `main.py` - Main program entry point
  - `helpers.py` - Utility functions
  - `analyze.py` - Analysis tools for comparing search methods
  - `requirements.txt` - Python dependencies
  - `dataset/` - Contains puzzle instances
  - `analysis_results/` - Results from algorithm analysis
  - `data/` - Additional data files

#### Features
- Multiple search algorithm implementations
- Performance analysis tools
- Dataset of puzzle instances
- Visualization and statistics generation

## Requirements
- Python 3.x
- Dependencies listed in `fifteen_puzzle/requirements.txt`

## Usage
1. Navigate to the `fifteen_puzzle` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Run the main program: `python main.py`

For detailed usage instructions and analysis tools, refer to the README.md in the `fifteen_puzzle` directory.

## License
This project is open source and available under the MIT License.
