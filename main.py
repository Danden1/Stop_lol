import requests
import datetime
import os
import argparse

class MatchTime:
    def __init__(self, path='data.txt'):
        f = open(path, 'r')
        tmp_list = f.read().splitlines()
        f.close()
        self.api_key = tmp_list[0]
        self.name = tmp_list[1]
        self.limit = tmp_list[2]
        self.path = tmp_list[3]
        self.puuid = self.get_puuid()



    def get_puuid(self):
        url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + self.name
        res = requests.get(url, headers={"X-Riot-Token": self.api_key})
        if res.status_code == 200:
            return res.json()['puuid']

        return None

    def get_lol_matchid(self):
        url = 'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/'+ self.puuid + '/ids?start=0&count=' + self.limit
        res = requests.get(url, headers={"X-Riot-Token": self.api_key})

        if res.status_code == 200:
            return res.json()

        return None

    def get_tft_matchid(self):
        url = 'https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/'+self.puuid + '/ids?count=' + self.limit
        res = requests.get(url, headers={"X-Riot-Token": self.api_key})
        if res.status_code == 200:
            return res.json()

        return None

    def get_lol_match_time(self, matchid):
        url = 'https://asia.api.riotgames.com/lol/match/v5/matches/' + matchid
        res = requests.get(url, headers={"X-Riot-Token": self.api_key})

        if res.status_code == 200:
            return res.json()['info']['gameCreation']

        return None

    def get_tft_match_time(self, matchid):
        url = 'https://asia.api.riotgames.com/tft/match/v1/matches/' + matchid
        res = requests.get(url, headers={"X-Riot-Token": self.api_key})

        if res.status_code == 200:
            return res.json()['info']['game_datetime']

        return None

    def check_can_game(self):
        now_time = datetime.datetime.now()
        count = 0
        lol_matchid = self.get_lol_matchid()
        tft_matchid = self.get_tft_matchid()

        for id in lol_matchid:
            match_time = self.get_lol_match_time(id)
            match_time = datetime.datetime.fromtimestamp(match_time/1000)
            if match_time.year == now_time.year and match_time.month == now_time.month and match_time.day == now_time.day:
                count+=1
            else:
                break

        for id in tft_matchid:
            match_time = self.get_tft_match_time(id)
            match_time = datetime.datetime.fromtimestamp(match_time / 1000)
            if match_time.year == now_time.year and match_time.month == now_time.month and match_time.day == now_time.day:
                count+=1
            else:
                break
        if count < int(self.limit):
            os.system(self.path)
            print('Run Game...')
        else:
            print("Stop Game!!!!!")

parser = argparse.ArgumentParser()

parser.add_argument("-k", "--api_key", default=None, type=str, help='your riot api-key')
parser.add_argument('-n', '--name', default=None, type=str, help='your summoner name')
parser.add_argument('-l', '--limit', default=None, type=int, help = 'limit match number')
parser.add_argument('-p', '--path', default=None, type=str, help='lol client path')
args = parser.parse_args()

f=open("data.txt", 'r')
file_list=f.readlines()
f.close()

if len(file_list) < 4:
    if args.api_key is None or args.name is None or args.limit is None or args.path is None:
        print('plz init')
        exit(0)
    file_list = ['','','','']

if args.api_key is not None:
    file_list[0] = args.api_key+'\n'
if args.name is not None:
    file_list[1] = args.name+'\n'
if args.limit is not None:
    file_list[2] = str(args.limit)+'\n'
if args.path is not None:
    file_list[3] = str(args.limit)+'\n'

f = open('data.txt', 'w')
f.writelines(file_list)
f.close()

t = MatchTime()

t.check_can_game()