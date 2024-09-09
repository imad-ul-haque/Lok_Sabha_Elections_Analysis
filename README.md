# Lok Sabha Elections

![Lok Sabha Election](https://github.com/user-attachments/assets/74bba43a-ef71-4c0c-92ee-0ef20e896179)

-------------------------------

# Overview
This project delves into the intricacies of India's democratic process through a detailed analysis of Lok Sabha elections from 1977 to 2019. It aims to uncover insights into voter behavior, political party performance, and key factors influencing election outcomes.

STEPS OF DATA SCRAPPING FROM THE Indian Lok Sabha Elections. 

1. Setting Up:
    The code imports libraries to control a web browser and work with data.
    It stores the given links which contain the Lok election data.
    It sets up a tool to control the Chrome web browser.

2. Preparing for Data Collection:
    The code creates a container to store Election information (Election_year, pc_name, pc_no, etc.).
    It identifies all the page numbers on the current election portal (assuming they have a specific class name).

3. Looping Through Job Listing Pages:
    The code loops through each State, potentially scraping election data from all available pages.
    On each page, it clicks the corresponding Constituency to navigate.
    It waits a few seconds (not ideal) to allow the page to load.
    The code then identifies all the constituencies in each state on the current page (assuming they have a specific class name).

4. Extracting Data from Each constituency:
    The code loops through each constituency on the current page.
    For each constituency, it clicks on it to open the details page.
    It scrolls down the page to the bottom.
    The code then tries to extract various details about the constituency and votes from the page:

    election_year, 
    pc_name, 
    pc_no, 
    electors, 
    male_electors, 
    female_electors, 
    booths, 
    votes_polled, 
    male_voters, 
    female_voters.


        1. election_year, 
        2. pc_name, 
        3. pc_no, 
        4. electors, 
        5. male_electors, 
        6. female_electors, 
        7. booths, 
        8. votes_polled, 
        9. male_voters, 
        10. female_voters.


5. Storing Extracted Data:
    If the code successfully finds each data element, it stores the information in the container created earlier.


Overall, this code automates Visiting the given websites and scraping data from Election details across potentially multiple pages.

Here is the code file link:https://github.com/imad-ul-haque/Pixel-Pioneers_008/blob/main/Code_for_Data_Scrapping_.ipynb

![ER Diagram](https://github.com/user-attachments/assets/c999cfa7-b305-42bb-9bdd-84b62dc84eb0)

---

# Election Data Scraping Script

## Overview

This script utilizes the Selenium WebDriver to scrape election data from the **IndiaVotes** website for multiple years of the **Lok Sabha** elections. The data is extracted from different pages corresponding to election results, constituency details, and candidate information.

### Key Features:
- Scraping data for multiple election years from 1977 to 2024.
- Capturing election details such as the winning candidate, party, electors, votes, and more.
- Saving the data in a structured format using **Pandas DataFrame**.
- Exporting data into CSV files.

---

## Prerequisites

Before running the script, ensure the following:
1. Install the necessary Python libraries:
   ```bash
   pip install selenium pandas
   ```
2. Download and set up the appropriate WebDriver for your browser (in this case, **ChromeDriver**).
3. Ensure you have an active internet connection to access the IndiaVotes website.

---

## Libraries Used

- **Selenium**: For browser automation and interaction with web elements.
- **Pandas**: For organizing and storing data in a tabular format (DataFrame).
- **time**: For adding delays between actions to avoid detection as a bot.

---

## Code Sections

### 1. Election Details (Table 1)
This section extracts general election data, including the winning candidate, party, votes, and turnout information for each year.

- **URL**: The script starts with a hardcoded URL for the 1977 election. This can be modified for other years.
- **Data Fields**: The script scrapes and stores:
  - Year of election
  - Parliamentary Constituency (PC) name and number
  - Winning candidate
  - Party, electors, votes, turnout, margin, and margin percentage.
  
The script loops through multiple election years by modifying the URL and extracts data for each constituency.

```python
years_range = [1977, 1980, 1984, 1989, 1991, 1996, 1998, 1999, 2004, 2009, 2014, 2019, 2024]
```

### 2. Constituency Details (Table 2)
This section collects detailed data on the electors and voters, broken down by gender.

- **Data Fields**: The script scrapes:
  - Total electors, male and female electors.
  - Booths, votes polled, male and female voters.

The data is retrieved by navigating to each constituency's detailed page and extracting the required fields.

### 3. Candidate Details (Table 3)
This section gathers data about candidates and their performance in the election.

- **Data Fields**: The script collects:
  - Candidate names, positions, votes received, and vote percentage.
  - The candidate's party affiliation.

The candidate data is scraped from a table specific to each constituency, iterating through each row to gather the necessary information.

---

## How to Run the Script

1. Modify the **URL** to point to the specific election year or constituency you want to scrape.
2. Ensure the WebDriver (ChromeDriver) is correctly set up and matches your browser version.
3. Execute the script. For example:
   ```bash
   python Code_for_Data_Scrapping_.py
   ```
4. The data is saved as CSV files:
   - **scrapped_dataset_table_1_2nd.csv** for Table 1 (Election Details)
   - **Table_2_2014_part-2.csv** for Table 2 (Constituency Details)
   - **Table_3_2024_part_3.csv** for Table 3 (Candidate Details)

---

## Notes

- The script uses **XPaths** to identify web elements, which might break if the structure of the website changes.
- The use of `time.sleep()` ensures that the scraping process doesn't overwhelm the server and helps avoid detection as a bot.
- **Error Handling**: The script uses `try-except` blocks to handle missing data gracefully. If a specific field isn't found, it appends `None` to the list, ensuring that the DataFrame remains consistent.


---

## Conclusion

This script provides a powerful and flexible tool to automate the extraction of election data from the IndiaVotes website. With some modifications, it can be adapted to other election years, regions, or data sources.



------------------------------

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

**Outcome**: The cleaned data is saved in `Table_1.csv`, `Table_2.csv`, and `Table_3.csv`, ready for download, and is downloaded using the files.download() function.

--------


# Dashboard:

To access our interactive dashboard and explore the data-driven insights, click on the given link below. 
This will take you directly to the Streamlit platform, where you can interact with our dashboard and analyze the data in detail.

Dashboard link: (https://lok-sabha-election-analysis.streamlit.app/)
