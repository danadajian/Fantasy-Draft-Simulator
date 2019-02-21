import requests
from bs4 import BeautifulSoup

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
