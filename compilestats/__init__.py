import statistics as s
from getstats import positionDict, playerPointDicts, playerPassAttemptsDicts, playerRushDicts, playerTarDicts, \
    playerRecDicts, playersAndOpps
from pointsallowed import pointsAllowedDictList


# define functions that find max, min, avg, and std of list, ignoring weird entries
def get_max(your_list):
    new_list = []
    for item in your_list:
        if item != '--' and item is not None:
            new_list.append(item)
    new_list = map(float, new_list)
    try:
        return max(new_list)
    except ValueError:
        return 0


def get_min(your_list):
    new_list = []
    for item in your_list:
        if item != '--' and item is not None:
            new_list.append(item)
    new_list = map(float, new_list)
    try:
        return min(new_list)
    except ValueError:
        return 0


def get_avg(your_list):
    new_list = []
    for item in your_list:
        if item != '--' and item is not None:
            new_list.append(item)
    new_list = map(float, new_list)
    try:
        return s.mean(new_list)
    except ValueError:
        return 0


def get_std(your_list):
    new_list = []
    for item in your_list:
        if item != '--' and item is not None:
            new_list.append(item)
    new_list = map(float, new_list)
    try:
        return round(s.stdev(new_list), 1)
    except ValueError:
        return 0


# define lists and dicts to be populated later
playerMasterPointDict = {}
playerMasterRushDict = {}
playerMasterRecDict = {}
playerMasterTarDict = {}

# create dictionaries that organizes players with their weekly stats
for player in positionDict.keys():
    # only add stats if the player played in the game
    for i in range(len(playerPointDicts)):
        playerRushes = []
        playerRecs = []
        playerTars = []
        playerPoints = []
        if positionDict.get(player) == 'QB' and playerPassAttemptsDicts[i].get(player) == '0/0':
            continue
        elif positionDict.get(player) == 'RB' and playerRushDicts[i].get(player) == 0:
            continue
        elif positionDict.get(player) == 'WR' and playerTarDicts[i].get(player) == 0:
            continue
        elif positionDict.get(player) == 'TE' and playerTarDicts[i].get(player) == 0:
            continue
        else:
            playerRushes.append(playerRushDicts[i].get(player))
            playerMasterRushDict.update({player: playerRushes})

            playerRecs.append(playerRecDicts[i].get(player))
            playerMasterRecDict.update({player: playerRecs})

            playerTars.append(playerTarDicts[i].get(player))
            playerMasterTarDict.update({player: playerTars})

            playerPoints.append(playerPointDicts[i].get(player))
            playerMasterPointDict.update({player: playerPoints})

# create master lists to be populated
playerMaxPointsDict = {}
playerMinPointsDict = {}
playerAvgPointsDict = {}
playerStdPointsDict = {}

for player, weeklyPoints in playerMasterPointDict.items():
    playerMaxPointsDict.update({player: get_max(weeklyPoints)})
    playerMinPointsDict.update({player: get_min(weeklyPoints)})
    playerAvgPointsDict.update({player: round(get_avg(weeklyPoints), 1)})
    playerStdPointsDict.update({player: get_std(weeklyPoints)})

# get average player usage
playerMasterUsageDict = {}
for player in playerMasterRushDict.keys():
    playerUsageList = []
    playerUsage = get_avg(playerMasterRushDict.get(player)) + get_avg(playerMasterRecDict.get(player)) + get_avg(
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
                0.025 * std) + (0.025 * oppPointsAllowed)
        overallScore = float(round(overallScoreFloat, 2))
        overallPlayerScoresDict.update({player: overallScore})

sortedScores = sorted(overallPlayerScoresDict, key=overallPlayerScoresDict.__getitem__, reverse=True)
