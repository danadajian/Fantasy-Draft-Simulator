import requests
from bs4 import BeautifulSoup
from getstats import find_all, weeks

# define dictionary containing useful info about all 32 teams
teamNames = {'Arizona': 'Cardinals', 'Atlanta': 'Falcons', 'Baltimore': 'Ravens', 'Buffalo': 'Bills',
             'Carolina': 'Panthers', 'Chicago': 'Bears', 'Cincinnati': 'Bengals', 'Cleveland': 'Browns',
             'Dallas': 'Cowboys', 'Denver': 'Broncos', 'Detroit': 'Lions', 'Green Bay': 'Packers', 'Houston': 'Texans',
             'Indianapolis': 'Colts', 'Jacksonville': 'Jaguars', 'Kansas City': 'Chiefs',
             'Los Angeles': ['Chargers', 'Rams'], 'Miami': 'Dolphins', 'Minnesota': 'Vikings',
             'New England': 'Patriots',
             'New Orleans': 'Saints', 'New York': ['Giants', 'Jets'], 'Oakland': 'Raiders',
             'Philadelphia': 'Eagles', 'Pittsburgh': 'Steelers', 'San Francisco': '49ers', 'Seattle': 'Seahawks',
             'Tampa Bay': 'Buccaneers', 'Tennessee': 'Titans', 'Washington': 'Redskins'}


# define function that determines whether a player is a player or a defense
def player_check(name):
    for city in teamNames.keys():
        # check for NY and LA teams
        if name == 'New York G':
            return 'Giants D/ST'
        elif name == 'New York J':
            return 'Jets D/ST'
        elif name == 'LA Chargers':
            return 'Chargers D/ST'
        elif name == 'LA Rams':
            return 'Rams D/ST'
        else:
            # check for the city and team name in the string
            if city in name:
                team_name = teamNames.get(city)
                return str(team_name) + ' D/ST'
    return name


# set up request to site for both DraftKings and Fanduel salaries
sites = ['dk', 'fd']
siteSalaries = []
for site in sites:
    # make http request to scrape html
    dfsSession = requests.session()
    dfsUrl = 'http://rotoguru1.com/cgi-bin/fyday.pl?week=' + str(weeks + 1) + '&game=' + str(site)
    dfsReq = dfsSession.get(dfsUrl)
    dfsDoc = BeautifulSoup(dfsReq.content, 'html.parser')
    dfsText = str(dfsDoc.get_text)

    # lines containing players & salaries start with that substring
    dfsPlayerIndexList = []
    find_all(dfsText, '--><tr><td><a href="http://rotoguru1.com/cgi-bin/', dfsPlayerIndexList)

    dfsPlayerList = []
    dfsSalaryList = []

    # find string indices of players and salaries and put them in lists
    for index in dfsPlayerIndexList:
        dfsLowerNameIndex = dfsText.find('>', index + len('--><tr><td><a href="http://rotoguru1.com/cgi-bin/')) + 1
        dfsUpperNameIndex = dfsText.find('<', dfsLowerNameIndex)
        dfsLowerSalaryIndex = dfsText.find('<td align="right">', dfsUpperNameIndex) + len('<td align="right">')
        dfsUpperSalaryIndex = dfsText.find('<', dfsLowerSalaryIndex)
        dfsPlayer = dfsText[dfsLowerNameIndex: dfsUpperNameIndex]
        dfsSalaryText = dfsText[dfsLowerSalaryIndex: dfsUpperSalaryIndex]
        if dfsSalaryText == 'N/A':
            continue
        else:
            dfsAmount = dfsSalaryText[1:]
            dfsSalary = int(dfsAmount[:dfsAmount.find(',')] + dfsAmount[dfsAmount.find(',') + 1:])
        dfsSalaryList.append(dfsSalary)
        result = player_check(dfsPlayer)
        if result.endswith('D/ST'):
            dfsPlayerList.append(result)
        else:
            dfsLastNameIndex = dfsText.find(',', dfsLowerNameIndex)
            dfsLastName = dfsText[dfsLowerNameIndex: dfsLastNameIndex]
            dfsFirstName = (dfsText[dfsLastNameIndex + 1: dfsUpperNameIndex])[1:]
            dfsPlayerName = str(dfsFirstName) + ' ' + str(dfsLastName)
            dfsPlayerList.append(dfsPlayerName)

    # put players and salaries into dictionary
    dfsPlayersAndSalaries = dict(zip(dfsPlayerList, dfsSalaryList))
    siteSalaries.append(dfsPlayersAndSalaries)

    # prints accumulated salaries from each site
    print('Acquired ' + str(site) + ' salaries!')
    print(dfsPlayersAndSalaries)

