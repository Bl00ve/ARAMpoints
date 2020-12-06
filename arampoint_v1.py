#TODO
"""
- Add total games played for all players
- Send output to CSV 

Achievements to Add
--------------------
Highest Average KDA
Highest Average Deaths
Highest Average Assists
Most Penta Kills
Most Wins
Most kills in a single game
Most CC points in a single game
Most damage in a single game
Win a game with >=10 deaths as Yasuo
Win a game as Janna and count
Lose a game as Teemo and count
"""

import requests, time, pandas, json, datetime, pytz, urllib, config, playerlist
from pandas.io.json import json_normalize
from config import APIKEY
from playerlist import lookuplist

# Variables
REGION = 'na1'
windowstart = datetime.datetime(2020, 12, 5)
windowend = datetime.datetime(2020, 12, 6)
apirequest = 0

# Testing Variables
#accountId = "8l0Jlnj7CxKt3RFAsPp5ZePmwgp1EoD3hdrL1ruDEXqq7Q"
#puuid = "zuCGa6S5b8PXYm3U73IXqEwtYF8L38hm_HUGPQqShcZFDDMIhg4URgegm-fmeOs3zVshSDywAJ5YcQ"
#leagueid = "wCwoTAi3g4eQOLMLCWXRbuHoyGlumOlW3SngCdHrhUs_yks"
#gameId = '3565806531'

# Classes
class Summoner:
    def __init__(self, name):
        if type(name) == list:
            for name in name:
                self.getaccountid(name)
        elif len(name) < 17:
            self.getaccountid(name)
        else:
            self.getname(name)

    def getaccountid(self, name):
        global apirequest
        URL = 'https://' + REGION + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name + '?api_key=' + APIKEY
        apirequest += 1
        response = requests.get(URL)
        self.accountid = response.json()['accountId']

    def getname(self, accountid):
        global apirequest
        URL = 'https://'+ REGION +'.api.riotgames.com/lol/summoner/v4/summoners/by-accountid/' + accountid + '?api_key=' + APIKEY
        apirequest += 1
        response = requests.get(URL)
        self.name = response.json()['name']

class Match:
    def __init__(self, Summoner):
        if type(Summoner) == list:
           for x in Summoner:
               self.getmatchhistory(x.accountid)
        else:
            self.getmatchhistory(Summoner.accountid)
        self.getarams(Summoner)
  
    def getmatchhistory(self, accountid):
        global apirequest
        URL = 'https://' + REGION + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountid + '?api_key=' + APIKEY
        apirequest += 1
        response = urllib.request.urlopen(URL).read()
        self.matchhistory = json.loads(response)
    
    def getarams(self, Summoner):
        aram_match = {}
        i = 0
        for match in self.matchhistory['matches']:
            if (match['queue'] == 450) or (match['queue'] == 931) or (match['queue'] == 452) or (match['queue'] == 451) or (match['queue'] == 62) or (match['queue'] == 63) or (match['queue'] == 64) or (match['queue'] == 65) or (match['queue'] == 930):
                match['timestamp'] = Match.getmatchdate(match['timestamp'])
                if windowend >= match['timestamp'] >= windowstart:
                    aram_match[i] = match
                    i += 1
                else:
                    pass
            else:
                pass
        self.arams = aram_match

    @staticmethod
    def getmatchdate(ts):
        pacific = datetime.timedelta(hours=8)
        return (datetime.datetime.utcfromtimestamp(ts/1000) - pacific)

    @staticmethod
    def getarammatchinfo(match):
        global apirequest
        URL = 'https://' + REGION + '.api.riotgames.com/lol/match/v4/matches/' + str(match) + '?api_key=' + APIKEY
        apirequest += 1
        response = urllib.request.urlopen(URL).read()
        matchinfo = json.loads(response)
        matchinfo['gameCreation'] = Match.getmatchdate(matchinfo['gameCreation'])
        matchinfo['gameDuration'] = str(datetime.timedelta(seconds=(matchinfo['gameDuration'])))
        for participant in matchinfo['participantIdentities']:
            if participant['player']['summonerName'].casefold() == searchSummoner.casefold():
                for players in matchinfo['participants']:
                    if players['participantId'] == participant['participantId']:
                        matchid = matchinfo['gameId']
                        points[matchid] = {}
                        points[matchid]['SummonerName'] = str(participant['player']['summonerName'])
                        points[matchid]['GameDuration'] = str(matchinfo['gameDuration'])
                        points[matchid]['Champ'] = str(Match.getchampid(players['championId']))
                        points[matchid]['Kills'] = str(players['stats']['kills'])
                        points[matchid]['Deaths'] = str(players['stats']['deaths'])
                        points[matchid]['Assists'] = str(players['stats']['assists'])
                        points[matchid]['LargestKillingSpree'] = str(players['stats']['largestKillingSpree'])
                        points[matchid]['LargestMultiKill'] = str(players['stats']['largestMultiKill'])
                        points[matchid]['KillingSprees'] = str(players['stats']['killingSprees'])
                        points[matchid]['LongestLife'] = str(datetime.timedelta(seconds=players['stats']['longestTimeSpentLiving']))
                        points[matchid]['DoubleKills'] = str(players['stats']['doubleKills'])
                        points[matchid]['TripleKills'] = str(players['stats']['tripleKills'])
                        points[matchid]['QuadKills'] = str(players['stats']['quadraKills'])
                        points[matchid]['PentaKills'] = str(players['stats']['pentaKills'])
                        points[matchid]['DamageDealt'] = str(players['stats']['totalDamageDealtToChampions'])
                        points[matchid]['CC'] = str(players['stats']['totalTimeCrowdControlDealt'])
                        points[matchid]['FirstBlood'] = str(players['stats']['firstBloodKill'])
                        return points
            else:
                pass

    @staticmethod
    def getchampid(champid):
        for key, value in champdict.items():
            if str(champid) == value:
                return key  
        #return next((k for k, v in champdict.items() if v == champid), None)

def getchampdict():
    global champdict
    versionURL = 'https://ddragon.leagueoflegends.com/api/versions.json'
    versionresponse = urllib.request.urlopen(versionURL).read()
    patches = versionresponse
    patches = [patches.decode('utf-8')]
    currentpatch = patches[0][2:9]
    champdict = {}
    URL = 'http://ddragon.leagueoflegends.com/cdn/' + currentpatch + '/data/en_US/champion.json'
    response = urllib.request.urlopen(URL).read()
    champlib = json.loads(response)
    for champion in champlib['data']:
        champdict[champlib['data'][champion]['name']] = champlib['data'][champion]['key']
    return champdict

def main():
    global points
    global searchSummoner
    global apirequest
    getchampdict()
    #apirequest = 0
    print('Data is taken from ' + str(windowstart.strftime('%Y-%m-%d')) + ' to ' +str(windowend.strftime('%Y-%m-%d')))
    for searchSummoner in lookuplist:
        points = {}
        a_summoner = Summoner(searchSummoner)
        arams = Match(a_summoner).arams
        for match in arams.items():
            Match.getarammatchinfo(match[1]['gameId'])
            if apirequest > 60:
                time.sleep(120)
                apirequest = 0
        if bool(points) == True:
            killpoints = 0
            deathpoints = 0
            assistpoints = 0
            doublekills = 0
            triplekills = 0
            quadrakills = 0
            pentakills = 0
            firstblood = 0
            ccscore = 0
            damagedealt = 0
            killingsprees = 0
            #lifetime = datetime.datetime('0:0:0','%H:%M:%S')
            for match in points:
                killpoints += int(points[match]['Kills'])
                deathpoints += int(points[match]['Deaths'])
                assistpoints += int(points[match]['Assists'])
                if int(points[match]['DoubleKills']) > 0:
                    doublekills += int(points[match]['DoubleKills'])
                if int(points[match]['TripleKills']) > 0:
                    triplekills += int(points[match]['TripleKills'])
                if int(points[match]['QuadKills']) > 0:
                    quadrakills += int(points[match]['QuadKills'])
                if int(points[match]['PentaKills']) > 0:
                    pentakills += int(points[match]['PentaKills'])
                if points[match]['FirstBlood'] == True:
                    firstblood += 1
                if int(points[match]['CC']) > 0:
                    ccscore += int(points[match]['CC'])
                if int(points[match]['DamageDealt']) > 0:
                    damagedealt += int(points[match]['DamageDealt'])
                if int(points[match]['KillingSprees']) > 0:
                    killingsprees += int(points[match]['KillingSprees'])
                #if datetime.datetime.strptime((points[match]['LongestLife']),'%H:%M:%S') > datetime.datetime.strptime('0:0:0','%H:%M:%S'):
                #    lifetime += datetime.timedelta((points[match]['LongestLife']),'%H:%M:%S')
            print(points[match]['SummonerName'])
            print('Number of Games - ' + str(len(points)))
            print('Total Kills - ' + str(killpoints))
            print('Total Deaths - ' + str(deathpoints))
            print('Total Assists - ' + str(assistpoints))
            print('Average Kills - ' + str(round(killpoints/len(points),2)))
            print('Average Deaths - ' + str(round(deathpoints/len(points),2)))
            print('Average Assists - ' + str(round(assistpoints/len(points),2)))
            print('Total KDA - ' + str(round(((killpoints + assistpoints) / deathpoints),2)))
            print('Number of Double Kills - ' + str(doublekills))
            print('Number of Triple Kills - ' + str(triplekills))
            print('Number of Quadra Kills - ' + str(quadrakills))
            print('Number of Penta Kills - ' + str(pentakills))
            print('Number of First Bloods - ' + str(firstblood))
            #print('Time Spent Alive - ' + str(lifetime))
            #print('Average Life Span - ' + )
            #print('Average Time Spent Alive - ' + str(round(lifetime/len(points),2)))
            print('Total CC Score - ' + str(ccscore))
            print('Average CC Score - ' + str(round(ccscore/len(points),2)))
            print('Total Damage Dealt - ' + str(damagedealt))
            print('Average Damage Dealt - ' +  str(round(damagedealt/len(points),2)))
            print('Total Killing Sprees - ' + str(killingsprees))
            print('Total First Bloods - ' + str(firstblood))
            print('')
        #    getmatchinfo(arams[0]['gameId'])
        else:
            print(searchSummoner + ' hasn\'t played any ARAM games in this time period')
            print('')

if __name__ == '__main__':
    main()