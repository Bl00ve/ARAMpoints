import requests, time, pandas, json, datetime, pytz, urllib
from pandas.io.json import json_normalize

# Variables
REGION = 'na1'
APIKEY = ''
if APIKEY == '':
    print('Don\'t forget to insert your API key')
tournamentstart = datetime.datetime(2020, 10, 7)
tournamentend = datetime.datetime(2020, 10, 14)
#searchSummoner = 'We Need a 5th'
lookuplist = ['We Need a 5th', 'Bloodvault', 'Hottie2Naughty', 'Dul', 'Khaosix', 'Swagtasticles']

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
        URL = 'https://' + REGION + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name + '?api_key=' + APIKEY
        response = requests.get(URL)
        self.accountid = response.json()['accountId']

    def getname(self, accountid):
        URL = 'https://'+ REGION +'.api.riotgames.com/lol/summoner/v4/summoners/by-accountid/' + accountid + '?api_key=' + APIKEY
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
        time.sleep(120)
        URL = 'https://' + REGION + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountid + '?api_key=' + APIKEY
        #response = requests.get(URL)
        response = urllib.request.urlopen(URL).read()
        self.matchhistory = json.loads(response)
    
    def getarams(self, Summoner):
        aram_match = {}
        i = 0
        for match in self.matchhistory['matches']:
            if (match['queue'] == 450) or (match['queue'] == 931) or (match['queue'] == 452) or (match['queue'] == 451) or (match['queue'] == 62) or (match['queue'] == 63) or (match['queue'] == 64) or (match['queue'] == 65) or (match['queue'] == 930):
                match['timestamp'] = Match.getmatchdate(match['timestamp'])
                if tournamentend >= match['timestamp'] >= tournamentstart:
                    aram_match[i] = match
                    i += 1
                else:
                    pass
            else:
                pass
        self.arams = aram_match

    def getmatchdate(ts):
        pacific = datetime.timedelta(hours=8)
        #return (datetime.datetime.utcfromtimestamp(ts/1000) - pacific).strftime('%Y-%m-%d %H:%M:%S')
        return (datetime.datetime.utcfromtimestamp(ts/1000) - pacific)

    def getarammatchinfo(match):
        URL = 'https://' + REGION + '.api.riotgames.com/lol/match/v4/matches/' + str(match) + '?api_key=' + APIKEY
        #response = requests.get(URL)
        response = urllib.request.urlopen(URL).read()
        matchinfo = json.loads(response)
        matchinfo['gameCreation'] = Match.getmatchdate(matchinfo['gameCreation'])
        matchinfo['gameDuration'] = str(datetime.timedelta(seconds=(matchinfo['gameDuration'])))
        for participant in matchinfo['participantIdentities']:
            if participant['player']['summonerName'].casefold() == searchSummoner.casefold():
                #if tournamentend > matchinfo['gameCreation'] > tournamentstart:
                for players in matchinfo['participants']:
                    if players['participantId'] == participant['participantId']:
                        matchid = matchinfo['gameId']
                        points[matchid] = {}
                        #print(matchinfo['gameId'], matchinfo['platformId'], matchinfo['gameMode'], matchinfo['gameType'], matchinfo['gameCreation'], matchinfo['gameDuration'])
                        #print('SummonerName - ' + participant['player']['summonerName'])
                        points[matchid]['SummonerName'] = str(participant['player']['summonerName'])
                        #print('Match Date - ' + str(matchinfo['gameCreation']))
                        #print('Game Duration - '  + str(matchinfo['gameDuration']))
                        points[matchid]['GameDuration'] = str(matchinfo['gameDuration'])
                        #print('Champ Played ' + str(Match.getchampid(players['championId'])))
                        points[matchid]['Champ'] = str(Match.getchampid(players['championId']))
                        #print('Kills ' + str(players['stats']['kills']))
                        points[matchid]['Kills'] = str(players['stats']['kills'])
                        #print('Deaths ' + str(players['stats']['deaths']))
                        points[matchid]['Deaths'] = str(players['stats']['deaths'])
                        #print('Assists ' + str(players['stats']['assists']))
                        points[matchid]['Assists'] = str(players['stats']['assists'])
                        #print('Largest Killing Spree ' + str(players['stats']['largestKillingSpree']))
                        points[matchid]['LargestKillingSpree'] = str(players['stats']['largestKillingSpree'])
                        #print('Largest Multi Kill ' + str(players['stats']['largestMultiKill']))
                        points[matchid]['LargestMultiKill'] = str(players['stats']['largestMultiKill'])
                        #print('Killing Sprees ' + str(players['stats']['killingSprees']))
                        points[matchid]['KillingSprees'] = str(players['stats']['killingSprees'])
                        #print('Longest Time Spent Living ' + str(datetime.timedelta(seconds=players['stats']['longestTimeSpentLiving'])))
                        points[matchid]['LongestLife'] = str(datetime.timedelta(seconds=players['stats']['longestTimeSpentLiving']))
                        #print('Double Kills ' + str(players['stats']['doubleKills']))
                        points[matchid]['DoubleKills'] = str(players['stats']['doubleKills'])
                        #print('Triple Kills ' + str(players['stats']['tripleKills']))
                        points[matchid]['TripleKills'] = str(players['stats']['tripleKills'])
                        #print('Quadra Kills ' + str(players['stats']['quadraKills']))
                        points[matchid]['QuadKills'] = str(players['stats']['quadraKills'])
                        #print('Penta Kills ' + str(players['stats']['pentaKills']))
                        points[matchid]['PentaKills'] = str(players['stats']['pentaKills'])
                        #print('Total Damage Dealt '+ str(players['stats']['totalDamageDealtToChampions']))
                        points[matchid]['DamageDealt'] = str(players['stats']['totalDamageDealtToChampions'])
                        #print('Total CC Dealt ' + str(players['stats']['totalTimeCrowdControlDealt']))
                        points[matchid]['CC'] = str(players['stats']['totalTimeCrowdControlDealt'])
                        #print('Got First Blood ' + str(players['stats']['firstBloodKill']))
                        points[matchid]['FirstBlood'] = str(players['stats']['firstBloodKill'])
                        #print('')
                        return points
            else:
                pass

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
    getchampdict()
    print('Data is taken from ' + str(tournamentstart) + ' to ' +str(tournamentend))
    for searchSummoner in lookuplist:
        points = {}
        a_summoner = Summoner(searchSummoner)
        arams = Match(a_summoner).arams
    #    print(arams)
        #Match(a_summoner).matchhistory['matches']
        #print(getarams(a_summoner))
    #    print(Match(a_summoner).arams)
    #    print(arams[0])
        for match in arams.items():
            Match.getarammatchinfo(match[1]['gameId'])
        #print(points)
        if bool(points) == True:
            killpoints = 0
            deathpoints = 0
            assistpoints = 0
            doublekills = 0
            triplekills = 0
            quadrakills = 0
            pentakills = 0
            firstblood = 0
            for match in points:
                killpoints += int(points[match]['Kills'])
                deathpoints += int(points[match]['Deaths'])
                assistpoints += int(points[match]['Assists'])
                if int(points[match]['DoubleKills']) > 0:
                    doublekills += int(points[match]['DoubleKills'])
                if int(points[match]['TripleKills']) > 0:
                    triplekills += int(points[match]['DoubleKills'])
                if int(points[match]['QuadKills']) > 0:
                    quadrakills += int(points[match]['DoubleKills'])
                if int(points[match]['PentaKills']) > 0:
                    pentakills += int(points[match]['DoubleKills'])
                if points[match]['FirstBlood'] == True:
                    firstblood += 1
            print(points[match]['SummonerName'])
            print('Number of Games - ' + str(len(points)))
            print('Total Kills - ' + str(killpoints))
            print('Total Deaths - ' + str(deathpoints))
            print('Total Assists - ' + str(assistpoints))
            print('Total KDA - ' + str(round(((killpoints + assistpoints) / deathpoints),2)))
            print('Number of Double Kills - ' + str(doublekills))
            print('Number of Triple Kills - ' + str(triplekills))
            print('Number of Quadra Kills - ' + str(quadrakills))
            print('Number of Penta Kills - ' + str(pentakills))
            print('Number of First Bloods - ' + str(firstblood))
            print('')
        #    getmatchinfo(arams[0]['gameId'])
        else:
            print(searchSummoner + ' hasn\'t played any ARAM games in this time period')
            print('')
"""
Notable Stats
--------------
matchinfo['participants'][X]['stats'][<see below>]
    kills(int)
    deaths(int)
    assists(int)
    largetsKillingSpree(int)
    largestMultiKill(int)
    killingSprees(int)
    longestTimeSpentLiving(int)
    doubleKills(int)
    tripleKills(int)
    quadraKills(int)
    pentaKills(int)
    totalDamageDealtToChampions(int)
    totalTimeCrowdControlDealt(int)
    firstBloodKill(bool)

wins???

matchinfo['participantIdentities'][X]['participantId']
matchinfo['participantIdentities'][X]['player']['SummonerName']

FAQ
Q - Do I need a team?
A - Single person entry

Q - Do custom games count?
A - No

Q - How many games count?
A - I can only track up to 99 games, if you play more than that you should go outside
"""


if __name__ == '__main__':
    main()