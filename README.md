# Extract table
```python
table = soup.find('table', class_='table table-striped table-bordered table-hover table-condensed table-list')
```

# Extract table headers
```python
headers = [header.text.strip() for header in table.find_all('th')]
```

# Extract table rows
```python
data = []
for row in table.find_all('tr'):
    row_data = [cell.text.strip() for cell in row.find_all('td')]
    if row_data:
        data.append(row_data)
```

# Create DataFrame
```python
df = pd.DataFrame(data, columns=headers)
```

# Save to CSV
```python
df.to_csv('nepal_gdp.csv', index=False)
```

# Connect to SQLite database
```python
conn = sqlite3.connect('nepal_gdp.db')
cur = conn.cursor()
```

# Create table
```python
cur.execute('''CREATE TABLE IF NOT EXISTS gdptable (
                Year INTEGER,
                GDP_Nominal_Current_USD INTEGER,
                GDP_Real_Inflation_adj INTEGER,
                GDP_change DECIMAL(4,2),
                GDP_per_capita INTEGER,
                Pop_change DECIMAL(4,2),
                Population INTEGER
            )''')
```

# Insert data into table
```python
query = """
INSERT INTO gdptable (Year, GDP_Nominal_Current_USD, GDP_Real_Inflation_adj, GDP_change, GDP_per_capita, Pop_change, Population)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""
```
```python
data_to_be_inserted = df.to_records(index = False)
```
```python
try:
    for row_data in data_to_be_inserted:
        cur.execute(query, row_data)
    conn.commit()
except Exception as e:
    print(e)
```
  ```python
cur.execute("Select * from gdptable").fetchall()
```    
# Commit changes and close connection
```python
conn.commit()
conn.close()
```
