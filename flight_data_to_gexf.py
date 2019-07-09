from bs4 import BeautifulSoup
from selenium import webdriver
from datapackage import Package
import time
import sys
import argparse
import networkx as nx

def to_visit(iata_code):
	if iata_code in airports_to_visit:
		return
	airports_to_visit.append(iata_code)
	return

def correct_argument(string):
    if sys.version_info.major == 3:
        return string
    else:
        return string.encode('utf-8')

def get_airport_list():
	print('Getting Airport Data.....')
	package = Package('https://datahub.io/core/airport-codes/datapackage.json')
	for resource in package.resources:
	    if resource.descriptor['datahub']['type'] == 'derived/csv':
	        data = resource.read(keyed=True)
	        print('Got Airport Data.....')
	        return data
	return -1

def get_airport_info(iata_code):
	try:
		for airport in airport_data:
			if airport['iata_code'] == iata_code:
				return airport['name'], airport['gps_code'] 
	except:
		print('Couldnt find iata_code')

def get_flights(iata_code, edge_count):
	if len(edges)>edge_count:
		return
	airport_name, airport_gps_code = get_airport_info(iata_code)
	print('************* GETTING FLIGHTS FOR ' + airport_name + ' *************')
	driver = webdriver.Firefox()
	driver.get('https://tr.flightaware.com/live/airport/' + airport_gps_code);
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')

	departures = soup.find(id='departures-board')
	arrivals = soup.find(id='arrivals-board')
	departures_table_body = departures.find('tbody')
	arrivals_table_body = arrivals.find('tbody')

	for tr in arrivals_table_body.find_all('tr'):
		flight_destination = tr.find_all('td')[2].text.strip()
		if flight_destination is "":
			continue
		edges.append((flight_destination[:-5], airport_name))
		print("From: " + flight_destination[:-5])
		if flight_destination[-5] is not '(':
			continue
		to_visit(flight_destination[-4:-1])

	for tr in departures_table_body.find_all('tr'):
		flight_destination = tr.find_all('td')[2].text.strip()
		if flight_destination is "":
			continue
		edges.append((airport_name ,flight_destination[:-5]))
		print("To: " + flight_destination[:-5])
		if flight_destination[-5] is not '(':
			continue
		to_visit(flight_destination[-4:-1])
	driver.quit()
	return

if __name__ == '__main__':
	class Ids:
		pass
	ids = Ids()
	parser = argparse.ArgumentParser()
	parser.add_argument(
	    '--start',
	    type=str,
	    metavar='\tStarting Airport Code',
	    dest='start'
	)
	parser.add_argument(
	    '--edge-count',
	    type=int,
	    metavar='\tNumber of edges',
	    dest='edge_count'
	)
	args = parser.parse_args(namespace=ids)
	starting_airport = correct_argument(ids.start)
	edge_count = correct_argument(ids.edge_count)

	starting_time = time.time()

	airport_data = get_airport_list()
	
	airports_to_visit = list()
	edges = list()
	get_flights(starting_airport, edge_count)

	for iata_code in airports_to_visit:
		get_flights(iata_code, edge_count)

	print('************* ELAPSED TIME: ' + str(time.time()-starting_time) + ' *************')

	G = nx.Graph()

	G.add_edges_from(edges)

	print(f"Nodes : {G.number_of_nodes()}")
	print(f"Edges : {G.number_of_edges()}")

	nx.write_gexf(G, "airport_data.gexf")