So, during data scraping, we found out that we have multiple files, so to merge them all into one, instead of using an application we felt it appropriate to write a program

```python
year = 2014
years = {2014:2, 2019:4, 2024:6}
header = ''',election_year,pc_name,pc_no,electors,male_electors,female_electors,booths,votes_polled,male_voters,female_voters'''
csv = ''
for year in list(years.keys()):
    for part in range(1, years[year] + 1):
        filename = "/home/jane/Downloads/Table_2_19_&_24/Table_2_" + str(year) + "_part-" + str(part) + ".csv"
        with open(filename, 'r') as file:
            clip = file.read()
            clip = clip.replace(header, '')
            csv += clip + "\n"
    year += 5

final_csv = header  + csv
final_csv = final_csv.replace(r'\n\n\n','\n') # Interesting this won't work without \n

# Making sure our merged CSV file is shared
with open("merged.csv", 'w') as merged:
    merged.write(final_csv)
```

![image](https://github.com/user-attachments/assets/47020a3a-6b20-484a-bbe0-caa13014fa94)
![image](https://github.com/user-attachments/assets/95b52830-d53f-4d1a-95e2-86a94917c5c0)



