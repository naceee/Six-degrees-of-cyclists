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

        #for i in range(len(riders)):
        #    print(riders[i], ids[i])

        for i in range(len(riders)):
            for j in range(len(riders)):
                self.ridersObjects[ids[i]].addTeammates(ids[j], self.ridersObjects[ids[j]])

    def printResults(self):
        for r in self.ridersObjects:
            print(r.name, r.number)


    def updateNumbers(self):
        for rider in self.ridersObjects:
            rider.number = 69

    def numberBetween2riders(self, riderId1, riderId2):
        self.ridersObjects[riderId1].count(0)
        n = self.ridersObjects[riderId2].number
        self.updateNumbers()
        return n

class Rider():

    def __init__(self, name):
        self.name = name
        self.teammateIds = set()
        self.teammates = []
        self.number = 69

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
        print(i)
        ids = getTeamIds(i)

        for teamId in ids:
            names = getRidersNames(teamId)
            for name in names:
                f.write(name + '\n')
            f.write('\n')

    f.close()  



# write to database

YEAR_FROM = 2000
YEAR_TO = 2021 #included

#writeToDatabase(YEAR_FROM, YEAR_TO)


# read from database, create graph and connections 

fileName = 'database' + str(YEAR_FROM) + '-' + str(YEAR_TO) + '.txt'
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

id1 = g.ridersDict["Romain Bardet"]
id2 = g.ridersDict["Ivan Sosa"]

n = g.numberBetween2riders(id1, id2)
print(n)







