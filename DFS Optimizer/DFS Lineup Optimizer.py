from itertools import combinations
from compilestats import *
from getsalaries import *


def get_total(players, data):
    data_list = []
    for dude in players:
        data_list.append(data.get(dude))
    return sum(data_list)


def valid_lineup(lineup, cap):
    lineup_positions = []
    for person in lineup:
        lineup_positions.append(positionDict.get(person))
    if lineup_positions.count('QB') == lineup_positions.count('D/ST') == 1 <= lineup_positions.count(
            'TE') <= 2 <= lineup_positions.count('RB') <= 3 <= lineup_positions.count(
            'WR') <= 4 and get_total(lineup, playerSalaries) <= cap:
        return True
    else:
        return False


totalPlayerScores = get_total(sortedScores, overallPlayerScoresDict)
scoreThreshold = 0.25*totalPlayerScores
playerLineupList = []
for player, score in sortedPlayersAndScores.items():
    if player in playerSalaries.keys() and score > scoreThreshold:
        playerLineupList.append(player)

if playerSalaries:
    print('Generating possible lineups...')
    # create optimal DFS lineup!
    # maximize total projected points with constraint of salary cap
    # set salary cap to 50k for Draftkings and 60k for Fanduel
    salaryCap = 60000
    validLineups = [lineup for lineup in combinations(playerLineupList, 9)
                    if valid_lineup(lineup, salaryCap)]

    print('Maximizing projected points...')
    bestLineup = []
    maxPoints = 0
    for lineup in validLineups:
        pointTotal = get_total(lineup, overallPlayerScoresDict)
        if pointTotal > maxPoints:
            bestLineup = lineup
            maxPoints = pointTotal

    optimalLineup = {}
    for player in bestLineup:
        optimalLineup.update({player: positionDict.get(player)})

    # print output!
    for player, position in optimalLineup.items():
        if position == 'WR' and 'WR2' in optimalLineup.values():
            optimalLineup.update({player: 'WR3'})
        elif position in {'RB', 'WR'} and str(position) + '1' in optimalLineup.values():
            optimalLineup.update({player: str(position) + '2'})
        elif position in {'RB', 'WR'}:
            optimalLineup.update({player: str(position) + '1'})
        elif position in {'RB', 'WR'} and all(
                item in optimalLineup.values() for item in {'RB1', 'RB2', 'WR1', 'WR2', 'WR3'}):
            optimalLineup.update({player: 'FLEX'})
        elif position == 'TE' and 'FLEX' not in optimalLineup.values():
            optimalLineup.update({player: 'FLEX'})

    positionOrder = ['QB', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE', 'FLEX', 'D/ST']
    for pos in positionOrder:
        player = None
        for guy, position in optimalLineup.items():
            if pos == position:
                player = guy
                break
        print(str(pos) + ': ' + str(player) + ' - $' + str(playerSalaries.get(player)))
    print('Total projected points: ' + str(round(maxPoints, 2)))
    print('Remaining salary: ' + str(salaryCap - get_total(bestLineup, playerSalaries)))

    # make sure final code gets current week and sets "weeks" to that number
    # put an "if projected points from ESPN = 0, exclude this player"
else:
    print('No salary data available.')
