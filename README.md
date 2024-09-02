# Lok Sabha Elections

![Lok Sabha Election](https://github.com/user-attachments/assets/74bba43a-ef71-4c0c-92ee-0ef20e896179)

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


Overall, this code automates logging into LinkedIn and scraping data from job listings across potentially multiple pages.

Here the code file link :codeforwebscraping.ipynb

# STEPS FOR DATA CLEANING :

