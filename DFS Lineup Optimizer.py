from itertools import combinations
from compilestats import *
from getsalaries import *


def get_total(players, data):
    data_list = [data.get(dude) for dude in players]
    return sum(data_list)


for playerSalaries in siteSalaries:
    if playerSalaries:
        pointsPercentile = round(0.50 * len(sortedScores))
        pointsThreshold = overallPlayerScoresDict.get(sortedScores[pointsPercentile])
        playerLineupList = []
        for player, score in overallPlayerScoresDict.items():
            if player in playerSalaries.keys() and score > pointsThreshold:
                playerLineupList.append(player)

        playerQBList = [player for player in playerLineupList if positionDict.get(player) == 'QB']
        playerRBList = [player for player in playerLineupList if positionDict.get(player) == 'RB']
        playerWRList = [player for player in playerLineupList if positionDict.get(player) == 'WR']
        playerTEList = [player for player in playerLineupList if positionDict.get(player) == 'TE']
        playerFLEXList = playerRBList + playerWRList + playerTEList
        playerDSTList = [player for player in playerLineupList if positionDict.get(player) == 'D/ST']

        # create optimal DFS lineup!
        # maximize total projected points with constraint of salary cap
        # set salary cap to 50k for Draftkings and 60k for Fanduel
        if siteSalaries.index(playerSalaries) == 0:
            print('Determining optimal Draftkings lineup...')
            salaryCap = 50000
        else:
            print('Determining optimal FanDuel lineup...')
            salaryCap = 60000
        bestLineup = []
        maxPoints = 0
        qbSalary = 0
        rbSalary = 0
        wrSalary = 0
        teSalary = 0
        dstSalary = 0
        maxRBPoints = max([get_total(rbs, overallPlayerScoresDict) for rbs in list(combinations(playerRBList, 3))])
        minRBSalary = min([get_total(rbs, playerSalaries) for rbs in list(combinations(playerRBList, 3))])
        maxWRPoints = max([get_total(wrs, overallPlayerScoresDict) for wrs in list(combinations(playerWRList, 3))])
        minWRSalary = min([get_total(wrs, playerSalaries) for wrs in list(combinations(playerWRList, 3))])
        maxTEPoints = max([overallPlayerScoresDict.get(te) for te in playerTEList])
        minTESalary = min([playerSalaries.get(te) for te in playerTEList])
        maxDSTPoints = max([overallPlayerScoresDict.get(dst) for dst in playerDSTList])
        minDSTSalary = min([playerSalaries.get(dst) for dst in playerDSTList])
        for qb in playerQBList:
            qbPoints = overallPlayerScoresDict.get(qb)
            qbSalary = playerSalaries.get(qb)
            for rbs in combinations(playerRBList, 3):
                rbPoints = get_total(rbs, overallPlayerScoresDict)
                rbSalary = get_total(rbs, playerSalaries)
                if qbPoints + rbPoints + maxWRPoints + maxTEPoints + maxDSTPoints > maxPoints and qbSalary + rbSalary + minWRSalary + minTESalary + minDSTSalary <= salaryCap:
                    for wrs in combinations(playerWRList, 3):
                        wrPoints = get_total(wrs, overallPlayerScoresDict)
                        wrSalary = get_total(wrs, playerSalaries)
                        if qbPoints + rbPoints + wrPoints + maxTEPoints + maxDSTPoints > maxPoints and qbSalary + rbSalary + wrSalary + minTESalary + minDSTSalary <= salaryCap:
                            for te in playerTEList:
                                tePoints = overallPlayerScoresDict.get(te)
                                teSalary = playerSalaries.get(te)
                                if qbPoints + rbPoints + wrPoints + tePoints + maxDSTPoints > maxPoints and qbSalary + rbSalary + wrSalary + teSalary + minDSTSalary <= salaryCap:
                                    for dst in playerDSTList:
                                        dstPoints = overallPlayerScoresDict.get(dst)
                                        dstSalary = playerSalaries.get(dst)
                                        pointTotal = qbPoints + rbPoints + wrPoints + tePoints + dstPoints
                                        totalSalary = qbSalary + rbSalary + wrSalary + teSalary + dstSalary
                                        if pointTotal > maxPoints and totalSalary <= salaryCap:
                                            bestLineup = [qb, rbs[0], rbs[1], wrs[0], wrs[1], wrs[2], te, rbs[2], dst]
                                            maxPoints = pointTotal

        for qb in playerQBList:
            qbPoints = overallPlayerScoresDict.get(qb)
            qbSalary = playerSalaries.get(qb)
            for rbs in combinations(playerRBList, 2):
                rbPoints = get_total(rbs, overallPlayerScoresDict)
                rbSalary = get_total(rbs, playerSalaries)
                if qbPoints + rbPoints + maxWRPoints + maxTEPoints + maxDSTPoints > maxPoints and qbSalary + rbSalary + minWRSalary + minTESalary + minDSTSalary <= salaryCap:
                    for wrs in combinations(playerWRList, 4):
                        wrPoints = get_total(wrs, overallPlayerScoresDict)
                        wrSalary = get_total(wrs, playerSalaries)
                        if qbPoints + rbPoints + wrPoints + maxTEPoints + maxDSTPoints > maxPoints and qbSalary + rbSalary + wrSalary + minTESalary + minDSTSalary <= salaryCap:
                            for te in playerTEList:
                                tePoints = overallPlayerScoresDict.get(te)
                                teSalary = playerSalaries.get(te)
                                if qbPoints + rbPoints + wrPoints + tePoints + maxDSTPoints > maxPoints and qbSalary + rbSalary + wrSalary + teSalary + minDSTSalary <= salaryCap:
                                    for dst in playerDSTList:
                                        dstPoints = overallPlayerScoresDict.get(dst)
                                        dstSalary = playerSalaries.get(dst)
                                        pointTotal = qbPoints + rbPoints + wrPoints + tePoints + dstPoints
                                        totalSalary = qbSalary + rbSalary + wrSalary + teSalary + dstSalary
                                        if pointTotal > maxPoints and totalSalary <= salaryCap:
                                            bestLineup = [qb, rbs[0], rbs[1], wrs[0], wrs[1], wrs[2], te, wrs[3], dst]
                                            maxPoints = pointTotal

        minTESalary = min([get_total(tes, playerSalaries) for tes in list(combinations(playerTEList, 2))])
        for qb in playerQBList:
            qbPoints = overallPlayerScoresDict.get(qb)
            qbSalary = playerSalaries.get(qb)
            for rbs in combinations(playerRBList, 3):
                rbPoints = get_total(rbs, overallPlayerScoresDict)
                rbSalary = get_total(rbs, playerSalaries)
                if qbPoints + rbPoints + maxWRPoints + maxTEPoints + maxDSTPoints > maxPoints and qbSalary + rbSalary + minWRSalary + minTESalary + minDSTSalary <= salaryCap:
                    for wrs in combinations(playerWRList, 3):
                        wrPoints = get_total(wrs, overallPlayerScoresDict)
                        wrSalary = get_total(wrs, playerSalaries)
                        if qbPoints + rbPoints + wrPoints + maxTEPoints + maxDSTPoints > maxPoints and qbSalary + rbSalary + wrSalary + minTESalary + minDSTSalary <= salaryCap:
                            for tes in combinations(playerTEList, 2):
                                tePoints = get_total(tes, overallPlayerScoresDict)
                                teSalary = get_total(tes, playerSalaries)
                                if qbPoints + rbPoints + wrPoints + tePoints + maxDSTPoints > maxPoints and qbSalary + rbSalary + wrSalary + teSalary + minDSTSalary <= salaryCap:
                                    for dst in playerDSTList:
                                        dstPoints = overallPlayerScoresDict.get(dst)
                                        dstSalary = playerSalaries.get(dst)
                                        pointTotal = qbPoints + rbPoints + wrPoints + tePoints + dstPoints
                                        totalSalary = qbSalary + rbSalary + wrSalary + teSalary + dstSalary
                                        if pointTotal > maxPoints and totalSalary <= salaryCap:
                                            bestLineup = [qb, rbs[0], rbs[1], wrs[0], wrs[1], wrs[2], tes[0], tes[1],
                                                          dst]
                                            maxPoints = pointTotal

        # print output!
        positionOrder = ['QB', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE', 'FLEX', 'D/ST']
        optimalLineup = dict(zip(positionOrder, bestLineup))
        for position, player in optimalLineup.items():
            print(str(position) + ': ' + str(player) + ' - $' + str(playerSalaries.get(player)))
        print('Total projected points: ' + str(round(maxPoints, 2)))
        print('Remaining salary: ' + str(salaryCap - get_total(bestLineup, playerSalaries)))
        print('\n')

        # make sure final code gets current week and sets "weeks" to that number
        # put an "if projected points from ESPN = 0, exclude this player"
    else:
        print('No salary data available.')
