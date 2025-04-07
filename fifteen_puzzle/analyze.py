import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

def parse_filename(filename):
    """Parse the filename to extract components."""
    # Remove _stats.txt and split by underscore
    parts = filename.replace('_stats.txt', '').split('_')
    return {
        'depth': int(parts[1]),
        'combination': int(parts[2]),
        'method': parts[3],
        'strategy': parts[4]
    }

def read_stats_file(filepath):
    """Read and parse the stats file content."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return {
        'solution_length': int(lines[0]),
        'visited': int(lines[1]),
        'processed': int(lines[2]),
        'depth_reached': int(lines[3]),
        'time_ms': float(lines[4])
    }

def load_dataset(directory):
    """Load all stats files from the directory into a DataFrame."""
    data = []
    
    for file in Path(directory).glob('*_stats.txt'):
        filename = file.name
        file_info = parse_filename(filename)
        stats = read_stats_file(file)
        data.append({**file_info, **stats})
    
    return pd.DataFrame(data)

def calculate_detailed_statistics(df):
    """Calculate detailed statistics grouped by method and strategy."""
    metrics = ['solution_length', 'visited', 'processed', 'depth_reached', 'time_ms']
    
    # Basic statistics per method and strategy
    basic_stats = df.groupby(['method', 'strategy'])[metrics].agg([
        'mean', 'median', 'std', 'min', 'max'
    ])
    
    # Success rate
    success_rate = df.groupby(['method', 'strategy']).agg({
        'solution_length': lambda x: (x > -1).mean()
    }).rename(columns={'solution_length': 'success_rate'})
    
    # Additional statistics per method
    method_stats = df.groupby('method')[metrics].agg([
        'mean', 'median', 'std', 'min', 'max'
    ])
    
    # Additional statistics per strategy
    strategy_stats = df.groupby('strategy')[metrics].agg([
        'mean', 'median', 'std', 'min', 'max'
    ])
    
    return basic_stats, success_rate, method_stats, strategy_stats

def create_boxplots(df, output_dir):
    """Create boxplots for each metric with logarithmic scale where appropriate."""
    metrics = ['solution_length', 'visited', 'processed', 'depth_reached', 'time_ms']
    log_scale_metrics = ['visited', 'processed', 'time_ms']  # Metrics that need log scale
    
    for metric in metrics:
        plt.figure(figsize=(12, 6))
        
        if metric in log_scale_metrics:
            # Add small constant to handle zeros or negative values
            plot_data = df.copy()
            plot_data[metric] = plot_data[metric].apply(lambda x: x + 1e-10 if x <= 0 else x)
            
            plt.yscale('log', base=10)
            sns.boxplot(data=plot_data, x='method', y=metric, hue='strategy')
            
            # Format y-axis labels to show actual powers of 10
            plt.gca().yaxis.set_major_formatter(plt.ScalarFormatter())
            plt.gca().yaxis.set_major_formatter(
                plt.FuncFormatter(lambda y, _: '{:,.0f}'.format(y))
            )
        else:
            sns.boxplot(data=df, x='method', y=metric, hue='strategy')
            
        plt.title(f'{metric} by Method and Strategy\n{"(Log Scale)" if metric in log_scale_metrics else ""}')
        plt.xticks(rotation=45)
        plt.grid(True, which="both", ls="-", alpha=0.2)
        
        # Add gridlines for log scale
        if metric in log_scale_metrics:
            plt.grid(True, which="minor", ls=":", alpha=0.2)
            
        plt.tight_layout()
        plt.savefig(f'{output_dir}/{metric}_boxplot.png', dpi=300, bbox_inches='tight')
        plt.close()

def create_heatmaps(stats_df, output_dir):
    """Create heatmaps for each metric with logarithmic scale where appropriate."""
    log_scale_metrics = ['visited', 'processed', 'time_ms']
    
    # Explicitly define the exact order we want for strategies
    strategy_order = ['hamm', 'manh']  # Start with these two
    # Add any remaining strategies in alphabetical order
    other_strategies = sorted([s for s in stats_df.index.get_level_values('strategy').unique() 
                             if s not in strategy_order])
    strategy_order.extend(other_strategies)
    
    # Get all available methods and sort them
    all_methods = sorted(stats_df.index.get_level_values('method').unique())
    
    for metric in stats_df.columns.levels[0]:  # First level contains metric names
        plt.figure(figsize=(12, 8))
        pivot_table = stats_df[metric]['mean'].unstack()
        
        # Reorder the rows and columns with explicit ordering
        pivot_table = pivot_table.reindex(index=all_methods, columns=strategy_order)
        
        if metric in log_scale_metrics:
            # Apply log transformation for visualization
            pivot_table_log = np.log10(pivot_table + 1e-10)
            sns.heatmap(pivot_table_log, annot=pivot_table.values, 
                       fmt='.2e', cmap='YlOrRd')
        else:
            sns.heatmap(pivot_table, annot=True, fmt='.2f', cmap='YlOrRd')
            
        plt.title(f'{metric} Heatmap\n{"(Log Scale Values)" if metric in log_scale_metrics else ""}')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/{metric}_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()

def save_statistics_tables(basic_stats, success_rate, method_stats, strategy_stats, output_dir):
    """Save all statistics tables to separate CSV files with formatted output."""
    
    # Format and save basic statistics
    for metric in basic_stats.columns.levels[0]:
        metric_stats = basic_stats[metric].round(3)
        metric_stats.to_csv(f'{output_dir}/stats_{metric}.csv')
        
        # Also create a more readable text file
        with open(f'{output_dir}/stats_{metric}.txt', 'w') as f:
            f.write(f"Statistics for {metric}\n")
            f.write("=" * 50 + "\n")
            f.write(metric_stats.to_string())
            f.write("\n\n")
    
    # Save success rate
    success_rate.round(3).to_csv(f'{output_dir}/success_rate.csv')
    
    # Save method-wise statistics
    method_stats.round(3).to_csv(f'{output_dir}/method_statistics.csv')
    
    # Save strategy-wise statistics
    strategy_stats.round(3).to_csv(f'{output_dir}/strategy_statistics.csv')

def main():
    # Create output directory for plots and statistics
    output_dir = 'analysis_results'
    os.makedirs(output_dir, exist_ok=True)
    
    # Load and process data
    df = load_dataset('dataset')
    
    # Calculate detailed statistics
    basic_stats, success_rate, method_stats, strategy_stats = calculate_detailed_statistics(df)
    
    # Save all statistics tables
    save_statistics_tables(basic_stats, success_rate, method_stats, strategy_stats, output_dir)
    
    # Create visualizations
    create_boxplots(df, output_dir)
    create_heatmaps(basic_stats, output_dir)
    
    # Print summary to console
    print("\nSuccess Rate by Method and Strategy:")
    print(success_rate.round(3))
    
    print("\nMethod-wise Statistics (Mean Values):")
    print(method_stats.xs('mean', axis=1, level=1).round(3))
    
    print("\nStrategy-wise Statistics (Mean Values):")
    print(strategy_stats.xs('mean', axis=1, level=1).round(3))

if __name__ == "__main__":
    main()