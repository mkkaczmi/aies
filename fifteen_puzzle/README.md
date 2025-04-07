# Fifteen Puzzle Solver

This project contains a solution for the Fifteen Puzzle problem and analysis tools for evaluating different solving methods.

## Prerequisites

1. Download and install [Azul Zulu Java 8 JRE with JavaFX](https://www.azul.com/downloads/?version=java-8-lts&architecture=x86-64-bit&package=jre-fx#zulu)
   - This specific Java distribution is required as it includes JavaFX components

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

## Setup Instructions

1. After installing Java, you need to modify the following PowerShell scripts in the `dataset` directory to point to your Java installation:
   - `puzzlegen.ps1`
   - `runval.ps1`
   
   In both files, update the path to `java.exe` to match your installation location. The default path in the scripts is:
   ```
   "C:\Program Files\zulu8.84.0.15-ca-fx-jre8.0.442-win_x64\bin\java.exe"
   ```

## Usage

1. Generate puzzles by running:
   ```
   .\dataset\puzzlegen.ps1
   ```

2. Generate solutions by running:
   ```
   .\dataset\generate_solutions.ps1
   ```

3. Validate your solution using:
   ```
   .\dataset\runval.ps1
   ```

All scripts are located in the `dataset` directory.

## Analysis

After generating solutions, you can analyze the performance of different solving methods using the analysis script:

```
python analyze.py
```

This will create an `analysis_results` directory containing:

### Statistical Analysis Files
- `statistics.csv`: Basic statistics for each metric
- `success_rate.csv`: Success rates by method and strategy
- `method_statistics.csv`: Detailed statistics per method
- `strategy_statistics.csv`: Detailed statistics per strategy
- Additional metric-specific statistics in both CSV and TXT formats

### Visualizations
- Boxplots with logarithmic scale for:
  - Solution length
  - Number of visited states
  - Number of processed states
  - Maximum recursion depth
  - Computation time
- Heatmaps comparing methods and strategies for each metric

The analysis includes:
- Basic statistics (mean, median, std, min/max)
- Success rates
- Performance efficiency metrics
- Statistical significance tests
- Distribution analysis
- Correlation analysis between metrics

The visualizations are designed to handle the large scale differences between methods (particularly DFS vs others) using logarithmic scales where appropriate.