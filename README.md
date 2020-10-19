# APNIC conference scraper

This repository contains a Python web scraper to get the attendee lists of the bi-yearly APNIC conferences and a Jupyter Notebook to clean and standardise the data.

The data is then used to create an interactive dashboard to explore the impact different countries and organisations have on the APNIC policy process. The tool can be found [here](https://datastudio.google.com/reporting/db0e734e-6882-432c-81f1-c87e17bedc34
).

This work was done as part of the King's Undergraduate Research Fellowship project **Mapping the Digital Silk Road** supervised by Dr. Elisa Oreglia and Dr. Ashwin Mathew.

Special thanks to @finwarman for being a web scraping wizzard and supporting me.

## Setup

You need to have these things installed to run all the scripts.

- Python 3
- Jupyter
- BeautifulSoup, Pandas, NumPy

## Run scripts

To get the data:

```sh
git clone https://github.com/paumue/APNIC-conference-scraper.git
cd APNIC-conference-scraper/scripts/
python3 attendance_scraper.py
```

To clean the data and create a standardised data set:

```sh
cd APNIC-conference-scraper/scripts/
jupyter notebook attendee_data_preprocessing.ipynb
```
Then run the code in the notebook and it will create a cleaned and standardised csv.
