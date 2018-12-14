import requests
from bs4 import BeautifulSoup

playerCount = 0
for week in range(17):
    print('Week ' + str(week + 1) + ' Stats:')
    playerCount = 0
    while playerCount <= 250:
        session = requests.session()
        url = 'http://games.espn.com/ffl/leaders?&scoringPeriodId=' + str(week + 1) + '&seasonId=2018&startIndex=' + str(playerCount)
        req = session.get(url)
        doc = BeautifulSoup(req.content, 'html.parser')
        text = str(doc.get_text)

        locationList = []
        def findAll(string, substring):
            index = -1
            while True:
                index = string.find(substring, index + 1)
                if index == -1:
                    break
                locationList.append(index)

        findAll(text, 'teamid="-2147483648">')

        stringList = []
        pointsList = []

        for location in locationList:
            playerLowerIndex = location + len('teamid="-2147483648">')
            playerMiddleIndex = text.find('<', playerLowerIndex)
            playerUpperIndex = text.find('<', playerMiddleIndex + 1)
            player = text[playerLowerIndex:playerUpperIndex]
            if not player.startswith('<img'):
                stringList.append(player)
                pointsLowerIndex = text.find('appliedPoints appliedPointsProGameFinal', playerUpperIndex) + len('appliedPoints appliedPointsProGameFinal') + 2
                pointsUpperIndex = text.find('<', pointsLowerIndex)
                points = text[pointsLowerIndex:pointsUpperIndex]
                if text.find('playertableStat appliedPoints">--<', playerUpperIndex, pointsUpperIndex) != -1 or points.startswith('HTML PUBLIC'):
                    points = '--'
                pointsList.append(points)

        playerList = []
        positionList = []

        for player in stringList:
            playerList.append(player[:player.find('<')])
            positionHalf = player[player.find('</a>'):]
            if 'QB' in positionHalf and 'FA' not in positionHalf:
                positionList.append('QB')
            elif 'RB' in positionHalf and 'FA' not in positionHalf:
                positionList.append('RB')
            elif 'WR' in positionHalf and 'FA' not in positionHalf:
                positionList.append('WR')
            elif 'TE' in positionHalf and 'FA' not in positionHalf:
                positionList.append('TE')
            elif 'K' in positionHalf and 'FA' not in positionHalf:
                positionList.append('K')
            elif 'D/ST' in positionHalf and 'FA' not in positionHalf:
                positionList.append('D/ST')

        playersAndPositions = dict(zip(playerList, positionList))
        print(playersAndPositions)

        playersAndPoints = dict(zip(playerList, pointsList))
        print(playersAndPoints)

        playerCount += 50
    print('\n')
