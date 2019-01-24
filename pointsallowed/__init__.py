import requests
from bs4 import BeautifulSoup
from getstats import find_all

# get fantasy points allowed by position
pointsAllowedDictList = []
positions = [1, 2, 3, 4, 5, 16]
for position in positions:
    # make http request to ESPN for full page html
    teamSession = requests.session()
    teamUrl = 'http://games.espn.com/ffl/pointsagainst?positionId=' + str(position)
    teamReq = teamSession.get(teamUrl)
    teamDoc = BeautifulSoup(teamReq.content, 'html.parser')
    teamText = str(teamDoc.get_text)

    # find instance of substring to denote locations of all team names on page
    teamIndexList = []
    find_all(teamText, 'href="" instance="_ppc">', teamIndexList)

    teamList = []
    pointsAllowedList = []
    # add teams and points allowed for each team in html
    for index in teamIndexList:
        teamLowerIndex = index + len('href="" instance="_ppc">')
        teamUpperIndex = teamText.find('<', teamLowerIndex)
        team = teamText[teamLowerIndex: teamUpperIndex]
        teamList.append(team)
        pointsAllowedLowerIndex = teamText.find('"playertableStat appliedPoints">', teamUpperIndex) + len(
            '"playertableStat appliedPoints">')
        pointsAllowedUpperIndex = teamText.find('<', pointsAllowedLowerIndex)
        if teamText[pointsAllowedLowerIndex: pointsAllowedUpperIndex] != '--':
            pointsAllowed = float(teamText[pointsAllowedLowerIndex: pointsAllowedUpperIndex])
            pointsAllowedList.append(pointsAllowed)
    # add teams and points allowed to dictionaries
    teamsAndPointsAllowed = dict(zip(teamList, pointsAllowedList))
    pointsAllowedDictList.append(teamsAndPointsAllowed)
