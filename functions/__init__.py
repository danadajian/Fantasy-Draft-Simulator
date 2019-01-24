import statistics as s

# defines function that finds all string indices of a substring
def findAll(string, substring, indexList):
    index = -1
    while True:
        index = string.find(substring, index + 1)
        if index == -1:
            break
        indexList.append(index)


# defines function that finds the nth index of a substring
def findstat(haystack, needle, n):
    statIndex = haystack.find(needle)
    i = 1
    while i < n:
        statIndex = haystack.find(needle, statIndex + len(needle))
        i += 1
    lower = statIndex + len(needle)
    upper = haystack.find('<', lower)
    return haystack[lower: upper]


# define functions that find max, min, avg, and std of list, ignoring weird entries
def getmax(yourList):
    newList = []
    for item in yourList:
        if item != '--' and item is not None:
            newList.append(item)
    newList = map(float, newList)
    try:
        return max(newList)
    except ValueError:
        return 0


def getmin(yourList):
    newList = []
    for item in yourList:
        if item != '--' and item is not None:
            newList.append(item)
    newList = map(float, newList)
    try:
        return min(newList)
    except ValueError:
        return 0


def getavg(yourList):
    newList = []
    for item in yourList:
        if item != '--' and item is not None:
            newList.append(item)
    newList = map(float, newList)
    try:
        return s.mean(newList)
    except ValueError:
        return 0


def getstd(yourList):
    newList = []
    for item in yourList:
        if item != '--' and item is not None:
            newList.append(item)
    newList = map(float, newList)
    try:
        return round(s.stdev(newList), 1)
    except ValueError:
        return 0
