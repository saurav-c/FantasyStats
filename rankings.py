import pandas as pd
from tabulate import tabulate
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests



def run():
	espn()
	cbs()

def espn():
	df = pd.read_html("http://www.espn.com/fantasy/football/story/_/page/18RanksPreseason300nonPPR/2018-fantasy-football-non-ppr-rankings-top-300")
	data = df[1]
	data.columns = ['Player', 'Pos', 'Team', 'PosRank']
	data[['Rank','Player']] = data['Player'].str.split(' ', 1, expand=True)
	data = data.set_index('Rank', drop=True)
	print(data[[0]])


def cbs():
	entries = []
	res = requests.get('https://www.cbssports.com/fantasy/football/rankings/standard/top200/')
	soup = BeautifulSoup(res.content, 'lxml')
	data = soup.find('div', attrs = {'class': 'player-wrapper'})
	players = data.find_all("div", ["player-row first", "player-row"])
	for player in players[180:]:
		rank = player.find('div', 'rank').contents[0]
		a = player.find_all('div', 'player')[0].find_all('a')[0]
		try:
			url = a['href']
			result = requests.get('https://www.cbssports.com' + url)
			souper = BeautifulSoup(result.content, 'lxml')
			info = souper.find_all('div', 'marquee-full-player-info')
			name = info[0].find_all('h1')[0].contents[0]
		except IndexError:
			name = a.find_all('span')[0].contents[0]
		entries.append([rank, name])

	df = pd.DataFrame(entries, columns=['Rank', 'Name'])
	print(df)
run()
