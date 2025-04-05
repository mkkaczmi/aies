# Fifteen Puzzle Solver

This project contains a solution for the Fifteen Puzzle problem. Before running the solution, you need to follow these setup steps:

## Prerequisites

1. Download and install [Azul Zulu Java 8 JRE with JavaFX](https://www.azul.com/downloads/?version=java-8-lts&architecture=x86-64-bit&package=jre-fx#zulu)
   - This specific Java distribution is required as it includes JavaFX components

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