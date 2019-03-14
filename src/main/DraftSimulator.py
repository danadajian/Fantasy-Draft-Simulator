""" Fantasy Draft Simulator """

import requests
from bs4 import BeautifulSoup
import random
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog

# ranked player list that everyone drafts from
session = requests.session()
request = session.get('http://www.espn.com/fantasy/football/story/_/page/18RanksPreseason300nonPPR/'
                      + '2018-fantasy-football-non-ppr-rankings-top-300')
doc = BeautifulSoup(request.content, 'html.parser')
text = str(doc.get_text)

string = ''
for line in text.splitlines():
    if 'section class="col-c chk-height nocontent"' in line:
        string = line

words = string.split('<')

top300List = []
numList = list(str(range(200)))
for word in words:
    if 'http://www.espn.com/nfl/player/_/id/' in word:
        name = word.split('>')
        if 'http://' not in name:
            top300List.append(name[1])
    elif 'D/ST' in word:
        dName = word.split('. ')
        if 'td>' not in dName:
            top300List.append(dName[1])
    elif 'http://www.espn.com/nfl/player/_/id/' not in word and 'td>' in word and any(
            num in word for num in numList) and '.' in word:
        otherName = word.split('. ')
        if 'td>' not in otherName and otherName[1] != '':
            top300List.append(otherName[1])

top300Positions = []
posList = ['td>QB', 'td>RB', 'td>WR', 'td>TE', 'td>DST', 'td>K']
for word in words:
    if any(pos == word for pos in posList) and all(num not in word for num in numList):
        position = word.split('>')
        top300Positions.append(position[1])

top300dict = dict(zip(top300List, top300Positions))

userDraftPicks = []
user_dict = {}


# core functions
def position_count(player_list, pos):
    result = [player for player in player_list if top300dict.get(player) == pos]
    return len(result)


def valid_choice(player, user_team):
    if player:
        pos_limits = {'QB': 2, 'RB': 5, 'WR': 5, 'TE': 2, 'DST': 1, 'K': 1}
        player_pos = top300dict.get(player)
        if position_count(user_team, player_pos) + 1 <= pos_limits.get(player_pos):
            return True
    return False


class draftSimulator(Tk):

    # GUI
    def __init__(self, master):
        root.title('Fantasy Draft Simulator')

        # labels and entry boxes
        self.player_list_label = Label(text='ESPN Top 200 Players:')
        self.player_list_label.grid(row=0, column=0, columnspan=4, sticky=W, padx=20, pady=5)
        self.rank_list_label = Label(text='Players you want ordered by preference (drag & drop):')
        self.rank_list_label.grid(row=0, column=6, columnspan=4, sticky=W, padx=20, pady=5)
        self.draft_count_label = Label(text='Number of simulations:')
        self.draft_count_label.grid(row=4, column=8, sticky=W, padx=5)
        self.draft_count = Entry()
        self.draft_count.grid(row=5, column=8, sticky=W, padx=5)
        self.pick_order_label = Label(text='Which pick in the draft?')
        self.pick_order_label.grid(row=6, column=8, sticky=W, padx=5)
        self.pick_order = Entry()
        self.pick_order.grid(row=7, column=8, sticky=W, padx=5)
        self.results_list_label = Label(text='Draft Simulation Results:')
        self.results_list_label.grid(row=12, column=0, sticky=W, padx=20)

        # lists of players and scrollbar
        self.player_list = Listbox(selectmode=MULTIPLE, activestyle='none')
        self.player_list.grid(row=2, column=0, rowspan=10, columnspan=5, sticky=N + E + W + S, ipadx=80, ipady=50,
                              padx=20, pady=5)
        self.user_player_list = Listbox(selectmode=SINGLE, activestyle='none')
        self.user_player_list.grid(row=1, column=6, rowspan=10, columnspan=2, sticky=N + E + W + S, ipadx=80, ipady=50,
                                   padx=20, pady=5)
        self.results_list = Listbox(activestyle='none', font='Monaco')
        self.results_list.grid(row=14, column=0, rowspan=7, columnspan=10, sticky=E + W, ipady=100, padx=20, pady=5)
        self.left_scrollbar = Scrollbar(self.player_list, orien='vertical', command=self.player_list.yview)
        self.player_list.configure(yscrollcommand=self.left_scrollbar.set)
        self.left_scrollbar.pack(side=LEFT, fill=Y)

        # search bar
        self.search_label = Label(text='Search:')
        self.search_label.grid(row=1, column=0, sticky=W, padx=20)

        self.search_var = StringVar()
        self.search_var.trace("w", self.update_list_search)
        self.search_bar = Entry(textvariable=self.search_var)
        self.search_bar.grid(row=1, column=0, sticky=W, padx=70)

        # position dropdown
        self.drop_down = StringVar()
        positions = ['All', 'QB', 'RB', 'WR', 'TE', 'FLEX', 'DST']
        self.drop_down.set('All')
        self.drop_down_menu = OptionMenu(master, self.drop_down, *positions)
        self.drop_down_menu.grid(row=1, column=0, sticky=E)
        self.drop_down.trace("w", self.update_list_dropdown)

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
        self.send_button.grid(row=3, column=5, sticky=E + W)
        self.send_button = Button(text='Deselect All', command=self.deselect_all)
        self.send_button.grid(row=4, column=5, sticky=E + W)
        self.send_button = Button(text='>', command=self.choose_players)
        self.send_button.grid(row=5, column=5, sticky=E + W)
        self.send_button = Button(text='<', command=self.remove_player)
        self.send_button.grid(row=6, column=5, sticky=E + W)
        self.send_button = Button(text='<<', command=self.remove_all)
        self.send_button.grid(row=7, column=5, sticky=E + W)
        self.random_checkbox = ttk.Checkbutton(text='Random')
        self.random_checkbox.grid(row=7, column=9, sticky=W, padx=10)
        self.random_checkbox.state(['!alternate'])
        self.draft_button = Button(text='Draft!', command=self.simulate_draft)
        self.draft_button.grid(row=12, column=8, sticky=E + W, pady=10)

        # sliders
        self.team_count_label = Label(text='Number of teams:')
        self.team_count_label.grid(row=2, column=8, sticky=W, padx=5)
        self.team_count = Scale(from_=6, to=14, orient=HORIZONTAL)
        self.team_count.grid(row=3, column=8, sticky=W, padx=5)
        self.team_count.set(10)

        self.round_label = Label(text='Number of rounds per draft:')
        self.round_label.grid(row=8, column=8, sticky=S+E+W)
        self.round_count = Scale(from_=1, to=16, orient=HORIZONTAL)
        self.round_count.grid(row=9, column=8, sticky=N+E+W)
        self.round_count.set(16)

        # menu
        menu = Menu(root)
        root.config(menu=menu)

        file_menu = Menu(menu)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Import Players...', command=self.import_players)
        file_menu.add_command(label='Save As...', command=self.save_players)
        file_menu.add_command(label='Reset All', command=self.reset_all)
        file_menu.add_command(label="Quit", command=root.quit)
        helpmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About DraftSimulator", command=self.about_draft_simulator)

        for i in range(len(top300List)):
            self.player_list.insert(END, '       ' + str(top300List[i]) + '   ' + str(top300Positions[i]))

    # functions for GUI
    def update_list_search(self, *args):
        full_list = ['       ' + str(top300List[i]) + '   ' + str(top300Positions[i]) for i in range(len(top300List))]
        search_term = self.search_var.get()
        self.player_list.delete(0, END)
        for item in full_list:
            if search_term.lower() in item.lower():
                self.player_list.insert(END, item)

    def update_list_dropdown(self, *args):
        full_list = ['       ' + str(top300List[i]) + '   ' + str(top300Positions[i]) for i in range(len(top300List))]
        pos = self.drop_down.get()
        self.player_list.delete(0, END)
        if pos == 'All':
            for item in full_list:
                self.player_list.insert(END, item)
        elif pos == 'FLEX':
            for item in full_list:
                if item.endswith('RB') or item.endswith('WR') or item.endswith('TE'):
                    self.player_list.insert(END, item)
        else:
            for item in full_list:
                if item.endswith(pos):
                    self.player_list.insert(END, item)

    def choose_players(self):
        selected_players = self.player_list.curselection()
        for i in selected_players:
            if top300List[i] not in self.user_player_list.get(0, END):
                self.user_player_list.insert(END, str(top300List[i]))
                user_dict.update({top300List[i]: top300Positions[i]})

    def remove_player(self):
        selected_players = self.user_player_list.curselection()
        self.user_player_list.delete(selected_players)
        selection_list = [key for key in user_dict.keys()]
        for i in selected_players:
            del user_dict[selection_list[i]]

    def remove_all(self):
        self.user_player_list.delete(0, END)
        user_dict.clear()

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

    def save_players(self):
        if len(self.user_player_list.get(0, END)) > 0:
            f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        else:
            messagebox.showinfo('Error', 'Please select players before saving.')
            return
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        user_player_list = str([player for player in self.user_player_list.get(0, END)])
        f.write(user_player_list)
        f.close()

    def import_players(self):
        filename = filedialog.askopenfilename(parent=root, filetypes=[("Text files", "*.txt")])
        try:
            f = open(filename)
            file_text = str(f.read().split(', "'))
            imported_list_str = file_text[3:-3].replace("'", "").replace(", ", ",")
            imported_list = imported_list_str.split(',')
            for player in imported_list:
                if player not in self.user_player_list.get(0, END):
                    self.user_player_list.insert(END, str(player))
                    user_dict.update({player: top300dict.get(player)})
        except FileNotFoundError:
            return

    def about_draft_simulator(self):
        messagebox.showinfo('Welcome!',
                            'Ever wondered how likely you are to get that fantasy stud or sleeper?  '
                            'DraftSimulator is the tool that will give you the edge for your upcoming fantasy draft!'
                            '\n \n'
                            'Follow these easy steps to get started:'
                            '\n \n'
                            u'\u2022 First, select a group of players that you really want on your team.'
                            '\n \n'
                            u'\u2022 Next, rearrange them in order of preference by clicking and dragging.'
                            '\n \n'
                            u'\u2022 Finally, select your desired draft parameters, and click Draft!'
                            '\n \n'
                            "Your draft results will appear in the results box at the bottom, and will display "
                            "how often you were able to draft each player throughout the simulation.  "
                            "Look for the player names in red -- these are the ones you wanted!"
                            "\n \n"
                            "You can also save your player list and import it later!  Use File > Save and File > Import"
                            " accordingly.")

    # draft function
    def simulate_draft(self):
        self.results_list.delete(0, END)

        try:
            team_count = int(self.team_count.get())
        except ValueError:
            messagebox.showinfo('Error', 'Please specify the number of teams in your draft.')
            return
        if team_count < 8 or team_count > 12:
            messagebox.showinfo('Stop', 'Number of teams must be between 8 and 12. Try again.')
            return

        try:
            draft_count = int(self.draft_count.get())
        except ValueError:
            messagebox.showinfo('Error', 'Please specify the number of simulations.')
            return
        if draft_count > 10000:
            messagebox.showinfo('Stop', 'Maximum of 10000 simulations allowed.')
            return

        try:
            pick_order = int(self.pick_order.get())
        except ValueError:
            if self.random_checkbox.instate(['selected']):
                pick_order = 0
            else:
                messagebox.showinfo('Error', 'Please specify your desired draft pick, or else select Random.')
                return
        if pick_order > team_count:
            messagebox.showinfo('Stop', 'Pick selection exceeds number of teams.')
            return

        team_dict = {}
        user_team = []
        for i in range(team_count - 1):
            n = i + 2
            team_dict['team_%s' % n] = []
        team_dict.update({'user_team': user_team})

        # determine draft order if not random
        draft_order = [team for team in team_dict.keys()]
        if self.random_checkbox.instate(['']):
            user_pick = draft_order.index('user_team')
            draft_order[user_pick], draft_order[pick_order - 1] = draft_order[pick_order - 1], draft_order[
                user_pick]
        user_draft_pick = draft_order.index('user_team')

        rounds_drafted = self.slider.get()

        # run simulation as many times as user specifies
        for _ in range(draft_count):
            # draft starts here
            print('The draft is live!')

            # making player lists you and AI will draft from
            user_list = [i for i in self.user_player_list.get(0, END)]
            comp_list = [key for key in top300dict.keys()]

            # reset your team
            user_team = []

            # reset team dict
            team_dict.clear()
            for i in range(team_count - 1):
                n = i + 2
                team_dict['team_%s' % n] = []
            team_dict.update({'user_team': user_team})

            # randomize draft order if selected
            if self.random_checkbox.instate(['selected']):
                random.shuffle(draft_order)

            draft_round = 0
            threshold = 2

            while any([len(team) < rounds_drafted for team in team_dict.values()]):
                for team in draft_order:
                    if team == 'user_team':  # your pick logic
                        if user_list:
                            while not valid_choice(user_list[0], user_team):
                                user_list.remove(user_list[0])
                            your_pick = user_list[0]
                            user_list.remove(your_pick)
                        else:
                            your_threshold = threshold
                            your_pick = None
                            while not valid_choice(your_pick, user_team):
                                your_pick = comp_list[random.randint(0, your_threshold)]
                                your_threshold += 1
                        user_team.append(your_pick)
                        comp_list.remove(your_pick)
                    else:  # AI pick logic
                        comp_threshold = threshold
                        comp_pick = None
                        while not valid_choice(comp_pick, team_dict.get(team)):
                            comp_pick = comp_list[random.randint(0, comp_threshold)]
                            comp_threshold += 1
                        team_dict.get(team).append(comp_pick)
                        if comp_pick in user_list:
                            user_list.remove(comp_pick)
                        comp_list.remove(comp_pick)
                draft_order = draft_order[::-1]  # reverses the draft order for every other round
                if draft_round % 2 == 0:
                    threshold += 1  # makes the AI choose from a larger pool of players every other round
                draft_round += 1  # moves on to the next round
            print('Your Team: ' + str(user_team))
            userDraftPicks.append(user_team)
            print('\n')

        # aggregate simulation data for output
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
        self.results_list.insert(END, '    Name              Position          Draft Frequency')
        self.results_list.insert(END, '-' * 55)
        # print results and make it look pretty
        for key, value in sorted(draft_frequency.items(), key=lambda x: x[1], reverse=True):
            key_string = key[:21] + ' ' * (25 - len(str(key[:21])))
            if top300dict.get(key) == 'DST':
                position_string = top300dict.get(key) + ' ' * 16
            elif top300dict.get(key) == 'K':
                position_string = top300dict.get(key) + ' ' * 18
            else:
                position_string = top300dict.get(key) + ' ' * 17
            self.results_list.insert(END, key_string + position_string + str(round((100.0 * value), 2)) + '%')
            if key in self.user_player_list.get(0, END):
                self.results_list.itemconfig(END, {'fg': 'red'})
        self.results_list.insert(END, '\n' '\n')
        userDraftPicks.clear()
        user_draft_picks_final.clear()
        draft_frequency.clear()
        messagebox.showinfo('Nice.', 'Your drafts are complete.')


root = Tk()
ds = draftSimulator(root)
root.mainloop()
