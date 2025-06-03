import os
from glob import glob
import tensorflow as tf
import pandas as pd
import numpy as np

# Constants
F8_PATH = 'dataset/F8/'
F10_PATH = 'dataset/F10/'
COLUMNS = ['data__coordinates__x', 'data__coordinates__y', 'reference__x', 'reference__y']

# Data normalization constants
NORMALIZATION_OFFSET = 2000
NORMALIZATION_FACTOR = 10000

# Neural network parameters
BATCH_SIZE = 512
EPOCHS = 50
HIDDEN_LAYERS = [32, 64, 32, 16, 2]

def read_static(choice):
    # Read static measurement data from multiple files
    path = F8_PATH if choice == 'f8' else F10_PATH
    files = glob(os.path.join(path, f'{choice}_stat_*.xlsx'))
    
    if not files:
        raise FileNotFoundError(f"No static measurement files found in {path}")
    
    print(f"Found {len(files)} static measurement files for {choice}")
    dfs = [pd.read_excel(file, usecols=COLUMNS) for file in files]
    concat_data = pd.concat(dfs, ignore_index=True)
    
    # Split into measured and reference points
    measured_points = concat_data[['data__coordinates__x', 'data__coordinates__y']]
    ref_points = concat_data[['reference__x', 'reference__y']]
    return measured_points, ref_points

def read_verifying(choice):
    # Read verification data from both clockwise and counterclockwise files
    path = F8_PATH if choice == 'f8' else F10_PATH
    
    # Check for both verification files
    clockwise_file = os.path.join(path, f'{choice}_1z.xlsx')
    counterclockwise_file = os.path.join(path, f'{choice}_1p.xlsx')
    
    if not os.path.exists(clockwise_file) or not os.path.exists(counterclockwise_file):
        raise FileNotFoundError(f"Verification files not found. Please ensure both {clockwise_file} and {counterclockwise_file} exist.")
    
    # Read both files
    clockwise_data = pd.read_excel(clockwise_file, usecols=COLUMNS)
    counterclockwise_data = pd.read_excel(counterclockwise_file, usecols=COLUMNS)
    
    # Combine data from both files
    combined_data = pd.concat([clockwise_data, counterclockwise_data], ignore_index=True)
    
    # Split into measured and reference points
    measured_points = combined_data[['data__coordinates__x', 'data__coordinates__y']]
    ref_points = combined_data[['reference__x', 'reference__y']]
    
    # Extract individual coordinates
    measured_x = measured_points['data__coordinates__x']
    measured_y = measured_points['data__coordinates__y']
    ref_x = ref_points['reference__x']
    ref_y = ref_points['reference__y']
    
    print(f"Loaded verification data from both clockwise and counterclockwise routes for {choice}")
    return measured_points, ref_points, measured_x, measured_y, ref_x, ref_y

def normalize_data(df):
    # Normalize data to range [0,1] using offset and scaling factor
    return (df.astype('float32') + NORMALIZATION_OFFSET) / NORMALIZATION_FACTOR

def create_neural_network():
    # Create and compile neural network model
    network = tf.keras.models.Sequential([
        tf.keras.layers.Dense(size, activation='relu') for size in HIDDEN_LAYERS[:-1]
    ] + [tf.keras.layers.Dense(HIDDEN_LAYERS[-1], activation='sigmoid')])

    network.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss=tf.keras.losses.MeanSquaredError(),
        metrics=[tf.keras.metrics.RootMeanSquaredError()]
    )
    return network

def calculate_errors(result, verif_measured_x, verif_measured_y, verif_ref_x, verif_ref_y):
    # Calculate errors between predicted and reference points
    result = result * NORMALIZATION_FACTOR - NORMALIZATION_OFFSET
    
    return pd.DataFrame({
        'x': result[:, 0],
        'y': result[:, 1],
        'data__coordinates__x': verif_measured_x,
        'data__coordinates__y': verif_measured_y,
        'reference__x': verif_ref_x,
        'reference__y': verif_ref_y,
        'error_arr_filtered': np.sqrt((result[:, 0] - verif_ref_x) ** 2 + (result[:, 1] - verif_ref_y) ** 2),
        'error_arr_unfiltered': np.sqrt((verif_measured_x - verif_ref_x) ** 2 + (verif_measured_y - verif_ref_y) ** 2)
    })

def process_data(choice):
    try:
        # Read and prepare data
        verif_measured, verif_ref, verif_measured_x, verif_measured_y, verif_ref_x, verif_ref_y = read_verifying(choice)
        training_points, ref_points = read_static(choice)

        # Handle missing values
        for df in [verif_measured, verif_ref, training_points, ref_points]:
            df.fillna(0, inplace=True)

        # Normalize data
        training_points = normalize_data(training_points)
        ref_points = normalize_data(ref_points)
        verif_measured = normalize_data(verif_measured)
        verif_ref = normalize_data(verif_ref)

        # Split data into training and validation sets
        rows_counter = len(training_points)
        split_idx = int(0.9 * rows_counter)
        
        training_data = training_points.iloc[:split_idx]
        reference_data = ref_points.iloc[:split_idx]
        val_data_measured = training_points.iloc[split_idx:].reset_index(drop=True)
        val_data_ref = ref_points.iloc[split_idx:].reset_index(drop=True)

        # Create and train neural network
        network = create_neural_network()
        network.fit(
            np.array(training_data),
            np.array(reference_data),
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            validation_data=(val_data_measured, val_data_ref)
        )

        # Evaluate and predict
        network.evaluate(np.array(verif_measured), np.array(verif_ref), batch_size=BATCH_SIZE)
        result = network.predict(np.array(verif_measured))
        
        # Calculate errors and save results
        result_df = calculate_errors(result, verif_measured_x, verif_measured_y, verif_ref_x, verif_ref_y)
        result_df.to_excel(f'result{choice.upper()}.xlsx', engine='xlsxwriter')
        print(f"Results for {choice.upper()} saved to result{choice.upper()}.xlsx")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure all required files are present in the dataset directory.")
    except Exception as e:
        print(f"An error occurred while processing {choice}: {e}")

if __name__ == "__main__":
    # Process both F8 and F10 data
    process_data('f8')
    process_data('f10')