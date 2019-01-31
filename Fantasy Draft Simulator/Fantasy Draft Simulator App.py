""" Fantasy Draft Simulator """

import requests
from bs4 import BeautifulSoup
import random
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

userDraftPicks = []

# ranked list of players that you want
userdict = {}

# ranked player list that everyone drafts from
session = requests.session()
req = session.get(
    'http://www.espn.com/fantasy/football/story/_/page/18RanksPreseason300nonPPR/2018-fantasy-football-non-ppr-rankings-top-300')
doc = BeautifulSoup(req.content, 'html.parser')
text = str(doc.get_text)

string = ''
for line in text.splitlines():
    if 'section class="col-c chk-height nocontent"' in line:
        string = line

words = string.split('<')

top300List = []
numlist = list(str(range(200)))
for word in words:
    if 'http://www.espn.com/nfl/player/_/id/' in word:
        name = word.split('>')
        if 'http://' not in name:
            top300List.append(name[1])
    elif 'D/ST' in word:
        dname = word.split('. ')
        if 'td>' not in dname:
            top300List.append(dname[1])
    elif 'http://www.espn.com/nfl/player/_/id/' not in word and 'td>' in word and any(
            num in word for num in numlist) and '.' in word:
        othername = word.split('. ')
        if 'td>' not in othername and othername[1] != '':
            top300List.append(othername[1])

top300Positions = []
poslist = ['td>QB', 'td>RB', 'td>WR', 'td>TE', 'td>DST', 'td>K']
for word in words:
    if any(pos == word for pos in poslist) and all(num not in word for num in numlist):
        position = word.split('>')
        top300Positions.append(position[1])

top300dict = dict(zip(top300List, top300Positions))


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
        self.pick_order_label = Label(text='Which pick in the draft do you want? ')
        self.pick_order_label.grid(row=11, column=5, sticky=W, padx=10, pady=10)
        self.pick_order = Entry()
        self.pick_order.grid(row=11, column=6, sticky=W, padx=10)
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
        self.results_list.grid(row=14, column=0, rowspan=7, columnspan=9, sticky=E + W, ipady=100, padx=20, pady=10)
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
        self.send_button = Button(text='Select All', command=self.select_all)
        self.send_button.grid(row=2, column=5, sticky=E + W)
        self.send_button = Button(text='Deselect All', command=self.deselect_all)
        self.send_button.grid(row=3, column=5, sticky=E + W)
        self.send_button = Button(text='>', command=self.choose_players)
        self.send_button.grid(row=4, column=5, sticky=E + W)
        self.send_button = Button(text='<', command=self.remove_player)
        self.send_button.grid(row=5, column=5, sticky=E + W)
        self.send_button = Button(text='<<', command=self.remove_all)
        self.send_button.grid(row=6, column=5, sticky=E + W)
        self.send_button = Button(text='Import List', command=self.import_list)
        self.send_button.grid(row=7, column=5, sticky=E + W)
        self.random_checkbox = Checkbutton(text='Random')
        self.random_checkbox.grid(row=11, column=7, sticky=W)
        self.random_checkbox.state(['!alternate'])
        self.draft_button = Button(text='Draft!', command=self.fantasy_draft)
        self.draft_button.grid(row=11, column=8, sticky=W, pady=10)

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
        for i in range(len(top300List)):
            self.player_list.insert(END, '       ' + str(top300List[i]) + '   ' + str(top300Positions[i]))

    def choose_players(self):
        selected_players = self.player_list.curselection()
        for i in selected_players:
            if top300List[i] not in self.user_player_list.get(0, END):
                self.user_player_list.insert(END, str(top300List[i]))
                userdict.update({top300List[i]: top300Positions[i]})
        print(userdict)

    def import_list(self):
        list_to_import = (1, 2, 3, 5, 9, 8, 12, 11, 13, 15, 25, 31, 24, 42, 37, 19, 82, 43, 55, 41, 39, 60, 52, 67)
        for i in list_to_import:
            if top300List[i] not in self.user_player_list.get(0, END):
                self.user_player_list.insert(END, str(top300List[i]))
                userdict.update({top300List[i]: top300Positions[i]})
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

    def select_all(self):
        self.player_list.select_set(first=0, last=END)

    def deselect_all(self):
        self.player_list.select_clear(0, END)

    def reset_all(self):
        self.player_list.select_clear(0, END)
        self.draft_count.delete(0, END)
        self.user_player_list.delete(0, END)
        userdict.clear()
        self.results_list.delete(0, END)

    def fantasy_draft(self):
        self.results_list.delete(0, END)

        draft_count = int(self.draft_count.get())
        try:
            pick_order = int(self.pick_order.get())
        except ValueError:
            if self.random_checkbox.instate(['selected']):
                pick_order = 0
            else:
                self.random_checkbox.state(['selected'])

        for _ in range(draft_count):
            # making player lists of each position
            userList = []
            compList = [key for key in top300dict.keys()]
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
            userTeam = []
            Team2 = []
            Team3 = []
            Team4 = []
            Team5 = []
            Team6 = []
            Team7 = []
            Team8 = []

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

            for player, position in top300dict.items():
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
                if all(top300dict.get(player) == position for player in list):
                    temp = list
                else:
                    for player in list:
                        if top300dict.get(player) != position:
                            temp.append(player)
                return temp

            def position_count(list1, list2):
                list3 = [value for value in list1 if value in list2]
                return list3

            # variables
            draftRound = 0
            threshold = 3

            # draft starts here
            print('The draft is live!')
            print(self.user_player_list.get(0, END))
            # randomizes the draft order
            team_dict = {'userTeam': userTeam, 'Team2': Team2, 'Team3': Team3, 'Team4': Team4,
                         'Team5': Team5, 'Team6': Team6, 'Team7': Team7, 'Team8': Team8}
            draftOrder = [team for team in team_dict.keys()]
            if self.random_checkbox.instate(['selected']):
                random.shuffle(draftOrder)
            else:
                user_pick = draftOrder.index('userTeam')
                draftOrder[user_pick], draftOrder[pick_order - 1] = draftOrder[pick_order - 1], draftOrder[user_pick]

            print(draftOrder)
            teamList = draftOrder
            roundsDrafted = 0
            print()

            try:
                while draftRound < 100:  # we only want a certain number of rounds
                    for team in teamList:
                        if draftRound != 0:
                            if team == 'userTeam':  # this is your team's pick logic
                                if len(userQBList) > 0 and ((position_count(userTeam,
                                                                            userQBList) == 1 and position_count(
                                        userTeam, userRBList) < 3 and position_count(userTeam,
                                                                                     userWRList) < 3) or position_count(
                                        userTeam, userQBList) == 2):
                                    pick = (position_ignore(userList, 'QB')[:1])[0]  # cases to ignore picking QB
                                elif len(userRBList) > 0 and ((position_count(userTeam,
                                                                              userRBList) == 3 and position_count(
                                        userTeam, userWRList) < 2) or (position_count(userTeam,
                                                                                      userRBList) == 4 and position_count(
                                        userTeam, userWRList) == 2)):
                                    pick = (position_ignore(userList, 'RB')[:1])[0]  # cases to ignore picking RB
                                elif len(userWRList) > 0 and ((position_count(userTeam,
                                                                              userWRList) == 3 and position_count(
                                        userTeam, userRBList) < 2) or (position_count(userTeam,
                                                                                      userWRList) == 4 and position_count(
                                        userTeam, userRBList) == 2)):
                                    pick = (position_ignore(userList, 'WR')[:1])[0]  # cases to ignore picking WR
                                elif len(userTEList) > 0 and position_count(userTeam, userTEList) == 2:
                                    pick = position_ignore(userList, 'TE')[:1][0]  # case to ignore picking TE
                                elif position_count(userTeam, userQBList) == 1 and position_count(userTeam,
                                                                                                  userRBList) < 4 and position_count(
                                        userTeam, userWRList) < 4 and position_count(userTeam, userTEList) == 1:
                                    random.sample(random.sample((userRBList + userWRList), 3),
                                                  1)  # cases to ignore QB and TE
                                elif position_count(userTeam, userQBList) == 0 and len(
                                        compQBList) > 0 and draftRound > 9:  # case to pick QB
                                    if len(userQBList) > 0:
                                        pick = userQBList[0]
                                    else:
                                        pick = compQBList[0]
                                elif position_count(userTeam, userTEList) == 0 and (len(userTEList) > 0 or len(
                                        compTEList) > 0) and draftRound > 10:  # case to pick TE
                                    if len(userTEList) > 0:
                                        pick = userTEList[0]
                                    else:
                                        pick = compTEList[0]
                                else:
                                    pick = (userList[:1])[0]  # pick the player at the top of your list
                                userTeam.append(pick)  # add the pick to your team
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
                                if len(compQBList) > 0 \
                                        and ((position_count(team_dict.get(team), compQBList) == 1
                                              and position_count(team_dict.get(team), compRBList) < 3
                                              and position_count(team_dict.get(team), compWRList) < 3)
                                             or position_count(team_dict.get(team), compQBList) == 2):
                                    try:
                                        pick = random.sample(position_ignore(compList, 'QB')[:threshold], 1)[
                                            0]  # cases to ignore picking QB
                                    except IndexError or ValueError:
                                        pick = random.sample(position_ignore(compList, 'QB'),
                                                             1)  # in case list length is below threshold
                                elif len(compRBList) > 0 and ((position_count(team_dict.get(team), compRBList) == 3 and position_count(
                                        team_dict.get(team), compWRList) < 2) or (position_count(team_dict.get(team),
                                                                                  compRBList) == 4 and position_count(team_dict.get(team), compWRList) == 2)):
                                    try:
                                        pick = random.sample(position_ignore(compList, 'RB')[:threshold], 1)[
                                            0]  # cases to ignore picking RB
                                    except IndexError or ValueError:
                                        pick = random.sample(position_ignore(compList, 'RB'), 1)
                                elif len(compWRList) > 0 and ((position_count(team_dict.get(team), compWRList) == 3 and position_count(
                                        team_dict.get(team), compRBList) < 2) or (position_count(team_dict.get(team),
                                                                                  compWRList) == 4 and position_count(team_dict.get(team), compRBList) == 2)):
                                    try:
                                        pick = random.sample(position_ignore(compList, 'WR')[:threshold], 1)[
                                            0]  # cases to ignore picking WR
                                    except IndexError or ValueError:
                                        pick = random.sample(position_ignore(compList, 'WR'), 1)
                                elif len(compTEList) > 0 and position_count(team_dict.get(team), compTEList) == 2:
                                    try:
                                        pick = random.sample(position_ignore(compList, 'TE')[:threshold], 1)[
                                            0]  # cases to ignore picking TE
                                    except IndexError or ValueError:
                                        pick = random.sample(position_ignore(compList, 'TE'), 1)
                                    except ValueError:
                                        try:
                                            pick = random.sample(compList[:threshold], 1)[0]
                                        except IndexError or ValueError:
                                            pick = random.sample(compList, 1)
                                elif position_count(team_dict.get(team), compQBList) == 1 and position_count(team_dict.get(team),
                                                                                              compRBList) < 4 and position_count(
                                    team_dict.get(team), compWRList) < 4 and position_count(team_dict.get(team), compTEList) == 1:
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
                                team_dict.get(team).append(pick)  # add the pick to the comp team
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
                            if team == 'userTeam':
                                pick = (userList[:1])[0]
                                userTeam.append(pick)
                                userList.remove(pick)
                                compList.remove(pick)
                            else:
                                pick = random.sample(compList[:threshold], 1)[0]
                                team_dict.get(team).append(pick)
                                if pick in userList:
                                    userList.remove(pick)
                                compList.remove(pick)
                    print()
                    teamList = teamList[::-1]  # reverses the draft order for every other round
                    if draftRound % 2 == 0:
                        threshold += 2  # makes the AI choose from a larger pool of players every other round
                    draftRound += 1  # moves on to the next round
                    roundsDrafted += 1
            except IndexError:
                print("Couldn't draft all players.")
                pass
            print('Your Team: ' + str(userTeam))
            userDraftPicks.append(userTeam)
            print()
            print('Rounds drafted: ' + str(roundsDrafted))
            print()
            print('End of Draft')
            print('\n')

        userDraftPicksFinal = [j for i in userDraftPicks for j in i]
        draft_frequency = {}
        for player in userDraftPicksFinal:
            if player in draft_frequency.keys():
                draft_frequency[player] += 1
            else:
                draft_frequency[player] = 1
        for key, value in draft_frequency.items():
            draft_frequency[key] = (value / draft_count)

        if self.random_checkbox.instate(['selected']):
            self.results_list.insert(END, 'The draft orders were randomized.')
        else:
            if draftOrder.index('userTeam') == 0:
                self.results_list.insert(END, 'You picked 1st.')
            elif draftOrder.index('userTeam') == 1:
                self.results_list.insert(END, 'You picked 2nd.')
            elif draftOrder.index('userTeam') == 2:
                self.results_list.insert(END, 'You picked 3rd.')
            else:
                self.results_list.insert(END, 'You picked ' + str(draftOrder.index('userTeam') + 1) + 'th.')
        self.results_list.insert(END, '\n')
        self.results_list.insert(END, 'Number of rounds per draft: ' + str(roundsDrafted))
        self.results_list.insert(END, '\n')
        self.results_list.insert(END, '-' * 55)
        self.results_list.insert(END, '    Name            Position      Draft Frequency')
        self.results_list.insert(END, '-' * 55)
        for key, value in sorted(draft_frequency.items(), key=lambda x: x[1], reverse=True):
            keystring = key + ' ' * (22 - len(str(key)))
            positionstring = top300dict.get(key) + ' ' * 15
            self.results_list.insert(END, keystring + positionstring + str(round((100.0 * value), 2)) + '%')
            # print(keystring, positionstring, str(round((100.0 * value), 2)) + '%')
        self.results_list.insert(END, '\n' '\n')
        userDraftPicks.clear()
        userDraftPicksFinal.clear()
        draft_frequency.clear()
        messagebox.showinfo('Nice.', 'Your drafts are complete.')
        print('\n')
        testList = []
        for i in self.user_player_list.get(0, END):
            testList.append(top300List.index(i))
        testTuple = tuple(testList)
        print(testTuple)



root = Tk()
ds = draftSimulator(root)
root.mainloop()
