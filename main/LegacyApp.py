""" Fantasy Draft Simulator """

from main.GetPlayers import *
import random
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

userDraftPicks = []

# ranked list of players that you want
user_dict = {}


# functions
def position_ignore(player_list, pos):
    if all(top300dict.get(player) == pos for player in player_list):
        temp = player_list
    else:
        temp = [player for player in player_list if top300dict.get(player) != pos]
    return temp


def position_count(list1, list2):
    list3 = [item for item in list1 if item in list2]
    return len(list3)


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
        def set_current(event):
            self.user_player_list.curIndex = self.user_player_list.nearest(event.y)

        def shift_selection(event):
            item = self.user_player_list.nearest(event.y)
            if item < self.user_player_list.curIndex:
                x = self.user_player_list.get(item)
                self.user_player_list.delete(item)
                self.user_player_list.insert(item + 1, x)
                self.user_player_list.curIndex = item
            elif item > self.user_player_list.curIndex:
                x = self.user_player_list.get(item)
                self.user_player_list.delete(item)
                self.user_player_list.insert(item - 1, x)
                self.user_player_list.curIndex = item

        self.user_player_list.bind('<Button-1>', set_current)
        self.user_player_list.bind('<B1-Motion>', shift_selection)
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
        self.draft_button = Button(text='Draft!', command=self.simulate_draft)
        self.draft_button.grid(row=11, column=8, sticky=W, pady=10)

        # menu
        menu = Menu(root)
        root.config(menu=menu)

        file_menu = Menu(menu)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Reset', command=self.reset_all)

        for i in range(len(top300List)):
            self.player_list.insert(END, '       ' + str(top300List[i]) + '   ' + str(top300Positions[i]))

    def choose_players(self):
        selected_players = self.player_list.curselection()
        for i in selected_players:
            if top300List[i] not in self.user_player_list.get(0, END):
                self.user_player_list.insert(END, str(top300List[i]))
                user_dict.update({top300List[i]: top300Positions[i]})
        print(user_dict)

    def import_list(self):
        list_to_import = (1, 2, 3, 5, 9, 8, 12, 11, 13, 15, 25, 31, 24, 42, 37, 19, 82, 43, 55, 41, 39, 60, 52, 67)
        for i in list_to_import:
            if top300List[i] not in self.user_player_list.get(0, END):
                self.user_player_list.insert(END, str(top300List[i]))
                user_dict.update({top300List[i]: top300Positions[i]})
        print(user_dict)

    def remove_player(self):
        selected_players = self.user_player_list.curselection()
        self.user_player_list.delete(selected_players)
        selection_list = [key for key in user_dict.keys()]
        for i in selected_players:
            del user_dict[selection_list[i]]
        print(user_dict)

    def remove_all(self):
        self.user_player_list.delete(0, END)
        user_dict.clear()
        print(user_dict)

    def select_all(self):
        self.player_list.select_set(first=0, last=END)

    def deselect_all(self):
        self.player_list.select_clear(0, END)

    def reset_all(self):
        self.player_list.select_clear(0, END)
        self.draft_count.delete(0, END)
        self.user_player_list.delete(0, END)
        user_dict.clear()
        self.results_list.delete(0, END)

    def simulate_draft(self):
        self.results_list.delete(0, END)

        draft_count = int(self.draft_count.get())
        pick_order = 0
        try:
            pick_order = int(self.pick_order.get())
        except ValueError:
            if self.random_checkbox.instate(['selected']):
                pick_order = 0
            else:
                self.random_checkbox.state(['selected'])

        # dictionary and list creation
        user_qb_list = [player for player, pos in user_dict.items() if pos == 'QB']
        user_rb_list = [player for player, pos in user_dict.items() if pos == 'RB']
        user_wr_list = [player for player, pos in user_dict.items() if pos == 'WR']
        user_te_list = [player for player, pos in user_dict.items() if pos == 'TE']
        comp_qb_list = [player for player, pos in top300dict.items() if pos == 'QB']
        comp_rb_list = [player for player, pos in top300dict.items() if pos == 'RB']
        comp_wr_list = [player for player, pos in top300dict.items() if pos == 'WR']
        comp_te_list = [player for player, pos in top300dict.items() if pos == 'TE']
        user_team = []
        team_2 = []
        team_3 = []
        team_4 = []
        team_5 = []
        team_6 = []
        team_7 = []
        team_8 = []

        rounds_drafted = 0

        # determine draft order if not random
        print(self.user_player_list.get(0, END))
        team_dict = {'user_team': user_team, 'team_2': team_2, 'team_3': team_3, 'team_4': team_4,
                     'team_5': team_5, 'team_6': team_6, 'team_7': team_7, 'team_8': team_8}
        draft_order = [team for team in team_dict.keys()]
        if self.random_checkbox.instate(['']):
            user_pick = draft_order.index('user_team')
            draft_order[user_pick], draft_order[pick_order - 1] = draft_order[pick_order - 1], draft_order[
                user_pick]
        user_draft_pick = draft_order.index('user_team')

        for _ in range(draft_count):
            # making player lists of each position
            user_list = [i for i in self.user_player_list.get(0, END)]
            comp_list = [key for key in top300dict.keys()]
            print(user_list)

            # variables
            draft_round = 0
            threshold = 3

            # draft starts here
            print('The draft is live!')

            if self.random_checkbox.instate(['selected']):
                random.shuffle(draft_order)

            print()
            pick = None

            try:
                while draft_round < 100:  # we only want a certain number of rounds
                    for team in draft_order:
                        if draft_round != 0:
                            if team == 'user_team':  # this is your team's pick logic
                                if len(user_qb_list) > 0 and (
                                        (position_count(user_team, user_qb_list) == 1 and position_count(user_team,
                                                                                                         user_rb_list) < 3 and position_count(
                                            user_team, user_wr_list) < 3) or position_count(user_team,
                                                                                            user_qb_list) == 2):
                                    pick = (position_ignore(user_list, 'QB')[:1])[0]  # cases to ignore picking QB
                                elif len(user_rb_list) > 0 and (
                                        (position_count(user_team, user_rb_list) == 3 and position_count(user_team,
                                                                                                         user_wr_list) < 2) or (
                                                position_count(user_team, user_rb_list) == 4 and position_count(user_team, user_wr_list) == 2)):
                                    pick = (position_ignore(user_list, 'RB')[:1])[0]  # cases to ignore picking RB
                                elif len(user_wr_list) > 0 and (
                                        (position_count(user_team, user_wr_list) == 3 and position_count(user_team,
                                                                                                         user_rb_list) < 2) or (
                                                position_count(user_team, user_wr_list) == 4 and position_count(user_team, user_rb_list) == 2)):
                                    pick = (position_ignore(user_list, 'WR')[:1])[0]  # cases to ignore picking WR
                                elif len(user_te_list) > 0 and position_count(user_team, user_te_list) == 2:
                                    pick = position_ignore(user_list, 'TE')[:1][0]  # case to ignore picking TE
                                elif position_count(user_team, user_qb_list) == 1 and position_count(user_team,
                                                                                                     user_rb_list) < 4 and position_count(user_team, user_wr_list) < 4 and position_count(user_team, user_te_list) == 1:
                                    random.sample(random.sample((user_rb_list + user_wr_list), 3),
                                                  1)  # cases to ignore QB and TE
                                elif position_count(user_team, user_qb_list) == 0 and len(
                                        comp_qb_list) > 0 and draft_round > 9:  # case to pick QB
                                    if len(user_qb_list) > 0:
                                        pick = user_qb_list[0]
                                    else:
                                        pick = comp_qb_list[0]
                                elif position_count(user_team, user_te_list) == 0 and (len(user_te_list) > 0 or len(
                                        comp_te_list) > 0) and draft_round > 10:  # case to pick TE
                                    if len(user_te_list) > 0:
                                        pick = user_te_list[0]
                                    else:
                                        pick = comp_te_list[0]
                                else:
                                    pick = (user_list[:1])[0]  # pick the player at the top of your list
                                user_team.append(pick)  # add the pick to your team
                                if pick in user_list:
                                    user_list.remove(pick)  # remove the player from your draft list
                                if pick in comp_list:
                                    comp_list.remove(pick)  # remove the player from the master list
                                if pick in user_qb_list:
                                    user_qb_list.remove(pick)
                                elif pick in user_rb_list:
                                    user_rb_list.remove(pick)
                                elif pick in user_wr_list:
                                    user_wr_list.remove(pick)
                                elif pick in user_te_list:
                                    user_te_list.remove(pick)
                                elif pick in comp_qb_list:
                                    comp_qb_list.remove(pick)
                                elif pick in comp_rb_list:
                                    comp_rb_list.remove(pick)
                                elif pick in comp_wr_list:
                                    comp_wr_list.remove(pick)
                                elif pick in comp_te_list:
                                    comp_te_list.remove(pick)
                            else:  # this is the AI's pick logic
                                if len(comp_qb_list) > 0 \
                                        and ((position_count(team_dict.get(team), comp_qb_list) == 1
                                              and position_count(team_dict.get(team), comp_rb_list) < 3
                                              and position_count(team_dict.get(team), comp_wr_list) < 3)
                                             or position_count(team_dict.get(team), comp_qb_list) == 2):
                                    try:
                                        pick = random.sample(position_ignore(comp_list, 'QB')[:threshold], 1)[
                                            0]  # cases to ignore picking QB
                                    except IndexError or ValueError:
                                        pick = random.sample(position_ignore(comp_list, 'QB'),
                                                             1)  # in case list length is below threshold
                                elif len(comp_rb_list) > 0 and (
                                        (position_count(team_dict.get(team), comp_rb_list) == 3 and position_count(
                                            team_dict.get(team), comp_wr_list) < 2) or (
                                                position_count(team_dict.get(team),
                                                               comp_rb_list) == 4 and position_count(team_dict.get(team), comp_wr_list) == 2)):
                                    try:
                                        pick = random.sample(position_ignore(comp_list, 'RB')[:threshold], 1)[
                                            0]  # cases to ignore picking RB
                                    except IndexError or ValueError:
                                        pick = random.sample(position_ignore(comp_list, 'RB'), 1)
                                elif len(comp_wr_list) > 0 and (
                                        (position_count(team_dict.get(team), comp_wr_list) == 3 and position_count(
                                            team_dict.get(team), comp_rb_list) < 2) or (
                                                position_count(team_dict.get(team),
                                                               comp_wr_list) == 4 and position_count(team_dict.get(team), comp_rb_list) == 2)):
                                    try:
                                        pick = random.sample(position_ignore(comp_list, 'WR')[:threshold], 1)[
                                            0]  # cases to ignore picking WR
                                    except IndexError or ValueError:
                                        pick = random.sample(position_ignore(comp_list, 'WR'), 1)
                                elif len(comp_te_list) > 0 and position_count(team_dict.get(team), comp_te_list) == 2:
                                    try:
                                        pick = random.sample(position_ignore(comp_list, 'TE')[:threshold], 1)[
                                            0]  # cases to ignore picking TE
                                    except IndexError or ValueError:
                                        pick = random.sample(position_ignore(comp_list, 'TE'), 1)
                                    except ValueError:
                                        try:
                                            pick = random.sample(comp_list[:threshold], 1)[0]
                                        except IndexError or ValueError:
                                            pick = random.sample(comp_list, 1)
                                elif position_count(team_dict.get(team), comp_qb_list) == 1 and position_count(
                                        team_dict.get(team),
                                        comp_rb_list) < 4 and position_count(
                                    team_dict.get(team), comp_wr_list) < 4 and position_count(team_dict.get(team),
                                                                                              comp_te_list) == 1:
                                    random.sample(random.sample((comp_rb_list + comp_wr_list), 3), 1)
                                elif position_count(team_dict.get(team), comp_qb_list) == 0 and len(
                                        comp_qb_list) > 0 and draft_round > 9:
                                    pick = random.sample(comp_qb_list, 1)  # case to pick QB
                                elif position_count(team_dict.get(team), comp_te_list) == 0 and len(
                                        comp_te_list) > 0 and draft_round > 10:
                                    try:
                                        pick = random.sample(comp_te_list[:threshold], 1)[0]  # case to pick TE
                                    except IndexError or ValueError:
                                        pick = random.sample(comp_te_list, 1)
                                else:  # pick a random player from the top "threshold" players
                                    try:
                                        pick = random.sample(comp_list[:threshold], 1)[0]
                                    except IndexError or ValueError:
                                        pick = random.sample(comp_list, 1)
                                team_dict.get(team).append(pick)  # add the pick to the comp team
                                if pick in user_list:
                                    user_list.remove(pick)
                                if pick in comp_list:
                                    comp_list.remove(pick)
                                if pick in user_qb_list:
                                    user_qb_list.remove(pick)
                                elif pick in user_rb_list:
                                    user_rb_list.remove(pick)
                                elif pick in user_wr_list:
                                    user_wr_list.remove(pick)
                                elif pick in user_te_list:
                                    user_te_list.remove(pick)
                                elif pick in comp_qb_list:
                                    comp_qb_list.remove(pick)
                                elif pick in comp_rb_list:
                                    comp_rb_list.remove(pick)
                                elif pick in comp_wr_list:
                                    comp_wr_list.remove(pick)
                                elif pick in comp_te_list:
                                    comp_te_list.remove(pick)
                        else:  # can't check for a team having too many of one position in the first round
                            if team == 'user_team':
                                pick = (user_list[:1])[0]
                                user_team.append(pick)
                                user_list.remove(pick)
                                comp_list.remove(pick)
                            else:
                                pick = random.sample(comp_list[:threshold], 1)[0]
                                team_dict.get(team).append(pick)
                                if pick in user_list:
                                    user_list.remove(pick)
                                comp_list.remove(pick)
                    print()
                    draft_order = draft_order[::-1]  # reverses the draft order for every other round
                    if draft_round % 2 == 0:
                        threshold += 2  # makes the AI choose from a larger pool of players every other round
                    draft_round += 1  # moves on to the next round
                    rounds_drafted += 1
            except IndexError:
                print("Couldn't draft all players.")
                pass
            print('Your Team: ' + str(user_team))
            userDraftPicks.append(user_team)
            print()
            print('Rounds drafted: ' + str(rounds_drafted))
            print()
            print('End of Draft')
            print('\n')

        user_draft_picks_final = [j for i in userDraftPicks for j in i]
        draft_frequency = {}
        for player in user_draft_picks_final:
            if player in draft_frequency.keys():
                draft_frequency[player] += 1
            else:
                draft_frequency[player] = 1
        for key, value in draft_frequency.items():
            draft_frequency[key] = (value / draft_count)

        if self.random_checkbox.instate(['selected']):
            self.results_list.insert(END, 'The draft orders were randomized.')
        else:
            if user_draft_pick == 0:
                self.results_list.insert(END, 'You picked 1st.')
            elif user_draft_pick == 1:
                self.results_list.insert(END, 'You picked 2nd.')
            elif user_draft_pick == 2:
                self.results_list.insert(END, 'You picked 3rd.')
            else:
                self.results_list.insert(END, 'You picked ' + str(user_draft_pick + 1) + 'th.')
        self.results_list.insert(END, '\n')
        self.results_list.insert(END, 'Number of rounds per draft: ' + str(rounds_drafted))
        self.results_list.insert(END, '\n')
        self.results_list.insert(END, '-' * 55)
        self.results_list.insert(END, '    Name            Position      Draft Frequency')
        self.results_list.insert(END, '-' * 55)
        for key, value in sorted(draft_frequency.items(), key=lambda x: x[1], reverse=True):
            key_string = key + ' ' * (22 - len(str(key)))
            position_string = top300dict.get(key) + ' ' * 15
            self.results_list.insert(END, key_string + position_string + str(round((100.0 * value), 2)) + '%')
            # print(key_string, position_string, str(round((100.0 * value), 2)) + '%')
        self.results_list.insert(END, '\n' '\n')
        userDraftPicks.clear()
        user_draft_picks_final.clear()
        draft_frequency.clear()
        messagebox.showinfo('Nice.', 'Your drafts are complete.')
        print('\n')
        test_list = []
        for i in self.user_player_list.get(0, END):
            test_list.append(top300List.index(i))
        test_tuple = tuple(test_list)
        print(test_tuple)


root = Tk()
ds = draftSimulator(root)
root.mainloop()