This Python script automatically tracks vessel movements by scraping data from goradar.ru using IMO numbers and exports the information to JSON format.

# Required Packages
```
pip install selenium beautifulsoup4 requests
```
# Output Example
```
[
  {
        "imo": "9185762",
        "name": "Neng Yuan",
        "time": "2025-03-31 02:55:23",
        "latitude": 42.7687,
        "longitude": 132.987
    }
]
```
