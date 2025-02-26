# Performance Comparison of Python Libraries for Large Datasets

I'm conducting a challenge to determine the best Python library for reading and manipulating a dataset with 1 billion rows. The libraries under evaluation are:

- `pandas`
- `fireducks`
- `duckdb`

The goal is to assess which library performs best for reading a file with 1 billion rows and which one executes specific operations most efficiently. The dataset consists of two columns: `city` (string) and `temperature` (integer).

Below are the suggested data manipulation operations to measure and compare the performance of these libraries.

---

# Generate File

The dataset used in this challenge is synthetically generated using a Python script (`generate_measurements.py`) included in this repository. The script creates a parquet file (`measurements.parquet`) with the specified number of rows, where each line represents a weather station measurement in the format `city;temperature` (e.g., `São Paulo;23.5`). Below is an overview of how the data is generated:

- **Source**: The script reads a list of weather station names from `data/weather_stations.csv`, deduplicates them, and uses a subset for generation.
- **Randomization**:
  - A random subset of up to 10,000 station names is selected from the list using `random.choices`.
  - Temperatures are randomly generated as floats between -99.9°C and 99.9°C with one decimal place (e.g., `-12.3`, `45.7`).
- **File Writing**:
  - Data is written in batches of 10,000 rows to optimize performance and reduce memory usage.
  - The output file is saved as `data/measurements.txt`.
- **Default Configuration**: The default setting generates 1 million rows, but this can be adjusted by modifying the `num_rows_to_create` variable in the script.
- **Size Estimation**: The script estimates the file size before generation and reports the actual size and elapsed time after completion.

To generate a custom dataset (e.g., 1 billion rows), update the `num_rows_to_create` variable in the `main()` function and run:

```bash
python generate_measurements.py
```

---

## Data Manipulation Operations for this test

To evaluate the libraries effectively, the following operations are designed to test different aspects of performance, such as reading speed, filtering, aggregation, and memory usage.

### 1. File Reading
Measure the time taken to load the entire dataset with 1 billion rows.
- **Test**: Load the file (e.g., CSV, Parquet) and display the first 5 rows to confirm successful reading.
- **Metrics**: Time to read, memory usage.
- **Why?**: Assesses initial data ingestion performance and memory efficiency.

### 2. Simple Filtering
Evaluate the speed of filtering rows based on conditions.
- **Examples**:
  - Filter rows where `temperature > 30`.
  - Filter rows for a specific city (e.g., "São Paulo").
- **Why?**: Tests the efficiency of row selection and comparison operations.

### 3. Aggregation by City
Compute aggregated statistics grouped by the `city` column.
- **Examples**:
  - Average temperature per city.
  - Maximum and minimum temperature per city.
  - Count of records per city.
- **Why?**: Evaluates grouping (`groupby`) and numerical computation performance.

### 4. Joining with Another Dataset
Perform a join operation with a smaller dataset (e.g., 100 cities with population data).
- **Test**: Execute an `inner join` or `left join` based on the `city` column.
- **Why?**: Measures performance on a computationally intensive operation common in data analysis.

### 5. Adding a New Column
Create a new column based on a simple calculation or condition.
- **Examples**:
  - Convert temperature from Celsius to Fahrenheit (`temperature * 1.8 + 32`).
  - Categorize temperatures (e.g., "cold" if < 15°C, "warm" if 15–25°C, "hot" if > 25°C).
- **Why?**: Tests the speed of applying functions or conditions across all rows.

### 6. Sorting
Sort the dataset by one or both columns.
- **Examples**:
  - Sort by `temperature` (ascending or descending).
  - Sort by `city` (alphabetically).
- **Why?**: Assesses sorting efficiency, which can be memory- and CPU-intensive.

### 7. Removing Duplicates
Identify and remove duplicate rows based on `city` and `temperature`.
- **Why?**: Tests the ability to compare and eliminate redundant data.

### 8. Window Functions
Perform calculations over a sliding window, such as a moving average.
- **Example**: Compute the moving average temperature for each city over the last 5 measurements (assuming an implicit order, e.g., a timestamp column).
- **Why?**: Evaluates performance on advanced analytical operations.

---

## Testing Tips

- **Dataset Size**: Ensure the 1 billion-row file is realistic. Generate synthetic data with random values for `city` (e.g., 100 unique cities) and `temperature` (e.g., -10°C to 40°C).
- **Metrics**: Record execution time, RAM usage, and optionally CPU usage for each operation.
- **Incremental Testing**: Start with a smaller dataset (e.g., 10M or 100M rows) to debug code before scaling to 1 billion rows.
- **DuckDB Advantage**: Leverage `duckdb`’s SQL optimization by writing operations as SQL queries and comparing them to Python APIs.

---

## Example Test Workflow

1. **Reading**: Load the dataset.
2. **Filtering**: Filter rows where `temperature > 30`.
3. **Aggregation**: Calculate the average temperature per city.
4. **New Column**: Add a Fahrenheit temperature column.
5. **Sorting**: Sort by temperature in descending order.

This workflow provides a comprehensive comparison of how `pandas`, `fireducks`, and `duckdb` handle various tasks.

---

## Next Steps

With these operations, you’ll gain insights into each library’s strengths and weaknesses. If you need help generating the dataset or writing the code, feel free to explore the other sections of this repository or open an issue!

Happy coding, and good luck with the challenge!