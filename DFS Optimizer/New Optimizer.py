import requests
import statistics as s
from bs4 import BeautifulSoup
from functions import *

# define lists and dicts to be populated later
playerPointDicts = []
playerPassAttemptsDicts = []
playerRushDicts = []
playerRecDicts = []
playerTarDicts = []
positionDict = {}
playerTeamDict = {}
finalPlayerList = []
playerOppList = []
playerMasterPointDict = {}
playerMasterRushDict = {}
playerMasterRecDict = {}
playerMasterTarDict = {}
# define dictionaries containing useful info about all 32 teams
teamAbbrevDict = {'Ari': 'Cardinals', 'Atl': 'Falcons', 'Bal': 'Ravens', 'Buf': 'Bills', 'Car': 'Panthers',
                  'Chi': 'Bears', 'Cin': 'Bengals', 'Cle': 'Browns', 'Dal': 'Cowboys', 'Den': 'Broncos', 'Det': 'Lions',
                  'GB': 'Packers', 'Hou': 'Texans', 'Ind': 'Colts', 'Jax': 'Jaguars', 'KC': 'Chiefs', 'LAC': 'Chargers',
                  'LAR': 'Rams', 'Mia': 'Dolphins', 'Min': 'Vikings', 'NE': 'Patriots', 'NO': 'Saints', 'NYG': 'Giants',
                  'NYJ': 'Jets', 'Oak': 'Raiders', 'Phi': 'Eagles', 'Pit': 'Steelers', 'SF': '49ers', 'Sea': 'Seahawks',
                  'TB': 'Buccaneers', 'Ten': 'Titans', 'Wsh': 'Redskins'}
teamNames = {'Arizona': 'Cardinals', 'Atlanta': 'Falcons', 'Baltimore': 'Ravens', 'Buffalo': 'Bills',
             'Carolina': 'Panthers', 'Chicago': 'Bears', 'Cincinnati': 'Bengals', 'Cleveland': 'Browns',
             'Dallas': 'Cowboys', 'Denver': 'Broncos', 'Detroit': 'Lions', 'Green Bay': 'Packers', 'Houston': 'Texans',
             'Indianapolis': 'Colts', 'Jacksonville': 'Jaguars', 'Kansas City': 'Chiefs',
             'Los Angeles': ['Chargers', 'Rams'], 'Miami': 'Dolphins', 'Minnesota': 'Vikings',
             'New England': 'Patriots',
             'New Orleans': 'Saints', 'New York': ['Giants', 'Jets'], 'Oakland': 'Raiders',
             'Philadelphia': 'Eagles', 'Pittsburgh': 'Steelers', 'San Francisco': '49ers', 'Seattle': 'Seahawks',
             'Tampa Bay': 'Buccaneers', 'Tennessee': 'Titans', 'Washington': 'Redskins'}

# sets first n weeks of data to be considered
playerCount = 0
weeks = 2
# begin looping over each week of the season
for week in range(weeks):
    print('Compiling Week ' + str(week + 1) + ' stats...')
    playerList = []
    positionList = []
    playerTeamList = []
    passAttemptsList = []
    rushList = []
    recList = []
    tarList = []
    pointsList = []
    playerCount = 0
    # begin looping over ESPN pages 50 players at a time up to 250
    while playerCount <= 200:
        # make http request to ESPN for full page html
        playerSession = requests.session()
        playerUrl = 'http://games.espn.com/ffl/leaders?&scoringPeriodId=' + str(
            week + 1) + '&seasonId=2018&startIndex=' + str(playerCount)
        playerReq = playerSession.get(playerUrl)
        playerDoc = BeautifulSoup(playerReq.content, 'html.parser')
        playerText = str(playerDoc.get_text)

        # find instance of substring to denote locations of all player names on page
        playerIndexList = []
        findAll(playerText, 'teamid="-2147483648">', playerIndexList)

        # add players and points to respective lists from HTML
        for index in playerIndexList:
            playerLowerIndex = index + len('teamid="-2147483648">')
            playerMiddleIndex = playerText.find('<', playerLowerIndex)
            playerUpperIndex = playerText.find('<', playerMiddleIndex + 1)
            player = playerText[playerLowerIndex: playerUpperIndex]
            if not player.startswith('<img'):
                pointsLowerIndex = playerText.find('appliedPoints appliedPointsProGameFinal', playerUpperIndex) + len(
                    'appliedPoints appliedPointsProGameFinal') + 2
                pointsUpperIndex = playerText.find('<', pointsLowerIndex)
                points = playerText[pointsLowerIndex: pointsUpperIndex]
                # account for case when points = '--'
                if playerText.find('playertableStat appliedPoints">--<', playerUpperIndex,
                                   pointsUpperIndex) != -1 or points.startswith('HTML PUBLIC'):
                    points = '--'
                # eliminate case when player is on IR, SSPD, Out or a free agent
                injuredReserveIndex = playerText.find('font-weight:bold;color: red;" title="IR"', playerUpperIndex,
                                                      pointsLowerIndex)
                suspendedIndex = playerText.find('font-weight:bold;color: red;" title="SSPD"', playerUpperIndex,
                                                 pointsLowerIndex)
                outIndex = playerText.find('font-weight:bold;color: red;" title="O"', playerUpperIndex,
                                           pointsLowerIndex)
                # begin to add in-scope players and points to lists
                infoString = player[player.find('</a>'):]
                if injuredReserveIndex == -1 and suspendedIndex == -1 and outIndex == -1 and 'FA' not in infoString:
                    playerName = player[:player.find('<')]
                    playerList.append(playerName)
                    pointsList.append(points)
                    # get rushes, receptions, and targets for each player and add them to respective lists
                    statsString = playerText[playerUpperIndex: pointsLowerIndex]
                    passAttempts = findstat(statsString, '</td><td class="playertableStat ">', 1)
                    rushes = findstat(statsString, '</td><td class="playertableStat ">', 5)
                    recs = findstat(statsString, '</td><td class="playertableStat ">', 8)
                    tars = findstat(statsString, '</td><td class="playertableStat ">', 11)
                    passAttemptsList.append(passAttempts)
                    rushList.append(rushes)
                    recList.append(recs)
                    tarList.append(tars)
                    # get opponent of current week and whether home or away
                    if week + 1 == weeks:
                        oppLowerIndex = playerText.find('href="" instance="_ppc">', playerUpperIndex) + len(
                            'href="" instance="_ppc">')
                        oppUpperIndex = playerText.find('<', oppLowerIndex)
                        opponent = playerText[oppLowerIndex: oppUpperIndex]
                        if opponent.startswith('@'):
                            playerOpp = teamAbbrevDict.get(opponent[1:])
                            homeOrAway = 'away'
                        else:
                            playerOpp = teamAbbrevDict.get(opponent)
                            homeOrAway = 'home'
                        playerOppList.append(playerOpp)
                    # add player's position to position list
                    if 'QB' in infoString:
                        positionList.append('QB')
                    elif 'RB' in infoString:
                        positionList.append('RB')
                    elif 'WR' in infoString:
                        positionList.append('WR')
                    elif 'TE' in infoString:
                        positionList.append('TE')
                    elif 'K' in infoString:
                        positionList.append('K')
                    elif 'D/ST' in infoString:
                        positionList.append('D/ST')
                    # add abbreviated team name to list
                    if playerName[-4:] == 'D/ST':
                        for team in teamAbbrevDict.values():
                            if playerName.find(team) != -1:
                                playerTeamList.append(team)
                                break
                    else:
                        for team in teamAbbrevDict.keys():
                            if infoString.find(team) != -1:
                                playerTeamList.append(teamAbbrevDict.get(team))
                                break
        playerCount += 50

    # put players and stats into master dictionary lists, 1 for each week
    playersAndPoints = dict(zip(playerList, pointsList))
    playerPointDicts.append(playersAndPoints)

    playersAndPassAttempts = dict(zip(playerList, passAttemptsList))
    playerPassAttemptsDicts.append(playersAndPassAttempts)

    playersAndRushes = dict(zip(playerList, rushList))
    playerRushDicts.append(playersAndRushes)

    playersAndRecs = dict(zip(playerList, recList))
    playerRecDicts.append(playersAndRecs)

    playersAndTars = dict(zip(playerList, tarList))
    playerTarDicts.append(playersAndTars)

    # now that we have a list of players updated to last week, let's make the final dictionaries
    if week + 1 == weeks:
        # put players and positions into master dictionary
        playersAndPositions = dict(zip(playerList, positionList))
        for player, position in playersAndPositions.items():
            if player not in positionDict.keys():
                positionDict.update({player: position})

        # put players and teams into master dictionary
        playersAndTeams = dict(zip(playerList, playerTeamList))
        for player, team in playersAndTeams.items():
            if player not in playerTeamDict.keys():
                playerTeamDict.update({player: team})
        finalPlayerList = playerList

# put players and opponents into master dictionary
playersAndOpps = dict(zip(finalPlayerList, playerOppList))

# create dictionaries that organizes players with their weekly stats
for player in positionDict.keys():
    # only add stats if the player played in the game
    for i in range(len(playerPointDicts)):
        if positionDict.get(player) == 'QB' and playerPassAttemptsDicts[i].get(player) == '0/0':
            continue
        elif positionDict.get(player) == 'RB' and playerRushDicts[i].get(player) == 0:
            continue
        elif positionDict.get(player) == 'WR' and playerTarDicts[i].get(player) == 0:
            continue
        elif positionDict.get(player) == 'TE' and playerTarDicts[i].get(player) == 0:
            continue
        else:
            playerRushes = []
            playerRushes.append(playerRushDicts[i].get(player))
            playerMasterRushDict.update({player: playerRushes})
            playerRecs = []
            playerRecs.append(playerRecDicts[i].get(player))
            playerMasterRecDict.update({player: playerRecs})
            playerTars = []
            playerTars.append(playerTarDicts[i].get(player))
            playerMasterTarDict.update({player: playerTars})
            # only add weekly points if player actually played
            playerPoints = []
            playerPoints.append(playerPointDicts[i].get(player))
            playerMasterPointDict.update({player: playerPoints})

# get fantasy points allowed by position
pointsAllowedDictList = []
positions = [1, 2, 3, 4, 5, 16]
for position in positions:
    # make http request to ESPN for full page html
    teamSession = requests.session()
    teamUrl = 'http://games.espn.com/ffl/pointsagainst?positionId=' + str(position)
    teamReq = teamSession.get(teamUrl)
    teamDoc = BeautifulSoup(teamReq.content, 'html.parser')
    teamText = str(teamDoc.get_text)

    # find instance of substring to denote locations of all team names on page
    teamIndexList = []
    findAll(teamText, 'href="" instance="_ppc">', teamIndexList)

    teamList = []
    pointsAllowedList = []
    # add teams and points allowed for each team in html
    for index in teamIndexList:
        teamLowerIndex = index + len('href="" instance="_ppc">')
        teamUpperIndex = teamText.find('<', teamLowerIndex)
        team = teamText[teamLowerIndex: teamUpperIndex]
        teamList.append(team)
        pointsAllowedLowerIndex = teamText.find('"playertableStat appliedPoints">', teamUpperIndex) + len(
            '"playertableStat appliedPoints">')
        pointsAllowedUpperIndex = teamText.find('<', pointsAllowedLowerIndex)
        if teamText[pointsAllowedLowerIndex: pointsAllowedUpperIndex] != '--':
            pointsAllowed = float(teamText[pointsAllowedLowerIndex: pointsAllowedUpperIndex])
            pointsAllowedList.append(pointsAllowed)
    # add teams and points allowed to dictionaries
    teamsAndPointsAllowed = dict(zip(teamList, pointsAllowedList))
    pointsAllowedDictList.append(teamsAndPointsAllowed)

# create master lists to be populated
playerMaxPointsDict = {}
playerMinPointsDict = {}
playerAvgPointsDict = {}
playerStdPointsDict = {}

for player, weeklyPoints in playerMasterPointDict.items():
    playerMaxPointsDict.update({player: getmax(weeklyPoints)})
    playerMinPointsDict.update({player: getmin(weeklyPoints)})
    playerAvgPointsDict.update({player: round(getavg(weeklyPoints), 1)})
    playerStdPointsDict.update({player: getstd(weeklyPoints)})

# get average player usage
playerMasterUsageDict = {}
for player in playerMasterRushDict.keys():
    playerUsageList = []
    playerUsage = getavg(playerMasterRushDict.get(player)) + getavg(playerMasterRecDict.get(player)) + getavg(
        playerMasterTarDict.get(player))
    playerMasterUsageDict.update({player: round(playerUsage, 1)})

# define positions and populate master dictionary with players and final projected points
positionNames = ['QB', 'RB', 'WR', 'TE', 'K', 'D/ST']
overallPlayerScoresDict = {}
for player, position in positionDict.items():
    if playerAvgPointsDict.get(player):
        playerPositionIndex = positionNames.index(position)
        avgPoints = playerAvgPointsDict.get(player)
        avgUsage = playerMasterUsageDict.get(player)
        ceiling = playerMaxPointsDict.get(player)
        floor = playerMinPointsDict.get(player)
        std = playerStdPointsDict.get(player)
        oppStrengthDict = pointsAllowedDictList[playerPositionIndex]
        playerOpp = playersAndOpps.get(player)
        oppPointsAllowed = oppStrengthDict.get(str(playerOpp) + ' vs. ' + str(position))
        # calculate adjusted projected points based on other data
        overallScoreFloat = (0.7 * avgPoints) + (0.2 * avgUsage) + (0.025 * ceiling) + (0.025 * floor) + (
                    0.025 * std) + (
                                    0.025 * oppPointsAllowed)
        overallScore = float(round(overallScoreFloat, 2))
        overallPlayerScoresDict.update({player: overallScore})

# incorporate DFS salaries into the mix


# define function that determines whether a player is a player or a defense
def playerCheck(name):
    player = True
    for city in teamNames.keys():
        # check for NY and LA teams
        if isinstance(teamNames.get(city), list):
            for team in teamNames.get(city):
                if team in name:
                    player = False
                    return str(team) + ' D/ST'
        else:
            # check for the city and team name in the string
            if city in name or teamNames.get(city) in name:
                player = False
                team = teamNames.get(city)
                return str(team) + ' D/ST'
            # use case where it just says "New England"
            elif city == name:
                player = False
                return str(city) + ' D/ST'
    # if player is never set to False, we know it's a player
    if player:
        return name


# set up request to site for both DraftKings and Fanduel salaries
sites = ['Draftkings', 'FanDuel']
siteSalaries = []
for site in sites:
    # make http request to scrape html
    dfsSession = requests.session()
    dfsUrl = 'https://www.footballdiehards.com/fantasyfootball/dailygames/' + str(site) + '-Salary-data.cfm'
    dfsReq = dfsSession.get(dfsUrl)
    dfsDoc = BeautifulSoup(dfsReq.content, 'html.parser')
    dfsText = str(dfsDoc.get_text)

    # lines containing players & salaries start with that substring
    dfsPlayerIndexList = []
    findAll(dfsText, '<td style="text-align:left;padding-left:10px;">', dfsPlayerIndexList)

    dfsPlayerList = []
    dfsSalaryList = []

    # find string indices of players and salaries and put them in lists
    for index in dfsPlayerIndexList:
        dfsLowerNameIndex = index + len('<td style="text-align:left;padding-left:10px;">')
        dfsUpperNameIndex = dfsText.find('<', dfsLowerNameIndex)
        dfsLowerSalaryIndex = dfsText.find('<sup>$</sup>', dfsUpperNameIndex) + len('<sup>$</sup>')
        dfsUpperSalaryIndex = dfsText.find('<', dfsLowerSalaryIndex)
        dfsPlayer = dfsText[dfsLowerNameIndex: dfsUpperNameIndex]
        dfsSalary = int(dfsText[dfsLowerSalaryIndex: dfsUpperSalaryIndex])
        dfsSalaryList.append(dfsSalary)
        result = playerCheck(dfsPlayer)
        if result.endswith('D/ST'):
            dfsPlayerList.append(result)
        else:
            dfsLastNameIndex = dfsText.find(',', dfsLowerNameIndex)
            dfsLastName = dfsText[dfsLowerNameIndex: dfsLastNameIndex]
            dfsFirstName = (dfsText[dfsLastNameIndex + 1: dfsUpperNameIndex])[1:]
            dfsPlayerName = str(dfsFirstName) + ' ' + str(dfsLastName)
            dfsPlayerList.append(dfsPlayerName)

    # put players and salaries into dictionary
    dfsPlayersAndSalaries = dict(zip(dfsPlayerList, dfsSalaryList))
    siteSalaries.append(dfsPlayersAndSalaries)

    # prints accumulated salaries from each site
    print(str(site) + ' salaries:')
    print(dfsPlayersAndSalaries)

# set salary dict to be FanDuel for now
playerSalaries = siteSalaries[1]


def getTotal(players, data):
    dataList = []
    for player in players:
        dataList.append(data.get(player))
    return sum(dataList)


playerListForLineup = list(playerSalaries.keys())

playerQBList = []
playerRBList = []
playerWRList = []
playerTEList = []
playerFLEXList = []
playerDSTList = []

for player in playerListForLineup:
    if positionDict.get(player) == 'QB':
        playerQBList.append(player)
    if positionDict.get(player) == 'RB':
        playerRBList.append(player)
        playerFLEXList.append(player)
    if positionDict.get(player) == 'WR':
        playerWRList.append(player)
        playerFLEXList.append(player)
    if positionDict.get(player) == 'TE':
        playerTEList.append(player)
        playerFLEXList.append(player)
    if positionDict.get(player) == 'D/ST':
        playerDSTList.append(player)

# print(len(playerQBList))
# print(len(playerRBList))
# print(len(playerWRList))
# print(len(playerTEList))
# print(len(playerFLEXList) - 3)
# print(len(playerDSTList))

if playerSalaries:
    # create optimal DFS lineup!
    # maximize total projected points with constraint of salary cap
    optimalLineup = {}
    # set salary cap to 50k for Draftkings and 60k for Fanduel
    salaryCap = 60000
    bestLineup = []
    maxPoints = 0

    for qb in playerQBList:
        salaryTotal = 0
        while salaryTotal <= salaryCap:
            for rb1 in playerRBList:
                for rb2 in playerRBList:
                    if rb1 != rb2:
                        for wr1 in playerWRList:
                            for wr2 in playerWRList:
                                if wr1 != wr2:
                                    for wr3 in playerWRList:
                                            if wr3 not in {wr1, wr2}:
                                                for te in playerTEList:
                                                    for flex in playerFLEXList:
                                                        if flex not in {rb1, rb2, wr1, wr2, wr3, te}:
                                                            for dst in playerDSTList:
                                                                thisLineup = [qb, rb1, rb2, wr1, wr2, wr3, te, flex, dst]
                                                                salaryTotal = getTotal(thisLineup, playerSalaries)
                                                                thisPointTotal = getTotal(thisLineup, overallPlayerScoresDict)
                                                                if thisPointTotal > maxPoints:
                                                                    bestLineup = thisLineup
                                                                    maxPoints = thisPointTotal

    print(bestLineup)
    print(round(maxPoints, 1))
    print(getTotal(bestLineup, playerSalaries))

# why is there only the Rams D???
#
#     # print output!
#     positionOrder = ['QB', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE', 'FLEX', 'D/ST']
#     for pos in positionOrder:
#         player = optimalLineup.get(pos)
#         print(str(pos) + ': ' + str(player) + ' - $' + str(playerSalaries.get(player)))
#     print('Remaining salary: ' + str(salaryCap - maxPointsSalary))
#
#     # make sure final code gets current week and sets "weeks" to that number
#     # put an "if projected points from ESPN = 0, exclude this player"
# else:
#     print('No salary data available.')
