""" Fantasy Draft Simulator """

import random

userDraftPicks = []

# ranked list of players that you want
userdict = {'Todd Gurley': 'RB', 'Ezekiel Elliott': 'RB', 'David Johnson': 'RB', 'Antonio Brown': 'WR',
            'Saquon Barkley': 'RB', 'Odell Beckham Jr.': 'WR', 'Dalvin Cook': 'RB', 'Leonard Fournette': 'RB',
            'LeSean McCoy': 'RB', 'Rob Gronkowski': 'TE', 'T.Y. Hilton': 'WR', 'Michael Thomas': 'WR',
            'Derrius Guice': 'RB', 'Derrick Henry': 'RB', 'Travis Kelce': 'TE', 'Zach Ertz': 'TE',
            'Josh Gordon': 'WR', 'Deshaun Watson': 'QB', 'Chris Hogan': 'WR', 'Joe Mixon': 'RB',
            'Sony Michel': 'RB', 'Alex Collins': 'RB', 'Demaryius Thomas': 'WR', 'Amari Cooper': 'WR',
            'Kenyan Drake': 'RB', 'Ronald Jones': 'RB', 'Golden Tate': 'WR', 'Corey Davis': 'WR'}

# ranked player list that everyone drafts from
top200dict = {"Le'Veon Bell": 'RB', 'Todd Gurley': 'RB', 'David Johnson': 'RB', 'Antonio Brown': 'WR',
              'Ezekiel Elliott': 'RB', 'DeAndre Hopkins': 'WR', 'Saquon Barkley': 'RB', 'Alvin Kamara': 'RB',
              'Julio Jones': 'WR', 'Odell Beckham Jr.': 'WR', 'Keenan Allen': 'WR', 'Kareem Hunt': 'RB',
              'Dalvin Cook': 'RB', 'Michael Thomas': 'WR', 'Melvin Gordon': 'RB', 'Leonard Fournette': 'RB',
              'A.J. Green': 'WR', 'LeSean McCoy': 'RB', 'Christian McCaffrey': 'RB', 'Devonta Freeman': 'RB',
              'Davante Adams': 'WR', 'Rob Gronkowski': 'TE', 'Mike Evans': 'WR', 'Adam Thielen': 'WR',
              'Larry Fitzgerald': 'WR', 'Tyreek Hill': 'WR', 'T.Y. Hilton': 'WR', 'Doug Baldwin': 'WR',
              'Travis Kelce': 'TE', 'Zach Ertz': 'TE', 'Demaryius Thomas': 'WR', 'Stefon Diggs': 'WR',
              'Allen Robinson': 'WR', 'Golden Tate': 'WR', 'Josh Gordon': 'WR', 'Jerick McKinnon': 'RB',
              'Joe Mixon': 'RB', 'Jordan Howard': 'RB', 'Alshon Jeffery': 'WR', 'JuJu Smith-Schuster': 'WR',
              'Amari Cooper': 'WR', 'Jarvis Landry': 'WR', 'Rashaad Penny': 'RB', 'Kenyan Drake': 'RB',
              'Derrius Guice': 'RB', 'Jay Ajayi': 'RB', 'Sony Michel': 'RB', 'Alex Collins': 'RB',
              'Royce Freeman': 'RB', 'Ronald Jones': 'RB', 'Marvin Jones Jr.': 'WR', 'Robert Woods': 'WR',
              'Emmanuel Sanders': 'WR', 'Pierre Garcon': 'WR', 'Marshawn Lynch': 'RB', 'Mark Ingram': 'RB',
              'Derrick Henry': 'RB', 'Dion Lewis': 'RB', 'Duke Johnson Jr.': 'RB', 'Michael Crabtree': 'WR',
              'Chris Hogan': 'WR', 'Brandin Cooks': 'WR', 'Corey Davis': 'WR', 'Aaron Rodgers': 'QB',
              'Tom Brady': 'QB', 'Sammy Watkins': 'WR', 'Cooper Kupp': 'WR', 'Devin Funchess': 'WR',
              'DeVante Parker': 'WR', 'Randall Cobb': 'WR', 'Will Fuller V': 'WR', 'Julian Edelman': 'WR',
              'Greg Olsen': 'TE', 'Delanie Walker': 'TE', 'Evan Engram': 'TE', 'Lamar Miller': 'RB',
              'Kelvin Benjamin': 'WR', 'Jamison Crowder': 'WR', 'Kerryon Johnson': 'RB', 'Cam Newton': 'QB',
              'Carson Wentz': 'QB', 'Russell Wilson': 'QB', 'Deshaun Watson': 'QB'}


def fantasy_draft():
    # making player lists of each position
    userList = [key for key in userdict.keys()]
    top200List = [key for key in top200dict.keys()]

    # dictionary and list creation
    userQBList = []
    userRBList = []
    userWRList = []
    userTEList = []
    draftQBList = []
    draftRBList = []
    draftWRList = []
    draftTEList = []
    roundResults = {}
    userTeam = []
    Team2 = []
    Team3 = []
    Team4 = []
    Team5 = []
    Team6 = []
    Team7 = []
    Team8 = []
    team_dict = {'Team 2': Team2, 'Team 3': Team3, 'Team 4': Team4, 'Team 5': Team5,
                 'Team 6': Team6, 'Team 7': Team7, 'Team 8': Team8}

    # making player lists by position
    for player, position in userdict.items():
        if position == 'QB':
            userQBList.append(player)
        elif position == 'RB':
            userRBList.append(player)
        elif position == 'WR':
            userWRList.append(player)
        elif position == 'TE':
            userTEList.append(player)

    for player, position in top200dict.items():
        if position == 'QB':
            draftQBList.append(player)
        elif position == 'RB':
            draftRBList.append(player)
        elif position == 'WR':
            draftWRList.append(player)
        elif position == 'TE':
            draftTEList.append(player)

    # functions
    def position_ignore(list, position):
        temp = []
        if all(top200dict.get(player) == position for player in list):
            temp = list
        else:
            for player in list:
                if top200dict.get(player) != position:
                    temp.append(player)
        return temp

    def position_count(list1, list2):
        return len(set(list1) & set(list2))

    # variables
    round = 0
    threshold = 3

    # draft starts here
    print('The draft is live!')

    # randomizes the draft order
    draftOrder = ['user', 'Team 2', 'Team 3', 'Team 4', 'Team 5', 'Team 6', 'Team 7', 'Team 8']
    random.shuffle(draftOrder)
    print(draftOrder)
    print()

    while round <= 6:  # we only want 7 rounds
        for team in draftOrder:
            if round != 0:
                if team == 'user':  # this is your team's pick logic
                    if position_count(userTeam, userRBList) >= 2 and position_count(userTeam, userWRList) >= 2:
                        pick = (userList[:1])[0]  # pick the player at the top of your list
                    elif position_count(userTeam, userWRList) < 2 <= position_count(userTeam, userRBList):
                        pick = (position_ignore(userList, 'RB')[:1])[0]  # limiting each team to 3 RB
                    elif position_count(userTeam, userRBList) < 2 <= position_count(userTeam, userWRList):
                        pick = (position_ignore(userList, 'WR')[:1])[0]  # limiting each team to 3 WR
                    else:
                        pick = (userList[:1])[0]  # pick the player at the top of your list
                    roundResults.update({team: pick})  # add the pick to the round results dictionary
                    userList.remove(pick)  # remove the player from your draft list
                    top200List.remove(pick)  # remove the player from the master list
                else:  # this is the AI's pick logic
                    if len(top200List) <= threshold:  # case when there are very few players left to choose from
                        if position_count(team_dict.get(team), draftRBList) >= 2 and position_count(team_dict.get(team),
                                                                                                    draftWRList) >= 2:
                            pick = random.sample(top200List, 1)  # pick any random player from the list
                        elif position_count(team_dict.get(team), draftWRList) < 2 <= position_count(team_dict.get(team),
                                                                                                    draftRBList):
                            pick = random.sample(position_ignore(top200List, 'RB'), 1)
                        elif position_count(team_dict.get(team), draftRBList) < 2 <= position_count(team_dict.get(team),
                                                                                                    draftWRList):
                            pick = random.sample(position_ignore(top200List, 'WR'), 1)
                        else:
                            pick = random.sample(top200List, 1)  # pick any random player from the list
                        roundResults.update({team: pick})
                        if pick in userList:
                            userList.remove(pick)
                        top200List.remove(pick)
                    else:
                        if position_count(team_dict.get(team), draftRBList) >= 2 and position_count(team_dict.get(team),
                                                                                                    draftWRList) >= 2:
                            pick = random.sample(top200List[:threshold], 1)[0]
                        elif position_count(team_dict.get(team), draftWRList) < 2 <= position_count(team_dict.get(team),
                                                                                                    draftRBList):
                            pick = random.sample(position_ignore(top200List, 'RB')[:threshold], 1)[0]
                        elif position_count(team_dict.get(team), draftRBList) < 2 <= position_count(team_dict.get(team),
                                                                                                    draftWRList):
                            pick = random.sample(position_ignore(top200List, 'WR')[:threshold], 1)[0]
                        else:  # pick a random player from the top "threshold" players
                            pick = random.sample(top200List[:threshold], 1)[0]
                        roundResults.update({team: pick})
                        if pick in userList:
                            userList.remove(pick)
                        top200List.remove(pick)
            else:  # can't check for a team having too many of one position in the first round
                if team == 'user':
                    userPick = (userList[:1])[0]
                    roundResults.update({team: userPick})
                    userList.remove(userPick)
                    top200List.remove(userPick)
                else:
                    draftPick = random.sample(top200List[:threshold], 1)[0]
                    roundResults.update({team: draftPick})
                    if draftPick in userList:
                        userList.remove(draftPick)
                    top200List.remove(draftPick)
        userTeam.append(roundResults.get('user'))  # adds the player you drafted to your team list
        Team2.append(roundResults.get('Team 2'))  # does the same for all other teams
        Team3.append(roundResults.get('Team 3'))
        Team4.append(roundResults.get('Team 4'))
        Team5.append(roundResults.get('Team 5'))
        Team6.append(roundResults.get('Team 6'))
        Team7.append(roundResults.get('Team 7'))
        Team8.append(roundResults.get('Team 8'))
        # print('Round ' + str(round + 1) + ': ' + str(roundResults))  # print results for each round
        print()
        draftOrder = draftOrder[::-1]  # reverses the draft order for every other round
        if round % 2 != 0:
            threshold += 1  # makes the AI choose from a larger pool of players every other round
        round += 1  # moves on to the next round
    """
    # prints the draft results!
    print('Your team: ' + str(userTeam))
    print('Team 2: ' + str(Team2))
    print('Team 3: ' + str(Team3))
    print('Team 4: ' + str(Team4))
    print('Team 5: ' + str(Team5))
    print('Team 6: ' + str(Team6))
    print('Team 7: ' + str(Team7))
    print('Team 8: ' + str(Team8))
    """
    print('Your Team: ' + str(userTeam))
    userDraftPicks.append(userTeam)
    print()
    print('End of Draft')
    print('\n')


draft_count = 1000
for _ in range(draft_count):
    fantasy_draft()
userDraftPicksFinal = [j for i in userDraftPicks for j in i]
draft_frequency = {}
for player in userDraftPicksFinal:
    if player in draft_frequency.keys():
        draft_frequency[player] += 1
    else:
        draft_frequency[player] = 1
for key, value in draft_frequency.items():
    draft_frequency[key] = (value / draft_count)

for key, value in sorted(draft_frequency.items(), key=lambda x: x[1], reverse=True):
    print(key, str(round(100 * value, 2)) + '%')
