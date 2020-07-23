import folium
import requests
from bs4 import BeautifulSoup
import pandas


def radius_gen(tcases):

	return tcases ** 0.31	


def color_gen(tcases):
	if tcases < 1000:
		return "blue"
	elif tcases < 5000:
		return "green"
	elif tcases < 25000:
		return "purple"
	elif tcases < 50000:
		return "pink"
	elif tcases < 100000:
		return "yellow"
	elif tcases < 150000:
		return "orange"
	else:
		return "red"


r = requests.get("https://www.worldometers.info/coronavirus/")
c = r.content

soup = BeautifulSoup(c, "html.parser")

data = soup.find("tbody")
rows = data.find_all("tr", {"style":""})

d = {}

for item in rows:
	tcases = item.find_all("td")[2].text
	d[item.find_all("td")[1].text] = int(tcases.replace(",", ""))


cdata = pandas.read_csv("countries.csv")

lat = list(cdata["latitude"])
lon = list(cdata["longitude"])
cnt = list(cdata["name"])


map = folium.Map(location = [21.69, 31.09], zoom_start = 3, tiles = "Stamen Terrain")

fg = folium.FeatureGroup(name = "Countries")


for lt, ln, ct in zip(lat, lon, cnt):


	if ct in d.keys():

		try:
			fg.add_child(folium.CircleMarker(location = [lt,ln], popup = str(ct) + "\n" + str(d[ct]),
				radius = radius_gen(d[ct]), fill_color = color_gen(d[ct]), color = "#666666", fill_opacity = 0.7))
		except:
			pass

map.add_child(fg)

map.save("CoronaMap.html")

