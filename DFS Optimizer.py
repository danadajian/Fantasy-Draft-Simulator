import requests
import statistics as s
from bs4 import BeautifulSoup

playerPointDicts = []
playerRushDicts = []
playerRecDicts = []
playerTarDicts = []
positionDict = {}
playerTeamDict = {}
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
playerOppList = []
playerMasterPointDict = {}
playerMasterRushDict = {}
playerMasterRecDict = {}
playerMasterTarDict = {}


# defines function that finds all string indices of a substring
def findAll(string, substring, indexList):
    index = -1
    while True:
        index = string.find(substring, index + 1)
        if index == -1:
            break
        indexList.append(index)


# defines function that finds the nth index of a substring
def findstat(haystack, needle, n):
    statIndex = haystack.find(needle)
    i = 1
    while i < n:
        statIndex = haystack.find(needle, statIndex + len(needle))
        i += 1
    lower = statIndex + len(needle)
    upper = haystack.find('<', lower)
    return haystack[lower: upper]


playerCount = 0
weeks = 2
# begin looping over each week of the season
for week in range(weeks):
    print('Compiling Week ' + str(week + 1) + ' stats...')
    playerList = []
    positionList = []
    playerTeamList = []
    rushList = []
    recList = []
    tarList = []
    pointsList = []
    playerCount = 0
    # begin looping over ESPN pages 50 players at a time up to 250
    while playerCount <= 250:
        playerSession = requests.session()
        playerUrl = 'http://games.espn.com/ffl/leaders?&scoringPeriodId=' + str(
            week + 1) + '&seasonId=2018&startIndex=' + str(playerCount)
        playerReq = playerSession.get(playerUrl)
        playerDoc = BeautifulSoup(playerReq.content, 'html.parser')
        playerText = str(playerDoc.get_text)

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
                # eliminate case when player is on IR, SSPD or a free agent
                injuredReserveIndex = playerText.find('font-weight:bold;color: red;" title="IR"', playerUpperIndex,
                                                      pointsLowerIndex)
                suspendedIndex = playerText.find('font-weight:bold;color: red;" title="IR"', playerUpperIndex,
                                                 pointsLowerIndex)
                infoString = player[player.find('</a>'):]
                if injuredReserveIndex == -1 and suspendedIndex == -1 and 'FA' not in infoString:
                    playerName = player[:player.find('<')]
                    playerList.append(playerName)
                    pointsList.append(points)
                    # get rushes, receptions, and targets for each player and add them to respective lists
                    statsString = playerText[playerUpperIndex: pointsLowerIndex]
                    rushes = findstat(statsString, '</td><td class="playertableStat ">', 5)
                    recs = findstat(statsString, '</td><td class="playertableStat ">', 8)
                    tars = findstat(statsString, '</td><td class="playertableStat ">', 11)
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
                    # add positions to position list
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

        # put players and opponents into master dictionary
        playersAndOpps = dict(zip(playerList, playerOppList))

# create dictionaries that organizes players with their weekly stats
for player in positionDict:
    playerPoints = []
    for dic in playerPointDicts:
        playerPoints.append(dic.get(player))
        playerMasterPointDict.update({player: playerPoints})
    playerRushes = []
    for dic in playerRushDicts:
        playerRushes.append(dic.get(player))
        playerMasterRushDict.update({player: playerRushes})
    playerRecs = []
    for dic in playerRecDicts:
        playerRecs.append(dic.get(player))
        playerMasterRecDict.update({player: playerRecs})
    playerTars = []
    for dic in playerTarDicts:
        playerTars.append(dic.get(player))
        playerMasterTarDict.update({player: playerTars})

# get fantasy points allowed by position

pointsAllowedDictList = []
positions = [1, 2, 3, 4, 5, 16]
for position in positions:
    teamSession = requests.session()
    teamUrl = 'http://games.espn.com/ffl/pointsagainst?positionId=' + str(position)
    teamReq = teamSession.get(teamUrl)
    teamDoc = BeautifulSoup(teamReq.content, 'html.parser')
    teamText = str(teamDoc.get_text)

    teamIndexList = []
    findAll(teamText, 'href="" instance="_ppc">', teamIndexList)

    teamList = []
    pointsAllowedList = []

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

    teamsAndPointsAllowed = dict(zip(teamList, pointsAllowedList))
    pointsAllowedDictList.append(teamsAndPointsAllowed)


def getmax(yourList):
    newList = []
    for item in yourList:
        if item != '--' and item is not None:
            newList.append(item)
    newList = map(float, newList)
    try:
        return max(newList)
    except ValueError:
        return 0


def getmin(yourList):
    newList = []
    for item in yourList:
        if item != '--' and item is not None:
            newList.append(item)
    newList = map(float, newList)
    try:
        return min(newList)
    except ValueError:
        return 0


def getavg(yourList):
    newList = []
    for item in yourList:
        if item != '--' and item is not None:
            newList.append(item)
    newList = map(float, newList)
    try:
        return s.mean(newList)
    except ValueError:
        return 0


def getstd(yourList):
    newList = []
    for item in yourList:
        if item != '--' and item is not None:
            newList.append(item)
    newList = map(float, newList)
    try:
        return round(s.stdev(newList), 1)
    except ValueError:
        return 0


playerMasterList = []
maxPointsList = []
minPointsList = []
avgPointsList = []
stdPointsList = []

for player in playerMasterPointDict.keys():
    playerMasterList.append(player)

for weeklyPoints in playerMasterPointDict.values():
    maxPointsList.append(getmax(weeklyPoints))
    minPointsList.append(getmin(weeklyPoints))
    avgPointsList.append(round(getavg(weeklyPoints), 1))
    stdPointsList.append(getstd(weeklyPoints))

playerMaxPointsDict = dict(zip(playerMasterList, maxPointsList))
playerMinPointsDict = dict(zip(playerMasterList, minPointsList))
playerAvgPointsDict = dict(zip(playerMasterList, avgPointsList))
playerStdPointsDict = dict(zip(playerMasterList, stdPointsList))

playerMasterUsageDict = {}

for player in playerMasterRushDict.keys():
    playerUsageList = []
    playerUsage = getavg(playerMasterRushDict.get(player)) + getavg(playerMasterRecDict.get(player)) + getavg(
        playerMasterTarDict.get(player))
    playerMasterUsageDict.update({player: round(playerUsage, 1)})

ceiling = sorted(playerMaxPointsDict.keys(), key=playerMaxPointsDict.__getitem__, reverse=True)
floor = sorted(playerMinPointsDict.keys(), key=playerMinPointsDict.__getitem__, reverse=True)
average = sorted(playerAvgPointsDict.keys(), key=playerAvgPointsDict.__getitem__, reverse=True)
usage = sorted(playerMasterUsageDict.keys(), key=playerMasterUsageDict.__getitem__, reverse=True)

overallPlayerScoresDict = {}
positionNames = ['QB', 'RB', 'WR', 'TE', 'K', 'D/ST']

for player, position in positionDict.items():
    playerPositionIndex = positionNames.index(position)
    avgPoints = playerAvgPointsDict.get(player)
    avgUsage = playerMasterUsageDict.get(player)
    ceiling = playerMaxPointsDict.get(player)
    floor = playerMinPointsDict.get(player)
    std = playerStdPointsDict.get(player)
    oppStrengthDict = pointsAllowedDictList[playerPositionIndex]
    playerOpp = playersAndOpps.get(player)
    oppPointsAllowed = oppStrengthDict.get(str(playerOpp) + ' vs. ' + str(position))
    overallScoreFloat = (0.7 * avgPoints) + (0.2 * avgUsage) + (0.025 * ceiling) + (0.025 * floor) + (0.025 * std) + (
            0.025 * oppPointsAllowed)
    overallScore = float(round(overallScoreFloat, 2))
    overallPlayerScoresDict.update({player: overallScore})


# incorporate DFS salaries

def playerCheck(name):
    player = True
    for city in teamNames.keys():
        # check for NY and LA teams
        if isinstance(teamNames.get(city), list):
            for team in teamNames.get(city):
                if team in name:
                    player = False
                    return str(team) + ' D/ST'
                    break
        else:
            # check for the city and team name in the string
            if city in name and teamNames.get(city) in name:
                player = False
                team = teamNames.get(city)
                return str(team) + ' D/ST'
                break
            # use case where it just says "New England"
            elif city == name:
                player = False
                return str(city) + ' D/ST'
                break
    # if player is never set to False, we know it's a player
    if player:
        return name


# set up request to site for salaries, can use draftkings or fanduel with site variable
sites = ['Draftkings', 'FanDuel']
siteSalaries = []
for site in sites:
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

    dfsPlayersAndSalaries = dict(zip(dfsPlayerList, dfsSalaryList))
    siteSalaries.append(dfsPlayersAndSalaries)

    print(str(site) + ' salaries:')
    print(dfsPlayersAndSalaries)

# create optimal DFS lineup!
# optimize lineup based on maximizing marginal projected point increase per salary increase
# (going from one player to the next most expensive)
optimalLineup = {}

# sort players with salaries in descending order
draftKingsSalaries = {}
sortedSalaries = sorted(siteSalaries[0], key=siteSalaries[0].__getitem__, reverse=True)
for player in sortedSalaries:
    draftKingsSalaries.update({player: siteSalaries[0].get(player)})
print(draftKingsSalaries)

# calculate marginal score increase per marginal salary increase by each position
# create dictionaries by position containing elements like {player: [score, salary]}
playerQBDict = {}
playerRBDict = {}
playerWRDict = {}
playerTEDict = {}
playerFLEXDict = {}
playerDSTDict = {}
playerDicts = [playerQBDict, playerRBDict, playerWRDict, playerTEDict, playerFLEXDict, playerDSTDict]
for player in draftKingsSalaries.keys():
    if positionDict.get(player) == 'QB':
        playerQBDict.update({player: [overallPlayerScoresDict.get(player), draftKingsSalaries.get(player)]})
    if positionDict.get(player) == 'RB':
        playerRBDict.update({player: [overallPlayerScoresDict.get(player), draftKingsSalaries.get(player)]})
        playerFLEXDict.update({player: [overallPlayerScoresDict.get(player), draftKingsSalaries.get(player)]})
    if positionDict.get(player) == 'WR':
        playerWRDict.update({player: [overallPlayerScoresDict.get(player), draftKingsSalaries.get(player)]})
        playerFLEXDict.update({player: [overallPlayerScoresDict.get(player), draftKingsSalaries.get(player)]})
    if positionDict.get(player) == 'TE':
        playerTEDict.update({player: [overallPlayerScoresDict.get(player), draftKingsSalaries.get(player)]})
        playerFLEXDict.update({player: [overallPlayerScoresDict.get(player), draftKingsSalaries.get(player)]})
    if positionDict.get(player) == 'D/ST':
        playerDSTDict.update({player: [overallPlayerScoresDict.get(player), draftKingsSalaries.get(player)]})

marginalPointsPerDollar = {}
for dictionary in playerDicts:
    playerList = list(dictionary.keys())
    for player in playerList:
        if player != playerList[len(playerList) - 1]:
            nextPlayer = playerList[playerList.index(player) + 1]
            marginalPoints = dictionary.get(player)[0] - dictionary.get(nextPlayer)[0]
            marginalSalary = dictionary.get(player)[1] - dictionary.get(nextPlayer)[1]
            if marginalSalary == 0:
                marginalSalary = 1
            marginalPointsPerSalary = marginalPoints / marginalSalary
            marginalPointsPerDollar.update({player: marginalPointsPerSalary})
        else:
            marginalPointsPerDollar.update({player: 0})

print(marginalPointsPerDollar)
# sort each position by descending overall score per salary dollar
sortedMarginalPoints = sorted(marginalPointsPerDollar, key=marginalPointsPerDollar.__getitem__, reverse=True)
print(sortedMarginalPoints)

# loop 9 times to get exactly 9 players in the lineup
for i in range(2):
    # implement a check for when position slots are full
    takenPositions = []
    if 'QB' in optimalLineup.keys():
        takenPositions.append('QB')
    if 'RB2' in optimalLineup.keys() and 'FLEX' in optimalLineup.keys():
        takenPositions.append('RB')
    if 'WR3' in optimalLineup.keys() and 'FLEX' in optimalLineup.keys():
        takenPositions.append('WR')
    if 'TE' in optimalLineup.keys() and 'FLEX' in optimalLineup.keys():
        takenPositions.append('TE')
    if 'D/ST' in optimalLineup.keys():
        takenPositions.append('D/ST')

player1 = 'Michael Thomas'

print(player1)
print(positionDict.get(player1))
print(draftKingsSalaries.get(player1))

remainingSalary = 50000

# logic for putting players in the lineup and "paying" for them each time
if positionDict.get(player1) == 'RB':
    if not optimalLineup.get('RB1'):
        optimalLineup.update({positionDict.get(player1): player1})
        remainingSalary -= draftKingsSalaries.get(player1)
    elif not optimalLineup.get('RB2'):
        optimalLineup.update({positionDict.get(player1): player1})
        remainingSalary -= draftKingsSalaries.get(player1)
    elif not optimalLineup.get('FLEX'):
        optimalLineup.update({positionDict.get(player1): player1})
        remainingSalary -= draftKingsSalaries.get(player1)
elif positionDict.get(player1) == 'WR':
    if not optimalLineup.get('WR1'):
        optimalLineup.update({positionDict.get(player1): player1})
        remainingSalary -= draftKingsSalaries.get(player1)
    elif not optimalLineup.get('WR2'):
        optimalLineup.update({positionDict.get(player1): player1})
        remainingSalary -= draftKingsSalaries.get(player1)
    elif not optimalLineup.get('WR3'):
        optimalLineup.update({positionDict.get(player1): player1})
        remainingSalary -= draftKingsSalaries.get(player1)
    elif not optimalLineup.get('FLEX'):
        optimalLineup.update({positionDict.get(player1): player1})
        remainingSalary -= draftKingsSalaries.get(player1)
elif positionDict.get(player1) == 'TE':
    if not optimalLineup.get('TE'):
        optimalLineup.update({positionDict.get(player1): player1})
        remainingSalary -= draftKingsSalaries.get(player1)
    elif not optimalLineup.get('FLEX'):
        optimalLineup.update({positionDict.get(player1): player1})
        remainingSalary -= draftKingsSalaries.get(player1)
else:
    if not optimalLineup.get(positionDict.get(player1)):
        optimalLineup.update({positionDict.get(player1): player1})
        remainingSalary -= draftKingsSalaries.get(player1)

print(optimalLineup)
print(remainingSalary)
print(takenPositions)

# DFS max salaries: DK = $50k, FD = $60k

# make sure final code gets current week and sets "weeks" to that number
