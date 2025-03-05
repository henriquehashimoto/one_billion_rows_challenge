# 1 BILLION ROWS CHALLENGE 

Inspired by [Luciano Galvao Filho](https://github.com/lvgalvao) original challange, I'm adding into the challenge a 2 new competitors. 

The goal of this project is to demonstrate how to efficiently process a massive data file containing 1 billion rows (~14GB), specifically to calculate statistics (including aggregation and sorting which are heavy operations) using Python.

The libraries under evaluation are:

- `pandas`
- `fireducks`
- `duckdb`
- `pyspark`

The data file consists of temperature measurements from several weather stations. Each record follows the format `<string:station name>;<double:measurement>`, with the temperature being displayed to one decimal place accuracy.

Here are ten example lines from the file:


```
Istanbul;6.2
Roseau;34.4
Conakry;31.2
Istanbul;23.0
Hamburg;12.0
Bulawayo;8.9
```

The challenge is to develop a Python program capable of reading this file and calculating the minimum, average (rounded to one decimal place) and maximum temperature for each station, displaying the results in a table sorted by station name.

| station      | min_temperature | mean_temperature | max_temperature |
|--------------|-----------------|------------------|-----------------|
| Abha         | -31.1           | 18.0             | 66.5            |
| Abidjan      | -25.9           | 26.0             | 74.6            |
| Abéché       | -19.8           | 29.4             | 79.9            |
| Accra        | -24.8           | 26.4             | 76.3            |
| Yinchuan     | -45.2           | 9.0              | 56.9            |
| Zagreb       | -39.2           | 10.7             | 58.1            |
| Zanzibar City| -26.5           | 26.0             | 75.2            |
| Zürich       | -42.0           | 9.3              | 63.6            |
| Ürümqi       | -42.1           | 7.4              | 56.7            |
| İzmir        | -34.4           | 17.9             | 67.9            |



---

# Results

Table of comparison between libraries.

The tests were done in a PC with 32gb of RAM, NVME M.2 as SSD and a Ryzen 5 5600G as CPU. 

All tests were conducted with pure Python and each library, the results of processing the 1 billion row file are:

| Deploy on | Time of Execution |
|-----------|-------------------|
| FireDucks | 141.255 sec       |
| Pandas    | 328.50 sec        |
| DuckDB    | 23.39 sec         | 
| PySpark   | 129.84            |

**Note:** FireDucks performance may be affected due to execution be on a WSL virtualization of VSCode. A pure linux based system may present a better result.

As we can see, DuckDB won with some margin! 

---

# Settings

## Environment setting with uv 

**1) Clone this repository**: using `git clone https://github.com/henriquehashimoto/one_billion_rows_challenge.git`

**2) Create venv**: `uv venv .venv` , if UV not installed: `pip install uv`

**3) Use libraries**: `uv sync`


## Files and folders organization

### data - save files that are manipulated

Here you'll find the files that were used as source datas for the project

### models - execution files

These files are the ones that generated the test to compare the execution time, use them for your own test


### src - Creating file with 1 billion rows

The dataset used in this challenge is synthetically generated using a Python script (`generate_measurements.py`) included in this repository. The script creates a txt file (`measurements.txt`) with the specified number of rows, where each line represents a weather station measurement in the format `city;temperature` (e.g., `São Paulo;23.5`). Below is an overview of how the data is generated:

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

### tests - random testing performed

Here is some scripts for simple tests done to practice before the scripts created on "models"


---

## Testing Tips

- **Dataset Size**: Ensure the 1 billion-row file is realistic. Generate synthetic data with random values for `city` (e.g., 100 unique cities) and `temperature` (e.g., -10°C to 40°C).
- **Metrics**: Record execution time, RAM usage, and optionally CPU usage for each operation.
- **Incremental Testing**: Start with a smaller dataset (e.g., 10M or 100M rows) to debug code before scaling to 1 billion rows.
- **DuckDB Advantage**: Leverage `duckdb`s SQL optimization by writing operations as SQL queries and comparing them to Python APIs.

---
