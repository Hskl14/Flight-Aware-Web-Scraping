# Flight-Aware-Web-Scraping
Gathering Flight Data For Social Network Analysis Using Selenium and BeautifulSoup from FlightAware

### Required Python Libraries
- BeautifulSoup(bs4)
- Selenium(geckodriver)
- Networkx
- Datapackage

### Usage
Required Arguments:
--start Initial Airport Code (IATA Code)
--edge-count Number of Edges to collect

### Getting Started
This program collects needed amount of direct flight edges between airports and creates a .gexf file for Social Network Analysis.
Both of the arguments are needed for the execution of the program. 
``` ini
python flight_data_to_gexf.py --start IST --edge-count 100
```

### Data Sources
Airport Data: https://datahub.io/core/airport-codes/
