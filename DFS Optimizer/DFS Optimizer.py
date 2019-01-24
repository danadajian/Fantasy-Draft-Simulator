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
weeks = 10
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
    while playerCount <= 250:
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

        # put players and opponents into master dictionary
        playersAndOpps = dict(zip(playerList, playerOppList))

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

if siteSalaries[0]:
    # create optimal DFS lineup!
    # optimize lineup based on maximizing marginal projected point increase per salary increase
    # start by selecting the highest overall proj pts per salary, and then anchor to that player
    # to minimize proj pts decrease per salary decrease
    optimalLineup = {}

    # sort players with scores in descending order
    playerScores = {}
    sortedScores = sorted(overallPlayerScoresDict, key=overallPlayerScoresDict.__getitem__, reverse=True)
    for player in sortedScores:
        playerScores.update({player: overallPlayerScoresDict.get(player)})
    print(playerScores)

    # set salary dict to be DraftKings for now
    draftKingsSalaries = siteSalaries[0]

    # sort players with score per salary in descending order
    playerPointsPerSalary = {}
    for player in sortedScores:
        if player in draftKingsSalaries.keys():
            playerScore = playerScores.get(player)
            playerSalary = draftKingsSalaries.get(player)
            playerPointsPerSalary.update({player: playerScore / playerSalary})
    sortedPointsPerSalary = sorted(playerPointsPerSalary, key=playerPointsPerSalary.__getitem__, reverse=True)

    # draft first player with highest pts per salary ratio
    playerPicked = sortedPointsPerSalary[0]

    # set salary cap to 50k (Fanduel will be 60k)
    remainingSalary = 50000
    takenPositions = []

    # loop 9 times to get all 9 players in the lineup
    for i in range(9):
        if i > 0:
            # determine player pool to select remaining players from
            playerPool = []
            for player in sortedPointsPerSalary:
                if player not in optimalLineup.values() and positionDict.get(player) not in takenPositions:
                    playerPool.append(player)

            # calculate each player's marginal salary decrease per projected pts decrease from the last player picked
            marginalPointsPerDollar = {}
            for player in playerPool:
                marginalPoints = playerScores.get(playerPicked) - playerScores.get(player)
                marginalSalary = draftKingsSalaries.get(playerPicked) - draftKingsSalaries.get(player)
                if marginalSalary == 0:
                    marginalSalary = 1
                marginalPointsPerSalary = marginalPoints / marginalSalary
                if marginalPointsPerSalary > 0:
                    marginalPointsPerDollar.update({player: marginalPointsPerSalary})

            # sort each position by descending overall score per salary dollar
            sortedMarginalPoints = sorted(marginalPointsPerDollar, key=marginalPointsPerDollar.__getitem__)
            playerPicked = sortedMarginalPoints[0]

        # logic for putting players in the lineup and "paying" for them each time
        if positionDict.get(playerPicked) == 'RB':
            if not optimalLineup.get('RB1'):
                optimalLineup.update({'RB1': playerPicked})
                remainingSalary -= draftKingsSalaries.get(playerPicked)
            elif not optimalLineup.get('RB2'):
                optimalLineup.update({'RB2': playerPicked})
                remainingSalary -= draftKingsSalaries.get(playerPicked)
            elif not optimalLineup.get('FLEX'):
                optimalLineup.update({'FLEX': playerPicked})
                remainingSalary -= draftKingsSalaries.get(playerPicked)
        elif positionDict.get(playerPicked) == 'WR':
            if not optimalLineup.get('WR1'):
                optimalLineup.update({'WR1': playerPicked})
                remainingSalary -= draftKingsSalaries.get(playerPicked)
            elif not optimalLineup.get('WR2'):
                optimalLineup.update({'WR2': playerPicked})
                remainingSalary -= draftKingsSalaries.get(playerPicked)
            elif not optimalLineup.get('WR3'):
                optimalLineup.update({'WR3': playerPicked})
                remainingSalary -= draftKingsSalaries.get(playerPicked)
            elif not optimalLineup.get('FLEX'):
                optimalLineup.update({'FLEX': playerPicked})
                remainingSalary -= draftKingsSalaries.get(playerPicked)
        elif positionDict.get(playerPicked) == 'TE':
            if not optimalLineup.get('TE'):
                optimalLineup.update({'TE': playerPicked})
                remainingSalary -= draftKingsSalaries.get(playerPicked)
            elif not optimalLineup.get('FLEX'):
                optimalLineup.update({'FLEX': playerPicked})
                remainingSalary -= draftKingsSalaries.get(playerPicked)
        else:
            if not optimalLineup.get(positionDict.get(playerPicked)):
                optimalLineup.update({positionDict.get(playerPicked): playerPicked})
                remainingSalary -= draftKingsSalaries.get(playerPicked)

        # implement a check for when position slots are full
        if 'QB' in optimalLineup.keys() and 'QB' not in takenPositions:
            takenPositions.append('QB')
        if 'RB2' in optimalLineup.keys() and 'FLEX' in optimalLineup.keys() and 'RB' not in takenPositions:
            takenPositions.append('RB')
        if 'WR3' in optimalLineup.keys() and 'FLEX' in optimalLineup.keys() and 'WR' not in takenPositions:
            takenPositions.append('WR')
        if 'TE' in optimalLineup.keys() and 'FLEX' in optimalLineup.keys() and 'TE' not in takenPositions:
            takenPositions.append('TE')
        if 'D/ST' in optimalLineup.keys() and 'D/ST' not in takenPositions:
            takenPositions.append('D/ST')

    # print output!
    positionOrder = ['QB', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE', 'FLEX', 'D/ST']
    for pos in positionOrder:
        print(optimalLineup.get(pos))
    print('Remaining salary: ' + str(remainingSalary))

    # make sure final code gets current week and sets "weeks" to that number
    # put an "if projected points from ESPN = 0, exclude this player"
else:
    print('No salary data available.')
