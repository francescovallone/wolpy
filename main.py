import requests
import sys
import time


def usage():
	print("Usage: python3 main.py -key DEVELOPMENT-KEY -summoner YourSummonerName -region YourRegion\n")
	print("Available Regions: br1, eun1, euw1, jp1, kr, la1, la2, na1, oc1, ru, tr1")
	sys.exit(0)


def get_summoner_account_id(region, summoner, key):
	url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(region, summoner)
	return requests.get(url, headers={"X-Riot-Token": key}).json()['accountId']


def get_games(region, summoner, key):
	print("Retrieving your games...")
	game_ids = []
	account_id = get_summoner_account_id(region, summoner, key)
	index = 0
	while True:
		url = "https://{}.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?beginIndex={}".format(region, account_id, index)
		games = requests.get(url, headers={"X-Riot-Token": key}).json()['matches']
		temp = [g['gameId'] for g in games]
		game_ids.extend(temp)
		print("Retrieved {0} games".format(len(game_ids)), end='\r', flush=True)
		if len(games) != 100:
			time.sleep(120)
			break
		else:
			index += 100
	return game_ids


def get_duration(region, summoner, key):
	total_hours = 0
	games = get_games(region, summoner, key)
	index = 0
	for game in games:
		index += 1
		print("Calculating how much time you wasted on League of Legends... [{}/{}]".format(index, len(games)), end='\r', flush=True)
		url = "https://{}.api.riotgames.com/lol/match/v4/matches/{}".format(region, game)
		seconds = requests.get(url, headers={"X-Riot-Token": key}).json()['gameDuration']
		total_hours += seconds/60
		if index%19 == 0:
			time.sleep(1)
		if index%99 == 0:
			time.sleep(120)
	return total_hours



def main(argv, argc):
	key = ""
	if argc < 7 or "-key" not in argv or "-summoner" not in argv or "-region" not in argv:
		usage()
	key = argv[argv.index("-key") + 1]
	summoner = argv[argv.index("-summoner")+1]
	region = argv[argv.index("-region") + 1]
	if region not in ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "ru", "tr1"]:
		usage()
	result = get_duration(region, summoner, key)
	print()
	print("Done!")
	print("You wasted on League of Legends:{} hours!\nCongratulations nerd!".format(int(result)))
	


if __name__ == "__main__":
	main(sys.argv, len(sys.argv))