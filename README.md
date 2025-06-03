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

### Neural Network for Robot Position Correction
A neural network-based solution for improving robot position measurements accuracy.

#### Directory Structure
- `neural_network/` - Neural network project directory
  - `main.py` - Core implementation of the neural network
  - `visualization.py` - Results visualization tools
  - `dataset/` - Contains robot measurement data
    - `F8/` - F8 robot configuration data
    - `F10/` - F10 robot configuration data

## Requirements
- Python 3.x
- Dependencies listed in respective project directories' `requirements.txt` files

## Usage

### Fifteen Puzzle Solver
1. Navigate to the `fifteen_puzzle` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Run the main program: `python main.py`

### Neural Network Project
1. Navigate to the `neural_network` directory
2. Install dependencies: `pip install -r requirements.txt`
3. Run the main program: `python main.py`
4. Generate visualizations: `python visualization.py`

For detailed usage instructions and analysis tools, refer to the README.md files in respective project directories.

## License
This project is open source and available under the MIT License.
