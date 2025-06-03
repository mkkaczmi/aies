import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def create_visualizations(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # 1. Robot path visualization (points only, no lines)
    plt.figure(figsize=(14, 8))
    plt.scatter(df['data__coordinates__x'], df['data__coordinates__y'], color='green', s=20, label='Zmierzona', alpha=0.7)
    plt.scatter(df['x'], df['y'], color='blue', s=20, label='Poprawiona przez sieć', alpha=0.7)
    plt.scatter(df['reference__x'], df['reference__y'], color='orange', s=20, label='Rzeczywista', alpha=0.9)
    plt.title('Wizualna reprezentacja trasy robota', fontsize=18)
    plt.xlabel('X', fontsize=14)
    plt.ylabel('Y', fontsize=14)
    plt.legend(fontsize=13, loc='best')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(file_path.replace('.xlsx', '_trajektoria.png'), dpi=300, facecolor='white')
    plt.close()

    # 2. Error line plot (thicker lines, clearer)
    plt.figure(figsize=(14, 6))
    plt.plot(df['error_arr_filtered'], label='Przefiltrowane (niebieski)', color='blue', linewidth=2)
    plt.plot(df['error_arr_unfiltered'], label='Nieprzefiltrowane (pomarańczowy)', color='orange', linewidth=2)
    plt.title('Dystrybuanta błędu pomiaru z danych przefiltrowanych i nieprzefiltrowanych', fontsize=16)
    plt.xlabel('Nr próbki', fontsize=13)
    plt.ylabel('Błąd', fontsize=13)
    plt.legend(fontsize=13, loc='best')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(file_path.replace('.xlsx', '_bledy.png'), dpi=300, facecolor='white')
    plt.close()

    print(f"Charts saved for {file_path}")

if __name__ == "__main__":
    create_visualizations('resultF8.xlsx')
    create_visualizations('resultF10.xlsx') 