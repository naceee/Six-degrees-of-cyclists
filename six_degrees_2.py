from urllib.request import urlopen

class Graph():

    def __init__(self):
        self.ridersDict = dict()
        self.ridersObjects = []

    def addTeam(self, riders):
        ids = []
        for r in riders:
            if r in self.ridersDict:
                ids.append(self.ridersDict[r])
            else:
                l = len(self.ridersDict)
                ids.append(l)
                self.ridersDict[r] = l
                self.ridersObjects.append(Rider(r))

        for i in range(len(riders)):
            for j in range(len(riders)):
                self.ridersObjects[ids[i]].addTeammates(ids[j], self.ridersObjects[ids[j]])

    def printResults(self):
        for r in self.ridersObjects:
            print(r.name, r.number)


    def resetNumbers(self):
        for rider in self.ridersObjects:
            rider.number = 69
            rider.via = None

    def numberBetween2riders(self, riderId1, riderId2):
        self.ridersObjects[riderId1].count(0)
        n = self.ridersObjects[riderId2].number
        
        r = self.ridersObjects[riderId2]
        path = [r.name]
        while r != self.ridersObjects[riderId1]:
            r = r.via
            path.append(r.name)

        self.resetNumbers()
        return (n, path)

class Rider():

    def __init__(self, name):
        self.name = name
        self.teammateIds = set()
        self.teammates = []
        self.number = 69
        self.via = None

    def addTeammates(self, mateId, mateObject):
        if not mateId in self.teammateIds:
            self.teammateIds.add(mateId)
            self.teammates.append(mateObject)

    def printRider(self):
        print(self.name)
        for mate in self.teammates:
            print("  ", mate.name)

    def count(self, num):
        self.number = num
        num += 1
        update = []
        for mate in self.teammates:
            if mate.number > num:
                mate.number = num
                mate.via = self
                update.append(mate)

        for mate in update:
            mate.count(num)



def getTeamIds(year):
    url = 'https://firstcycling.com/team.php?d=1&y=' + str(year)
    page = urlopen(url)
    html = page.read().decode("utf-8")
    #print(html)
    ids = []
    start = html.find('<tbody>')
    while start != -1:
        start = html.find('<a href="team.php?', start+1)
        teamId = html[start+20:start+26]
        for i in range(len(teamId), 1, -1):
            if teamId[0:i].isnumeric():
                ids.append(teamId[0:i])
                break
    return ids

def getRidersNames(teamId):
    url = 'https://firstcycling.com/team.php?l=' + str(teamId) + '&riders=1#team'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    #print(html)
    riders = []
    start = 1
    while start != -1:
        start = html.find('<a href="rider.php?r=', start+1)
        if start == -1:
            break
        start = html.find('>', start+1)
        stop = html.find('</a>', start)
        rider = html[start+8:stop-6]
        riders.append(rider)
        start = stop
    return riders

def writeToDatabase(yearFrom, yearTo):
    fileName = 'database' + str(YEAR_FROM) + '-' + str(YEAR_TO) + '.txt'
    print(fileName)
    f = open(fileName, 'w')


    for i in range(YEAR_FROM, (YEAR_TO+1)):
        print('year', i)
        ids = getTeamIds(i)

        for teamId in ids:
            names = getRidersNames(teamId)
            for name in names:
                f.write(name + '\n')
            f.write('\n')

    f.close() 
    print('data downloaded and saved in', fileName) 


def createGraph(fileName):
    f = open(fileName, 'r')
    g = Graph()

    team = []
    for line in f:
        if line == '\n':
            g.addTeam(team)
            team.clear()
        else:
            team.append(line.rstrip())

    print('Number of riders in database:', len(g.ridersDict))
    return g



# write to database

YEAR_FROM = 1960
YEAR_TO = 2021 #included
fileName = 'database' + str(YEAR_FROM) + '-' + str(YEAR_TO) + '.txt'

#writeToDatabase(YEAR_FROM, YEAR_TO)


g = createGraph(fileName)
allNames = g.ridersDict.keys()

print('hello dear cycling fan!')
print()
while True:
    print('input complete name of a first cyclist')
    rider1 = input()
    while rider1 not in g.ridersDict:
        print('there is no cyclist named "' + rider1 + '" in my database. Check if you misspeled his name.')
        riderSplit = rider1.split(' ')
        for name in allNames:
            nameSplit = name.split(' ')
            for r in riderSplit:
                for n in nameSplit:
                    if n == r:
                         print(' * maybe try searching ' + name + '?')
        rider1 = input()        

    print('input complete name of a second cyclist')
    rider2 = input()
    while rider2 not in g.ridersDict:
        print('there is no cyclist named "' + rider2 + '" in my database. Check if you misspeled his name.')
        riderSplit = rider2.split(' ')
        for name in allNames:
            nameSplit = name.split(' ')
            for r in riderSplit:
                for n in nameSplit:
                    if n == r:
                        print(' * maybe try searching ' + name + '?')
        rider2 = input()       

    riderId1 = g.ridersDict[rider1]
    riderId2 = g.ridersDict[rider2]

    connection = g.numberBetween2riders(riderId1, riderId2)
    print(rider1 + ' number of ' + rider2 + ' is ' + str(connection[0]) + ':')
    for i in range(len(connection[1])-1):
        print(' *', connection[1][i], 'was teammate with', connection[1][i+1])

    print('Do you want to check another pair of cyclists? (y/n)')
    ans = input()
    if ans == 'y' or ans == 'yes' or ans == 'Y' or ans == 'Yes':
        g.resetNumbers()
        print('\n\n')
    else: 
        break
        




    