from pyspark.sql import SparkSession
from pyspark.sql.functions import min, max, avg, col
import time

#===========================================
# Parameters
#===========================================

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Process 1 Billion Rows") \
    .config("spark.sql.adaptive.enabled", "true")\
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true")\
    .getOrCreate()

# File path
filename = "data/measurements.txt"

# Total lines (for reference, not strictly needed in PySpark)
total_linhas = 1_000_000_000


#===========================================
# Read and process data
#===========================================
def process_with_pyspark(filename):
    print("Starting file processing with PySpark...")
    
    # Record start time
    start_time = time.time()
    
    # Read the CSV file directly into a Spark DataFrame    
    df = spark.read \
        .option("sep", ";") \
        .option("header", "false") \
        .schema("station STRING, measure DOUBLE") \
        .csv(filename)
    
    # Perform aggregation
    aggregated_df = df.groupBy("station").agg(
            min("measure").alias("min"),
            max("measure").alias("max"),
            avg("measure").alias("mean")
        ) \
        .orderBy("station")
    
    # Collect results (this triggers the computation)
    result = aggregated_df
    
    # Show first few rows
    result.show(5)
    
    # Calculate processing time
    took = time.time() - start_time
    print(f"Processing took: {took:.2f} sec")
    
    return result



#===========================================
# Main
#===========================================
if __name__ == "__main__":
    try:
        # Execute the processing
        final_df = process_with_pyspark(filename)                
    finally:
        # Stop Spark session
        spark.stop()