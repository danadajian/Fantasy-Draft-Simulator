import requests
from bs4 import BeautifulSoup

playerPointDicts = []
playerPassAttemptsDicts = []
playerRushDicts = []
playerRecDicts = []
playerTarDicts = []
positionDict = {}
playerTeamDict = {}
playerOppList = []
finalPlayerList = []
# define dictionary containing useful info about all 32 teams
teamAbbrevDict = {'Ari': 'Cardinals', 'Atl': 'Falcons', 'Bal': 'Ravens', 'Buf': 'Bills', 'Car': 'Panthers',
                  'Chi': 'Bears', 'Cin': 'Bengals', 'Cle': 'Browns', 'Dal': 'Cowboys', 'Den': 'Broncos', 'Det': 'Lions',
                  'GB': 'Packers', 'Hou': 'Texans', 'Ind': 'Colts', 'Jax': 'Jaguars', 'KC': 'Chiefs', 'LAC': 'Chargers',
                  'LAR': 'Rams', 'Mia': 'Dolphins', 'Min': 'Vikings', 'NE': 'Patriots', 'NO': 'Saints', 'NYG': 'Giants',
                  'NYJ': 'Jets', 'Oak': 'Raiders', 'Phi': 'Eagles', 'Pit': 'Steelers', 'SF': '49ers', 'Sea': 'Seahawks',
                  'TB': 'Buccaneers', 'Ten': 'Titans', 'Wsh': 'Redskins'}


# defines function that finds all string indices of a substring
def find_all(string, substring, indices):
    x = -1
    while True:
        x = string.find(substring, x + 1)
        if x == -1:
            break
        indices.append(x)


# defines function that finds the nth index of a substring
def find_stat(haystack, needle, n):
    stat_index = haystack.find(needle)
    i = 1
    while i < n:
        stat_index = haystack.find(needle, stat_index + len(needle))
        i += 1
    lower = stat_index + len(needle)
    upper = haystack.find('<', lower)
    return haystack[lower: upper]


# sets first n weeks of data to be considered
playerCount = 0
weeks = 14
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
        find_all(playerText, 'teamid="-2147483648">', playerIndexList)

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
                    passAttempts = find_stat(statsString, '</td><td class="playertableStat ">', 1)
                    rushes = find_stat(statsString, '</td><td class="playertableStat ">', 5)
                    recs = find_stat(statsString, '</td><td class="playertableStat ">', 8)
                    tars = find_stat(statsString, '</td><td class="playertableStat ">', 11)
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
