# Pixel-Pioneers_008

# Data Cleaning Script Documentation

## Overview

This Python script is designed to clean and preprocess election data from multiple tables. The script systematically handles missing values, format inconsistencies, and transforms the data to ensure it's ready for further analysis. It primarily works with three main tables, performing specific cleaning tasks on each.

## Importing Libraries

The script starts by importing essential libraries:
- `pandas` for data manipulation.
- `re` for regular expressions.
- `numpy` for numerical operations.
- `google.colab.files` for handling file uploads and downloads in Google Colab.

### Example:
```python
import pandas as pd
import numpy as np
import re
import google.colab.files as files
```

These libraries are crucial for the operations performed in the script, such as reading data, cleaning text, and handling numerical conversions.

## Functions

### `convert_ratio(x)`
- **Purpose**: Converts a ratio to a percentage.
- **Example**: Suppose `x = "0.75"`. The function will convert it to `75.0`.
- **Usage in Script**: This function is applied to columns like `'turnout'` and `'margin_percent'` where some values are ratios, and others are percentages, ensuring uniformity.
  
  ```python
  t1['turnout'] = t1['turnout'].apply(convert_ratio)
  ```

### `replace_symbol(x)`
- **Purpose**: Removes percentage symbols and extra spaces from strings.
- **Example**: If `x = "75.0%"`, it will be cleaned to `75.0`.
- **Usage in Script**: This function cleans the `'turnout'` column by removing `%` symbols to prepare it for numerical conversion.
  
  ```python
  t1['turnout'] = t1['turnout'].apply(replace_symbol)
  ```

### `not_numeric(x)`
- **Purpose**: Checks if a value is non-numeric.
- **Example**: If `x = "ABC"`, the function will return `True`, indicating that it is not a number.
- **Usage in Script**: This is used to identify non-numeric values in the `'votes'` column, helping to isolate and clean these entries.
  
  ```python
  t2[t2['votes_polled'].apply(not_numeric)]['votes_polled']
  ```

### `replacecomma(x)`
- **Purpose**: Removes commas from strings and replaces specific non-numeric entries with zero.
- **Example**: If `x = "1,000"`, it will be cleaned to `1000`.
- **Usage in Script**: Applied to the `'Votes'` column to remove commas and handle entries like `'RU'` by replacing them with zero.
  
  ```python
  t3['Votes'] = t3['Votes'].apply(replacecomma)
  ```

## Data Cleaning Procedures

### Table 1 Cleaning
- **Objective**: Clean various columns in the first table, focusing on consistency and completeness.
- **Example**: For the `'electors'` column, the script removes commas and converts strings to numeric values, ensuring that the data is ready for analysis.
  
  ```python
  t1['electors'] = t1['electors'].str.replace(',', '')
  t1['electors'] = pd.to_numeric(t1['electors'])
  ```

  **Outcome**: This ensures that the `'electors'` column is free of formatting issues and ready for numerical operations.

### Table 2 Cleaning
- **Objective**: Handle and clean data for multiple election years, standardizing data across different years.
- **Example**: The script cleans the `'votes_polled'` column by removing text like "Total Votes Polled:" and converting it to numeric.
  
  ```python
  t2014['votes_polled'] = t2014['votes_polled'].str.replace("Total Votes Polled", '').str.replace(',', '')
  t2014['votes_polled'] = pd.to_numeric(t2014['votes_polled'])
  ```

  **Outcome**: The `votes_polled` column is cleaned, allowing for accurate aggregation and analysis of voter data.

### Table 3 Cleaning
- **Objective**: Clean candidate-related data and ensure all numeric fields are properly formatted.
- **Example**: The `'Votes_Percentage'` column is cleaned by removing non-numeric characters and converting the remaining values to numbers.
  
  ```python
  t3['Votes_Percentage'] = t3['Votes_Percentage'].apply(convert_ratio)
  t3['Votes_Percentage'] = t3['Votes_Percentage'].apply(replace_symbol)
  t3['Votes_Percentage'] = pd.to_numeric(t3['Votes_Percentage'])
  ```

  **Outcome**: This ensures that the `'Votes_Percentage'` column contains only numeric values, ready for statistical analysis.

### Supplemental Cleaning
- **Objective**: Standardize state names across the dataset.
- **Example**: The script replaces inconsistent state names with standardized versions, like changing `'Bihar [1947 - 1999]'` to `'Bihar'`.
  
  ```python
  t1['state'] = t1['state'].replace('Bihar [1947 - 1999]', 'Bihar')
  ```

  **Outcome**: This makes the `'state'` column consistent, which is crucial for any geographical analysis.

## Exporting Cleaned Data

The script concludes by exporting the cleaned tables into CSV files for further analysis. This allows for seamless integration with other data processing tools or for direct analysis.

### Example:
```python
t1.to_csv("Table_1.csv")
t2.to_csv("Table_2.csv")
t3.to_csv("Table_3.csv")
```

**Outcome**: The cleaned data is saved in `Table_1.csv`, `Table_2.csv`, and `Table_3.csv`, ready for download and is downloaded using the files.download() function.
