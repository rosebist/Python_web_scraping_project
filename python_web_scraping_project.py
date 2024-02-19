# -*- coding: utf-8 -*-
"""Python_web_scraping_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j6kpEmOx08nu8oseX4Jsct6GLJjd43Qd
"""

import requests

url = "https://www.worldometers.info/gdp/nepal-gdp/"
response = requests.get(url)

from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, 'html.parser')

"""# Extract table"""

table = soup.find('table', class_='table table-striped table-bordered table-hover table-condensed table-list')

"""# Extract table headers"""

headers = [header.text.strip() for header in table.find_all('th')]

"""# Extract table rows"""

data = []
for row in table.find_all('tr'):
    row_data = [cell.text.strip() for cell in row.find_all('td')]
    if row_data:
        data.append(row_data)

"""# Create DataFrame"""

import pandas as pd

df = pd.DataFrame(data, columns=headers)

df

"""# Save to CSV"""

df.to_csv('nepal_gdp.csv', index=False)

"""# Connect to SQLite database"""

import sqlite3

conn = sqlite3.connect('nepal_gdp.db')
cur = conn.cursor()

"""# Create table"""

query = '''CREATE TABLE gdptable (
                Year INTEGER,
                GDP_Nominal_Current_USD INTEGER,
                GDP_Real_Inflation_adj INTEGER,
                GDP_change DECIMAL(4,2),
                GDP_per_capita INTEGER,
                Pop_change DECIMAL(4,2),
                Population INTEGER
            )'''

cur.execute(query)



"""# Insert data into table"""

query = """
INSERT INTO gdptable (Year, GDP_Nominal_Current_USD, GDP_Real_Inflation_adj, GDP_change, GDP_per_capita, Pop_change, Population)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

data_to_be_inserted = df.to_records(index = False)

try:
    for row_data in data_to_be_inserted:
        cur.execute(query, row_data)
    conn.commit()
except Exception as e:
    print(e)

cur.execute("Select * from gdptable").fetchall()

"""# Commit changes and close connection"""

conn.commit()

conn.close()

