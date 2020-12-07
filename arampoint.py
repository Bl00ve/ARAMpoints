#TODO
"""
#Note for the future, to delete all previous git commits and start over - https://stackoverflow.com/questions/13716658/how-to-delete-all-commit-history-in-github

- Add total games played for all players
- Send output to CSV 
- Add multi region support (Messi-JP)

=====================
Achievements to Add
=====================
Weekend 1
----------
+ Highest Average KDA
+ Highest Average Deaths
+ Highest Average Assists
+ Most Penta Kills
Most Wins
Most kills in a single game
Most CC points in a single game
Most damage in a single game
Lose a game as Teemo and count
    
    Special Achievements
    --------------------
    Achievement 1 - Win a game with >=10 deaths as Yasuo
    Achievement 2 - Win a game as Janna and count
    Achievement 3 - Lose a game as Teemo and count

Weekend 2
---------
Played the same champion the most
"""

import requests, time, pandas, json, datetime, pytz, urllib, config, playerlist, csv, sys
from pandas.io.json import json_normalize
from config import APIKEY
from playerlist import lookuplist

# Variables
REGION = 'na1'
windowstart = datetime.datetime(2020, 12, 5)
windowend = datetime.datetime(2020, 12, 6)
apirequest = 0

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
                        points[matchid]['Win'] = str(players['stats']['win'])
                        if points[matchid]['Win'] == 'True' and points[matchid]['Champ'] == 'Yasuo' and points[matchid]['Deaths'] >= 10:
                            points[matchid['Achievement1'] = 1
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
    snowdowngames = 0
    print('[+] Data is taken from ' + str(windowstart.strftime('%Y-%m-%d')) + ' to ' +str(windowend.strftime('%Y-%m-%d')))
    # Start output file
    file = open('weekend1.csv', 'w', newline = '')
    with file:
        header = [
                    'Summoner',
                    'Games Played',
                    'Total Kills',
                    'Total Deaths',
                    'Total Assists',
                    'Average Kills',
                    'Average Deaths',
                    'Average Assists',
                    'Total KDA',
                    'Double Kills',
                    'Triple Kills',
                    'Quadra Kills',
                    'Penta Kills',
                    'First Bloods',
                    'Total CC Score',
                    'Average CC Score',
                    'Total Damage Dealt',
                    'Average Damage Dealt',
                    'Total Killing Sprees',
                    'Total Average KDA',
                    'Wins'
                ]
        writer = csv.DictWriter(file, fieldnames = header)

        writer.writeheader()
    file.close()
    apiwait = 0
    for searchSummoner in lookuplist:
        points = {}
        a_summoner = Summoner(searchSummoner)
        arams = Match(a_summoner).arams
        for match in arams.items():
            Match.getarammatchinfo(match[1]['gameId'])
            if apirequest > 60:
                for remaining in range(130, 0, -1):
                    sys.stdout.write('\r')
                    sys.stdout.write('Waiting {:2d} seconds to continue'.format(remaining))
                    sys.stdout.flush()
                    time.sleep(1)
                apiwait += 1
                sys.stdout.write('\r[*] API wait #' + str(apiwait) + ' has finished   \n')
                apirequest = 0
                # time.sleep(120)
                # apirequest = 0
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
            wins = 0
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
                if points[match]['FirstBlood'] == 'True':
                    firstblood += 1
                if int(points[match]['CC']) > 0:
                    ccscore += int(points[match]['CC'])
                if int(points[match]['DamageDealt']) > 0:
                    damagedealt += int(points[match]['DamageDealt'])
                if int(points[match]['KillingSprees']) > 0:
                    killingsprees += int(points[match]['KillingSprees'])
                if points[match]['Win'] == 'True':
                    wins += 1
                #if datetime.datetime.strptime((points[match]['LongestLife']),'%H:%M:%S') > datetime.datetime.strptime('0:0:0','%H:%M:%S'):
                #    lifetime += datetime.timedelta((points[match]['LongestLife']),'%H:%M:%S')
            file = open('weekend1.csv', 'a+', newline = '')
            with file:
                writer = csv.DictWriter(file, fieldnames = header)
                writer.writerow({
                                    'Summoner' : searchSummoner,
                                    'Games Played' : str(len(points)),
                                    'Total Kills' : str(killpoints),
                                    'Total Deaths' : str(deathpoints),
                                    'Total Assists' : str(assistpoints),
                                    'Average Kills' : str(round(killpoints/len(points),0)),
                                    'Average Deaths' : str(round(deathpoints/len(points),0)),
                                    'Average Assists' : str(round(assistpoints/len(points),0)),
                                    'Total KDA' : str(round(((killpoints + assistpoints) / deathpoints),0)),
                                    'Double Kills' : str(doublekills),
                                    'Triple Kills' : str(triplekills),
                                    'Quadra Kills' : str(quadrakills),
                                    'Penta Kills' : str(pentakills),
                                    'First Bloods' : str(firstblood),
                                    'Total CC Score' : str(ccscore),
                                    'Average CC Score' : str(round(ccscore/len(points),0)),
                                    'Total Damage Dealt' : str(damagedealt),
                                    'Average Damage Dealt' :  str(round(damagedealt/len(points),0)),
                                    'Total Killing Sprees' : str(killingsprees),
                                    'Total Average KDA' : str(round((round(killpoints/len(points),0)) + (round(assistpoints/len(points),0)) / (round(deathpoints/len(points),0))),0),
                                    'Wins' : str(wins),
                                    'Win Average' : str(round(wins/len(points),2))
                                 })
            # Text output in terminal
            print('[+] Getting data for ' + points[match]['SummonerName'])
            snowdowngames += len(points) 
            # print('[*] Number of Games - ' + str(len(points)))
            # print('[*] Total Kills - ' + str(killpoints))
            # print('[*] Total Deaths - ' + str(deathpoints))
            # print('[*] Total Assists - ' + str(assistpoints))
            # print('[*] Average Kills - ' + str(round(killpoints/len(points),2)))
            # print('[*] Average Deaths - ' + str(round(deathpoints/len(points),2)))
            # print('[*] Average Assists - ' + str(round(assistpoints/len(points),2)))
            # print('[*] Total KDA - ' + str(round(((killpoints + assistpoints) / deathpoints),2)))
            # print('[*] Number of Double Kills - ' + str(doublekills))
            # print('[*] Number of Triple Kills - ' + str(triplekills))
            # print('[*] Number of Quadra Kills - ' + str(quadrakills))
            # print('[*] Number of Penta Kills - ' + str(pentakills))
            # print('[*] Number of First Bloods - ' + str(firstblood))
            # print('Time Spent Alive - ' + str(lifetime))
            # print('Average Life Span - ' + )
            # print('Average Time Spent Alive - ' + str(round(lifetime/len(points),2)))
            # print('[*] Total CC Score - ' + str(ccscore))
            # print('[*] Average CC Score - ' + str(round(ccscore/len(points),2)))
            # print('[*] Total Damage Dealt - ' + str(damagedealt))
            # print('[*] Average Damage Dealt - ' +  str(round(damagedealt/len(points),2)))
            # print('[*] Total Killing Sprees - ' + str(killingsprees))
            # print('[*] Total First Bloods - ' + str(firstblood))
            # print('')
        #    getmatchinfo(arams[0]['gameId'])
        else:
            file = open('weekend1.csv', 'a+', newline = '')
            with file:
                writer = csv.DictWriter(file, fieldnames = header)
                writer.writerow({
                                    'Summoner' : searchSummoner,
                                    'Games Played' : 'N/A',
                                    'Total Kills' : 'N/A',
                                    'Total Deaths' : 'N/A',
                                    'Total Assists' : 'N/A',
                                    'Average Kills' : 'N/A',
                                    'Average Deaths' : 'N/A',
                                    'Average Assists' : 'N/A',
                                    'Total KDA' : 'N/A',
                                    'Double Kills' : 'N/A',
                                    'Triple Kills' : 'N/A',
                                    'Quadra Kills' : 'N/A',
                                    'Penta Kills' : 'N/A',
                                    'First Bloods' : 'N/A',
                                    'Total CC Score' : 'N/A',
                                    'Average CC Score' : 'N/A',
                                    'Total Damage Dealt' : 'N/A',
                                    'Average Damage Dealt' :  'N/A',
                                    'Total Killing Sprees' : 'N/A',
                                    'Total Average KDA' : 'N/A',
                                    'Wins' : 'N/A'
                                    'Win Average' : 'N/A'
                                 })
            print('[!] ' + searchSummoner + ' hasn\'t played any ARAM games in this time period')
            #print('')
    file.close()
    print('[*] Total Snowdown Showdown Games Played - ' + str(snowdowngames))
    for remaining in range(130, 0, -1):
        sys.stdout.write('\r')
        sys.stdout.write('Waiting {:2d} seconds to continue'.format(remaining))
        sys.stdout.flush()
        time.sleep(1)
    apiwait += 1
    sys.stdout.write('\r[*] API wait #' + str(apiwait) + ' has finished   \n')
    

if __name__ == '__main__':
    main()