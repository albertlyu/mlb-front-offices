# MLB Front Offices Scraper

from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import csv

teams = {	'chc': {'city': 'chicago', 'nickname': 'cubs'},
			'cws': {'city': 'chicago', 'nickname': 'whitesox'},
			'tor': {'city': 'toronto', 'nickname': 'bluejays'},
			'bos': {'city': 'boston', 'nickname': 'redsox'},
			'nyy': {'city': 'newyork', 'nickname': 'yankees'},
			'was': {'city': 'washington', 'nickname': 'nationals'},
			'phi': {'city': 'philadelphia', 'nickname': 'phillies'},
			'oak': {'city': 'oakland', 'nickname': 'athletics'},
			'col': {'city': 'colorado', 'nickname': 'rockies'},
			'bal': {'city': 'baltimore', 'nickname': 'orioles'},
			'min': {'city': 'minnesota', 'nickname': 'twins'},
			'atl': {'city': 'atlanta', 'nickname': 'braves'},
			'pit': {'city': 'pittsburgh', 'nickname': 'pirates'},
			'mia': {'city': 'miami', 'nickname': 'marlins'},
			'ana': {'city': 'losangeles', 'nickname': 'angels'},
			'tex': {'city': 'texas', 'nickname': 'rangers'},
			'sf': {'city': 'sanfrancisco', 'nickname': 'giants'},
			'la': {'city': 'losangeles', 'nickname': 'dodgers'},
			'kc': {'city': 'kansascity', 'nickname': 'royals'},
			'mil': {'city': 'milwaukee', 'nickname': 'brewers'},
			'cin': {'city': 'cincinnati', 'nickname': 'reds'},
			'det': {'city': 'detroit', 'nickname': 'tigers'},
			'nym': {'city': 'newyork', 'nickname': 'mets'},
			'tb': {'city': 'tampabay', 'nickname': 'rays'},
			'sea': {'city': 'seattle', 'nickname': 'mariners'},
			#'hou': {'city': 'houston', 'nickname': 'astros'},
			#'cle': {'city': 'cleveland', 'nickname': 'indians'}
			#'sd': {'city': 'sandiego', 'nickname': 'padres'},
			#'stl': {'city': 'stlouis', 'nickname': 'cardinals'},
			#'ari': {'city': 'arizona', 'nickname': 'diamondbacks'},
			}

# Get team url
def get_team_url(team):
	BASE_URL = "mlb.com/team/front_office.jsp?c_id="
	url = "".join(("http://",teams[team]['city'],".",teams[team]['nickname'],".",BASE_URL,team))
	return(url)
	
# Get unordered HTML list of front office employees from url
def get_list(url):
	html = urlopen(url)
	soup = BeautifulSoup(html.read()).find("div", {"id": "mc"})
	return soup

# Convert html tag to string
def stringify(html):
	if html is None:
		html = 'None'
	else:
		html = html.string
	return html

# Get front office employees for team from url
def get_employees(team):
	print("Loading",team,"front office info...")
	url = get_team_url(team)
	soup = get_list(url)
	ul = soup.find("ul", {"id": "front_office_list"}) # this doesn't account for weird teams like the CLE
	employees = []
	for dl in ul.find_all("dl"):
		department = stringify(dl.find_previous("h4"))
		subdepartment = stringify(dl.find_previous("h5"))
		employee = [dd.string for dd in dl.find_all("dd")]
		title = [dt.string for dt in dl.find_all("dt")]
		employees.append({
			'department': department,
			'subdepartment': subdepartment,
			'employee': employee,
			'title': title
		}) # Flat dictionary format
		#employees.append({department: {subdepartment: {
		#	'employee': employee,
		#	'title': title
		#}}}) # Nested dictionary format
	return employees

# Write data into excel file
with open("data/mlbfrontoffices.csv", "w") as f:
	fieldnames = ("team", "department", "subdepartment", "employee", "title")
	output = csv.writer(f, delimiter=",")
	output.writerow(fieldnames)

#for team in teams:
	team = 'chc'
	employees = get_employees(team)
	for i in range(0,len(employees)):
		department = employees[i]['department']
		subdepartment = employees[i]['subdepartment']
		for j in range(0,len(employees[i]['employee'])):
			employee = employees[i]['employee'][j]
			title = employees[i]['title'][j]
			output.writerow([team,department,subdepartment,employee,title])
		print("	Done writing",team,"-",department,"-",subdepartment)


# This gets all the team urls
#soup = get_list("http://mlb.mlb.com/team/")
#team_urls = [h5.a["href"] for h5 in soup.find_all("h5")]
#print(team_urls)