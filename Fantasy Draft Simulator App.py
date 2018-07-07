""" Fantasy Draft Simulator """

import random
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

userDraftPicks = []

# ranked list of players that you want
userdict = {}

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

top200List = [key for key in top200dict.keys()]
top200Positions = [value for value in top200dict.values()]


class draftSimulator(Tk):

    def __init__(self, master):
        root.title('Fantasy Draft Simulator')

        # labels and entry boxes
        self.player_list_label = Label(text='ESPN Top 200 Players:')
        self.player_list_label.grid(row=0, column=0, columnspan=4, sticky=W, padx=20, pady=5)
        self.rank_list_label = Label(text='Players you want ordered by preference (drag & drop):')
        self.rank_list_label.grid(row=0, column=6, columnspan=4, sticky=W, padx=20, pady=5)
        self.draft_count_label = Label(text='Enter number of simulations:')
        self.draft_count_label.grid(row=11, column=0, sticky=W, padx=10, pady=10)
        self.draft_count = Entry()
        self.draft_count.grid(row=11, column=2, sticky=W, padx=10)
        self.round_count_label = Label(text='Enter number of rounds per draft:')
        self.round_count_label.grid(row=11, column=5, sticky=W, padx=10, pady=10)
        self.round_count = Entry()
        self.round_count.grid(row=11, column=6, sticky=W, padx=10)
        self.results_list_label = Label(text='Draft Simulation Results:')
        self.results_list_label.grid(row=13, column=0, sticky=E + W, padx=20)

        # lists of players and scrollbar
        self.player_list = Listbox(selectmode=MULTIPLE, activestyle='none')
        self.player_list.grid(row=1, column=0, rowspan=10, columnspan=4, sticky=N + E + W + S, ipady=50, padx=20,
                              pady=5)
        self.user_player_list = Listbox(selectmode=SINGLE, activestyle='none')
        self.user_player_list.grid(row=1, column=6, rowspan=10, columnspan=4, sticky=N + E + W + S, ipadx=80, ipady=50,
                                   padx=20, pady=5)
        self.results_list = Listbox(activestyle='none', font='Monaco')
        self.results_list.grid(row=14, column=0, rowspan=7, columnspan=9, sticky=E + W, ipady=150, padx=20, pady=10)
        self.left_scrollbar = Scrollbar(self.player_list, orien='vertical', command=self.player_list.yview)
        self.player_list.configure(yscrollcommand=self.left_scrollbar.set)
        self.left_scrollbar.pack(side=LEFT, fill=Y)

        # self.right_scrollbar = Scrollbar(self.user_player_list, orien='vertical', command=self.user_player_list.yview)
        # self.player_list.configure(yscrollcommand=self.right_scrollbar.set)
        # self.right_scrollbar.pack(side=LEFT, fill=Y)

        # drag & drop!!!
        def setCurrent(event):
            self.user_player_list.curIndex = self.user_player_list.nearest(event.y)

        def shiftSelection(event):
            i = self.user_player_list.nearest(event.y)
            if i < self.user_player_list.curIndex:
                x = self.user_player_list.get(i)
                self.user_player_list.delete(i)
                self.user_player_list.insert(i + 1, x)
                self.user_player_list.curIndex = i
            elif i > self.user_player_list.curIndex:
                x = self.user_player_list.get(i)
                self.user_player_list.delete(i)
                self.user_player_list.insert(i - 1, x)
                self.user_player_list.curIndex = i

        self.user_player_list.bind('<Button-1>', setCurrent)
        self.user_player_list.bind('<B1-Motion>', shiftSelection)
        self.user_player_list.curIndex = None

        # buttons
        self.send_button = Button(text='Deselect All', command=self.deselect_all)
        self.send_button.grid(row=3, column=5, sticky=E + W)
        self.send_button = Button(text='>', command=self.choose_players)
        self.send_button.grid(row=4, column=5, sticky=E + W)
        self.send_button = Button(text='<', command=self.remove_player)
        self.send_button.grid(row=5, column=5, sticky=E + W)
        self.send_button = Button(text='<<', command=self.remove_all)
        self.send_button.grid(row=6, column=5, sticky=E + W)
        self.draft_button = Button(text='Draft!', command=self.fantasy_draft)
        self.draft_button.grid(row=11, column=7, sticky=W, pady=10)

        # menu
        menu = Menu(root)
        root.config(menu=menu)

        filemenu = Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='Reset', command=self.reset_all)
        """
        editmenu = Menu(menu)
        menu.add_cascade(label='Help', menu=editmenu)
        editmenu.add_command(label='Help')  # command=
        """
        for i in range(len(top200List)):
            self.player_list.insert(END, '       ' + str(top200List[i]) + '   ' + str(top200Positions[i]))

    def choose_players(self):
        selected_players = self.player_list.curselection()
        for i in selected_players:
            if top200List[i] not in self.user_player_list.get(0, END):
                self.user_player_list.insert(END, str(top200List[i]))
                userdict.update({top200List[i]: top200Positions[i]})
        print(userdict)

    def remove_player(self):
        selected_players = self.user_player_list.curselection()
        self.user_player_list.delete(selected_players)
        selectionlist = [key for key in userdict.keys()]
        for i in selected_players:
            del userdict[selectionlist[i]]
        print(userdict)

    def remove_all(self):
        self.user_player_list.delete(0, END)
        userdict.clear()
        print(userdict)

    def deselect_all(self):
        self.player_list.select_clear(0, END)

    def reset_all(self):
        self.player_list.select_clear(0, END)
        self.draft_count.delete(0, END)
        self.user_player_list.delete(0, END)
        userdict.clear()
        self.results_list.delete(0, END)

    def fantasy_draft(self):
        draft_count = int(self.draft_count.get())
        round_count = int(self.round_count.get())

        for _ in range(draft_count):
            try:
                # making player lists of each position
                userList = []
                compList = [key for key in top200dict.keys()]
                for i in self.user_player_list.get(0, END):
                    userList.append(i)
                print(userList)

                # dictionary and list creation
                userQBList = []
                userRBList = []
                userWRList = []
                userTEList = []
                compQBList = []
                compRBList = []
                compWRList = []
                compTEList = []
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
                        compQBList.append(player)
                    elif position == 'RB':
                        compRBList.append(player)
                    elif position == 'WR':
                        compWRList.append(player)
                    elif position == 'TE':
                        compTEList.append(player)

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
                draftRound = 0
                threshold = 3

                # draft starts here
                print('The draft is live!')
                print(self.user_player_list.get(ACTIVE))
                # randomizes the draft order
                draftOrder = ['user', 'Team 2', 'Team 3', 'Team 4', 'Team 5', 'Team 6', 'Team 7', 'Team 8']
                random.shuffle(draftOrder)
                print(draftOrder)
                print()

                while draftRound < round_count:  # we only want a certain number of rounds
                    for team in draftOrder:
                        if draftRound != 0:
                            if team == 'user':  # this is your team's pick logic
                                if len(userQBList) > 0 and ((position_count(userTeam, userQBList) == 1 and position_count(userTeam, userRBList) < 3 and position_count(userTeam, userWRList) < 3) or position_count(userTeam, userQBList) == 2):
                                    pick = (position_ignore(userList, 'QB')[:1])[0]  # cases to ignore picking QB
                                elif len(userRBList) > 0 and ((position_count(userTeam, userRBList) == 3 and position_count(userTeam, userWRList) < 2) or (position_count(userTeam, userRBList) == 4 and position_count(userTeam, userWRList) == 2)):
                                    pick = (position_ignore(userList, 'RB')[:1])[0]  # cases to ignore picking RB
                                elif len(userWRList) > 0 and ((position_count(userTeam, userWRList) == 3 and position_count(userTeam, userRBList) < 2) or (position_count(userTeam, userWRList) == 4 and position_count(userTeam, userRBList) == 2)):
                                    pick = (position_ignore(userList, 'WR')[:1])[0]  # cases to ignore picking WR
                                elif len(userTEList) > 0 and position_count(userTeam, userTEList) == 2:
                                    pick = position_ignore(userList, 'TE')[:1][0]  # case to ignore picking TE
                                elif position_count(userTeam, userQBList) == 1 and position_count(userTeam, userRBList) < 4 and position_count(userTeam, userWRList) < 4 and position_count(userTeam, userTEList) == 1:
                                    random.sample(random.sample((userRBList + userWRList), 3), 1)  # cases to ignore QB and TE
                                elif position_count(userTeam, userQBList) == 0 and len(compQBList) > 0 and draftRound > 9:  # case to pick QB
                                    if len(userQBList) > 0:
                                        pick = userQBList[0]
                                    else:
                                        pick = compQBList[0]
                                elif position_count(userTeam, userTEList) == 0 and (len(userTEList) > 0 or len(compTEList) > 0) and draftRound > 10:  # case to pick TE
                                    if len(userTEList) > 0:
                                        pick = userTEList[0]
                                    else:
                                        pick = compTEList[0]
                                else:
                                    pick = (userList[:1])[0]  # pick the player at the top of your list
                                roundResults.update({team: pick})  # add the pick to the round results dictionary
                                if pick in userList:
                                    userList.remove(pick)  # remove the player from your draft list
                                if pick in compList:
                                    compList.remove(pick)  # remove the player from the master list
                                if pick in userQBList:
                                    userQBList.remove(pick)
                                elif pick in userRBList:
                                    userRBList.remove(pick)
                                elif pick in userWRList:
                                    userWRList.remove(pick)
                                elif pick in userTEList:
                                    userTEList.remove(pick)
                                elif pick in compQBList:
                                    compQBList.remove(pick)
                                elif pick in compRBList:
                                    compRBList.remove(pick)
                                elif pick in compWRList:
                                    compWRList.remove(pick)
                                elif pick in compTEList:
                                    compTEList.remove(pick)
                            else:  # this is the AI's pick logic
                                if len(compQBList) > 0 and ((position_count(team_dict.get(team), compQBList) == 1 and position_count(team_dict.get(team), compRBList) < 3 and position_count(team_dict.get(team), compWRList) < 3) or position_count(team_dict.get(team), compQBList) == 2):
                                    try:
                                        pick = random.sample(position_ignore(compList, 'QB')[:threshold], 1)[0]  # cases to ignore picking QB
                                    except IndexError or ValueError:
                                        pick = random.sample(position_ignore(compList, 'QB'), 1)  # in case list length is below threshold
                                elif len(compRBList) > 0 and ((position_count(team_dict.get(team), compRBList) == 3 and position_count(team_dict.get(team), compWRList) < 2) or (position_count(team_dict.get(team), compRBList) == 4 and position_count(team_dict.get(team), compWRList) == 2)):
                                    try:
                                        pick = random.sample(position_ignore(compList, 'RB')[:threshold], 1)[0]  # cases to ignore picking RB
                                    except IndexError or ValueError:
                                        pick = random.sample(position_ignore(compList, 'RB'), 1)
                                elif len(compWRList) > 0 and ((position_count(team_dict.get(team), compWRList) == 3 and position_count(team_dict.get(team), compRBList) < 2) or (position_count(team_dict.get(team), compWRList) == 4 and position_count(team_dict.get(team), compRBList) == 2)):
                                    try:
                                        pick = random.sample(position_ignore(compList, 'WR')[:threshold], 1)[0]  # cases to ignore picking WR
                                    except IndexError or ValueError:
                                        pick = random.sample(position_ignore(compList, 'WR'), 1)
                                elif len(compTEList) > 0 and position_count(team_dict.get(team), compTEList) == 2:
                                    try:
                                        pick = random.sample(position_ignore(compList, 'TE')[:threshold], 1)[0]  # cases to ignore picking TE
                                    except IndexError or ValueError:
                                        pick = random.sample(position_ignore(compList, 'TE'), 1)
                                    except ValueError:
                                        try:
                                            pick = random.sample(compList[:threshold], 1)[0]
                                        except IndexError or ValueError:
                                            pick = random.sample(compList, 1)
                                elif position_count(team_dict.get(team), compQBList) == 1 and position_count(team_dict.get(team), compRBList) < 4 and position_count(team_dict.get(team), compWRList) < 4 and position_count(team_dict.get(team), compTEList) == 1:
                                    random.sample(random.sample((compRBList + compWRList), 3), 1)
                                elif position_count(team_dict.get(team), compQBList) == 0 and len(compQBList) > 0 and draftRound > 9:
                                    pick = random.sample(compQBList, 1)  # case to pick QB
                                elif position_count(team_dict.get(team), compTEList) == 0 and len(compTEList) > 0 and draftRound > 10:
                                    try:
                                        pick = random.sample(compTEList[:threshold], 1)[0]  # case to pick TE
                                    except IndexError or ValueError:
                                        pick = random.sample(compTEList, 1)
                                else:  # pick a random player from the top "threshold" players
                                    try:
                                        pick = random.sample(compList[:threshold], 1)[0]
                                    except IndexError or ValueError:
                                        pick = random.sample(compList, 1)
                                roundResults.update({team: pick})
                                if pick in userList:
                                    userList.remove(pick)
                                if pick in compList:
                                    compList.remove(pick)
                                if pick in userQBList:
                                    userQBList.remove(pick)
                                elif pick in userRBList:
                                    userRBList.remove(pick)
                                elif pick in userWRList:
                                    userWRList.remove(pick)
                                elif pick in userTEList:
                                    userTEList.remove(pick)
                                elif pick in compQBList:
                                    compQBList.remove(pick)
                                elif pick in compRBList:
                                    compRBList.remove(pick)
                                elif pick in compWRList:
                                    compWRList.remove(pick)
                                elif pick in compTEList:
                                    compTEList.remove(pick)
                        else:  # can't check for a team having too many of one position in the first round
                            if team == 'user':
                                pick = (userList[:1])[0]
                                roundResults.update({team: pick})
                                userList.remove(pick)
                                compList.remove(pick)
                            else:
                                pick = random.sample(compList[:threshold], 1)[0]
                                roundResults.update({team: pick})
                                if pick in userList:
                                    userList.remove(pick)
                                compList.remove(pick)
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
                    if draftRound % 6 == 0:
                        threshold += 1  # makes the AI choose from a larger pool of players every other round
                    draftRound += 1  # moves on to the next round
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
            except IndexError:
                messagebox.showinfo('Damn.',
                                    'You have entered too few players to draft. Please select additional players.')
                draftRound = 0
                threshold = 3
                break

        if draftRound == round_count:
            userDraftPicksFinal = [j for i in userDraftPicks for j in i]
            draft_frequency = {}
            for player in userDraftPicksFinal:
                if player in draft_frequency.keys():
                    draft_frequency[player] += 1
                else:
                    draft_frequency[player] = 1
            for key, value in draft_frequency.items():
                draft_frequency[key] = (value / draft_count)

            self.results_list.insert(END, '-' * 55)
            self.results_list.insert(END, '    Name            Position      Draft Frequency')
            self.results_list.insert(END, '-' * 55)
            for key, value in sorted(draft_frequency.items(), key=lambda x: x[1], reverse=True):
                keystring = key + ' ' * (22 - len(str(key)))
                positionstring = top200dict.get(key) + ' ' * 15
                self.results_list.insert(END, keystring + positionstring + str(round((100.0 * value), 2)) + '%')
                print(keystring, positionstring, str(round((100.0 * value), 2)) + '%')
            self.results_list.insert(END, '\n' '\n')
            userDraftPicks.clear()
            userDraftPicksFinal.clear()
            draft_frequency.clear()
            messagebox.showinfo('Nice.', 'Your drafts are complete.')


root = Tk()
ds = draftSimulator(root)
root.mainloop()
