import pandas as pd
import numpy as np
import time
import os
from typing import Dict, Union
from multiprocessing import Pool, cpu_count
from functools import partial

 
#================================================================
# Configuration constants
#================================================================
TOTAL_LINES = 1_000_000_000  # Total number of lines in the file
CHUNK_SIZE = 50_000_000  # Reduced chunk size for memory efficiency
FILENAME = "data/measurements.txt"
NUM_CORES = max(1, cpu_count() - 1)  # Leave one core free



#================================================================
# Process a large file using memory-efficient parallel processing
#================================================================
def process_large_file(filename: str,  total_lines: int,  chunk_size: int = CHUNK_SIZE) -> pd.DataFrame:
    """
    Args:
        filename (str): Path to the file
        total_lines (int): Total number of lines in the file
        chunk_size (int): Number of lines to process in each chunk
    
    Returns:
        pd.DataFrame: Aggregated results
    """

    # Validate file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    
    # Prepare chunk processing
    chunk_starts = list(range(0, total_lines, chunk_size))
    
    # Create partial function for chunk reading
    read_chunk_func = partial(read_chunk_efficiently, filename)
    
    results = []
    
    # Use memory-efficient parallel processing
    with Pool(NUM_CORES) as pool:
        # Read and process chunks in parallel
        chunks = pool.starmap(read_chunk_func, [(start, chunk_size) for start in chunk_starts])
        
        # Process chunks in parallel
        results = pool.map(aggregate_data, chunks)
    
    # Merge and return final results
    return merge_results(results)


#================================================================
# Read a specific chunk of the file using low-memory techniques.
#================================================================
def read_chunk_efficiently(filename: str, chunk_start: int, chunk_size: int) -> pd.DataFrame:
    """
    Args:
        filename (str): Path to the file
        chunk_start (int): Starting line of the chunk
        chunk_size (int): Number of lines to read
    
    Returns:
        pd.DataFrame: Processed chunk of data
    """
    try:
        # Use more memory-efficient reading method
        with open(filename, 'r') as f:
            # Skip to the starting line
            for _ in range(chunk_start):
                f.readline()
            
            # Read specific number of lines
            chunk_lines = [f.readline() for _ in range(chunk_size)]
            
            # Parse lines manually to avoid pandas overhead
            data = [line.strip().split(';') for line in chunk_lines if line.strip()]
            
            # Convert to numpy for memory efficiency
            if data:
                return pd.DataFrame(data, columns=['station', 'measure'])
            return pd.DataFrame(columns=['station', 'measure'])
    
    except Exception as e:
        print(f"Error reading chunk: {e}")
        return pd.DataFrame(columns=['station', 'measure'])


#================================================================
# Process a chunk of data and return aggregated statistics
#================================================================
def aggregate_data(chunk: pd.DataFrame) -> Dict[str, Union[float, str]]:
    """
    Args:
        chunk (pd.DataFrame): DataFrame chunk to process
    
    Returns:
        Dict with aggregated statistics per station
    """
    try:
        # Convert measure to numeric, handling potential errors
        chunk['measure'] = pd.to_numeric(chunk['measure'], errors='coerce')
        
        # Group by station and compute statistics
        station_stats = chunk.groupby('station')['measure'].agg([
            ('min', 'min'), 
            ('max', 'max'), 
            ('mean', 'mean')
        ])
        
        return station_stats.reset_index().to_dict('records')
    
    except Exception as e:
        print(f"Error processing chunk: {e}")
        return []


#================================================================
# Merge results from parallel processing
#================================================================
def merge_results(results: list) -> pd.DataFrame:
    """
    Args:
        results (list): List of station statistics
    
    Returns:
        pd.DataFrame: Merged and aggregated results
    """
    # Flatten the list of results
    flattened = [item for sublist in results for item in sublist]
    
    if not flattened:
        return pd.DataFrame()
    
    # Convert to DataFrame and aggregate
    df = pd.DataFrame(flattened)
    
    return (df.groupby('station')
              .agg({
                  'min': 'min',
                  'max': 'max',
                  'mean': 'mean'
              })
              .reset_index()
              .sort_values('station'))







#================================================================
# Main execution function
#================================================================
def main():    
    print("Starting large file processing...")
    
    start_time = time.time()
    
    try:
        # Process the file
        result_df = process_large_file(FILENAME, TOTAL_LINES)
        
        # Display results
        if not result_df.empty:
            print("\nTop Results:")
            print(result_df.head())
            print(f"\nProcessing completed in: {time.time() - start_time:.2f} seconds")
        else:
            print("No data processed.")
    
    except Exception as e:
        print(f"Critical error during processing: {e}")

if __name__ == "__main__":
    main()