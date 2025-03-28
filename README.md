This Python script automatically tracks vessel movements by scraping data from goradar.ru using IMO numbers and exports the information to JSON format.

# Required Packages
```
pip install selenium beautifulsoup4 requests
```
# Output Example
```
[
  {
    "imo": "9506344",
    "time": "2023-05-15 14:30:45",
    "latitude": 45.1234,
    "longitude": -122.5678,
    "course": 180,
    "speed": 12.5
  }
]
```
