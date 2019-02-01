from itertools import combinations as comb
from compilestats import *
from getsalaries import *
from emailresults import send_email


def get_total(players, data):
    data_list = [data.get(dude) for dude in players]
    return sum(data_list)


def optimize(score_dict, salary_dict):
    rb_count = [3, 2, 2]
    wr_count = [3, 4, 3]
    te_count = [1, 1, 2]
    best_lineup = []
    max_points = 0
    for n in range(3):
        max_wr_points = max([get_total(wrs, score_dict) for wrs in list(comb(playerWRList, wr_count[n]))])
        min_wr_salary = min([get_total(wrs, salary_dict) for wrs in list(comb(playerWRList, wr_count[n]))])
        max_te_points = max([get_total(tes, score_dict) for tes in list(comb(playerTEList, te_count[n]))])
        min_te_salary = min([get_total(tes, salary_dict) for tes in list(comb(playerTEList, te_count[n]))])
        max_dst_points = max([score_dict.get(dst) for dst in playerDSTList])
        min_dst_salary = min([salary_dict.get(dst) for dst in playerDSTList])
        flex = ''
        for qb in playerQBList:
            qb_points = score_dict.get(qb)
            qb_salary = salary_dict.get(qb)
            for rbs in comb(playerRBList, rb_count[n]):
                rb_points = get_total(rbs, score_dict)
                rb_salary = get_total(rbs, salary_dict)
                potential_max_points = qb_points + rb_points + max_wr_points + max_te_points + max_dst_points
                potential_max_salary = qb_salary + rb_salary + min_wr_salary + min_te_salary + min_dst_salary
                if potential_max_points > max_points and potential_max_salary <= salaryCap:
                    for wrs in comb(playerWRList, wr_count[n]):
                        wr_points = get_total(wrs, score_dict)
                        wr_salary = get_total(wrs, salary_dict)
                        potential_max_points = qb_points + rb_points + wr_points + max_te_points + max_dst_points
                        potential_max_salary = qb_salary + rb_salary + wr_salary + min_te_salary + min_dst_salary
                        if potential_max_points > max_points and potential_max_salary <= salaryCap:
                            for tes in comb(playerTEList, te_count[n]):
                                te_points = get_total(tes, score_dict)
                                te_salary = get_total(tes, salary_dict)
                                potential_max_points = qb_points + rb_points + wr_points + te_points + max_dst_points
                                potential_max_salary = qb_salary + rb_salary + wr_salary + te_salary + min_dst_salary
                                if potential_max_points > max_points and potential_max_salary <= salaryCap:
                                    for dst in playerDSTList:
                                        dst_points = score_dict.get(dst)
                                        dst_salary = salary_dict.get(dst)
                                        point_total = qb_points + rb_points + wr_points + te_points + dst_points
                                        total_salary = qb_salary + rb_salary + wr_salary + te_salary + dst_salary
                                        if point_total > max_points and total_salary <= salaryCap:
                                            if rbs[2]:
                                                flex = rbs[2]
                                            elif wrs[3]:
                                                flex = wrs[3]
                                            elif tes[1]:
                                                flex = tes[1]
                                            best_lineup = [qb, rbs[0], rbs[1], wrs[0], wrs[1], wrs[2], tes[0], flex,
                                                           dst]
                                            max_points = point_total

    return best_lineup


lineupResults = ''
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

        bestLineup = optimize(score_dict=overallPlayerScoresDict, salary_dict=playerSalaries)

        # print output!
        positionOrder = ['QB', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE', 'FLEX', 'D/ST']
        rb1Score = overallPlayerScoresDict.get(bestLineup[1])
        rb2Score = overallPlayerScoresDict.get(bestLineup[2])
        wr1Score = overallPlayerScoresDict.get(bestLineup[3])
        wr2Score = overallPlayerScoresDict.get(bestLineup[4])
        wr3Score = overallPlayerScoresDict.get(bestLineup[5])
        teScore = overallPlayerScoresDict.get(bestLineup[6])
        flexScore = overallPlayerScoresDict.get(bestLineup[7])

        optimalLineup = dict(zip(positionOrder, bestLineup))
        playerLineup = ''
        if siteSalaries.index(playerSalaries) == 0:
            playerLineup += 'Draftkings Lineup:' + '\n'
        else:
            playerLineup += 'Fanduel Lineup:' + '\n'
        for position, player in optimalLineup.items():
            playerLineup += str(position) + ': ' + str(player) + ' - $' + str(playerSalaries.get(player)) + '\n'
        projPoints = get_total(bestLineup, overallPlayerScoresDict)
        playerLineup += 'Total projected points: ' + str(round(projPoints, 2)) + '\n'
        playerLineup += 'Remaining salary: ' + str(salaryCap - get_total(bestLineup, playerSalaries)) + '\n'
        playerLineup += '\n'

        lineupResults += playerLineup

    else:
        print('No salary data available.')

if lineupResults:
    send_email(from_addr='fantasyoptimizationresults@gmail.com', to_addr_list=['carlyfox18@gmail.com'],
               cc_addr_list=[''], subject='Your Optimized Week ' + str(weeks + 1) + ' DFS Lineups!',
               message=lineupResults, login='fantasyoptimizationresults', password='optimize123')

    print('Lineups complete and results emailed!')

# make sure final code gets current week and sets "weeks" to that number
# put an "if projected points from ESPN = 0, exclude this player"
