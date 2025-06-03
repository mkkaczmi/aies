# Neural Network for Robot Position Correction

This project implements a neural network-based solution for correcting robot position measurements. The system uses a feedforward neural network to learn the relationship between measured coordinates and their corresponding reference positions, improving the accuracy of robot position tracking.

## Project Structure

- `main.py` - Core implementation of the neural network and data processing
- `visualization.py` - Tools for visualizing results and error analysis
- `dataset/` - Contains measurement data
  - `F8/` - Data for F8 robot configuration
  - `F10/` - Data for F10 robot configuration

## Features

- Neural network-based position correction
- Support for multiple robot configurations (F8 and F10)
- Data normalization and preprocessing
- Comprehensive error analysis
- Visualization tools for:
  - Robot trajectory comparison
  - Error distribution analysis
- Results export to Excel format

## Requirements

- Python 3.x
- TensorFlow
- Pandas
- NumPy
- Matplotlib
- XlsxWriter

## Usage

1. Ensure your dataset is properly organized in the `dataset` directory:
   - Static measurement files: `{f8/f10}_stat_*.xlsx`
   - Verification files: `{f8/f10}_1z.xlsx` and `{f8/f10}_1p.xlsx`

2. Run the main processing script:
   ```bash
   python main.py
   ```

3. Generate visualizations:
   ```bash
   python visualization.py
   ```

## Output

The program generates:
- Excel files with results (`resultF8.xlsx`, `resultF10.xlsx`)
- Visualization plots:
  - Trajectory comparison (`*_trajektoria.png`)
  - Error analysis (`*_bledy.png`)

## Neural Network Architecture

- Input layer: 2 neurons (x, y coordinates)
- Hidden layers: [32, 64, 32, 16] neurons with ReLU activation
- Output layer: 2 neurons (corrected x, y coordinates) with sigmoid activation
- Training parameters:
  - Batch size: 512
  - Epochs: 50
  - Optimizer: Adam
  - Loss function: Mean Squared Error

## Data Processing

- Data normalization using offset and scaling factor
- 90/10 split for training/validation
- Support for both static and verification measurements
- Error calculation and analysis
