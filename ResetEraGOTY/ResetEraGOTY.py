# Import Libraries
import urllib.request
from bs4 import BeautifulSoup
import sqlite3, csv

length = 0

# Define variables
allVotes = [[] for i in range(2000)]
userTotal = []
finalTally = [[] for i in range(500)]
tempVote = [0] * 2
userVote = 0
userNum = 0
gameNum = 0
voted = False
doesExist = False
results = open("results.txt","w")
place = ["runnerup", "tenth", "ninth", "eighth", "seventh", "sixth", "fifth", "fourth", "third", "second", "first"]

# Request Webpage
req = urllib.request.Request(
    'https://www.resetera.com/threads/mafia-ot-make-friends-through-murders-sign-up-inside.18/page-24', 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)
f = urllib.request.urlopen(req)

# Store page in variable
era_page = BeautifulSoup(f, 'html.parser')
f.close()

# Find out how many pages there are
pages = era_page.find("span", {"class" : "pageNavHeader"})
nav = pages.contents[0].split(" ")
numPages = int(nav[3])

thread = "https://www.resetera.com/threads/mafia-ot-make-friends-through-murders-sign-up-inside.18/"

for p in range(24, 25):
    thread2 = thread + "page-" + str(p)
    print(thread2)
    req = urllib.request.Request(thread2, data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    f = urllib.request.urlopen(req)
    # Collect posts/list items
    era_page = BeautifulSoup(f, 'html.parser')
    f.close()
    posts = era_page.find_all("div", {"class" : "messageContent"})
    for post in posts:
        hasQuote = post.find("div")
        if not hasQuote is None: # Skips quoted posts
            hasQuote.extract()
        post.append(post.get_text(strip=True))
        lists = post.find_all("li")
    # Store votes in userTotal, then put userTotal as a list item in allVotes
        for list in lists:
            bold = list.find("b")
            if(bold is not None):
                print(bold.contents[0])
                userTotal.append(bold.contents[0])
        for i in range(len(userTotal)):
            allVotes[userNum].append(userTotal[i])
        if(allVotes[userNum]!=[]):
           userNum += 1
        userTotal = []
# end for loop

# Tally the votes
for i in range(0, userNum):
    for j in range(len(allVotes[i])):
        for x in range(len(finalTally)):
            if allVotes[i][j] in finalTally[x]:
                finalTally[x][1] += (10 - j)
                doesExist = True #Game was found in the list already, will bypass the following
        if not doesExist: # Adds game to list if not found already
            tempVote[0] = allVotes[i][j]
            tempVote[1] = (10-j)
            finalTally[gameNum].append(tempVote[0])
            finalTally[gameNum].append(tempVote[1])
            gameNum += 1
    doesExist = False


list2 = [x for x in finalTally if x != []]

def getKey(item):
    return item[1]

final = sorted(list2, key = getKey, reverse=True)

for j in range(gameNum):
    r = str(final[j][0])
    results.write(r)
    results.write(" - ")
    s = str(final[j][1])
    results.write(s)
    results.write("\n")

# End Vote Collection
# Begin Tallying

def loadGamesList():
    global length
    con = sqlite3.connect("goty.db")
    con.text_factory = str
    c = con.cursor()
    c.executescript("""DROP TABLE IF EXISTS gameslist; CREATE TABLE gameslist (num INTEGER, title TEXT, platform TEXT, publisher TEXT, genre TEXT, points INTEGER, first INTEGER, second INTEGER, third INTEGER, fourth INTEGER, fifth INTEGER, sixth INTEGER, seventh INTEGER, eighth INTEGER, ninth INTEGER, tenth INTEGER, runnerup INTEGER, PRIMARY KEY (num));""")
    with open('gameslist.csv', 'rb') as f:
        dr = csv.DictReader(f)
        to_db = [(i['Game Number'], i['Title'], i['Platform'], i['Publisher'], 
                i['Genre'], i['Points'], i['First'], i['Second'], i['Third'], 
                i['Fourth'], i['Fifth'], i['Sixth'], i['Seventh'], i['Eighth'], 
                i['Ninth'], i['Tenth'], i['Runner Up']) for i in dr]
        length = len(to_db)

    c.executemany("INSERT INTO gameslist (num, title, platform, publisher, genre, points, first, "
        + "second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, runnerup) VALUES "
        + "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    con.commit()
    c.close()
    con.close()

def updatePoints(title, points, rank):
    global length
    query1 = 'SELECT * FROM gameslist WHERE title = \"%s\";' % (title)

    con = sqlite3.connect("goty.db")
    con.row_factory = sqlite3.Row
    c = con.cursor()
    c.execute(query1)
    row = c.fetchone()

    if row is None:
        print ("Inserting " + title)
        length = length + 1
        query3 = "INSERT INTO gameslist (num, title, platform, publisher, genre, points, first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, runnerup) VALUES (%i, '%s', 'PC', 'Other', 'Action', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);" % (length, title)
        c.execute(query3)
        c.execute(query1)
        row = c.fetchone()

    points = row["points"] + points
    addRank = row[rank] + 1
    p = str(points)
    r = str(addRank)

    query2 = 'UPDATE gameslist SET points = %s, %s = %s WHERE title = \"%s\";' % (p, rank, r, title)
    c.execute(query2)

    # test
    c.execute(query1)
    row = c.fetchone()

    con.commit()
    c.close()
    con.close()

def getGOTY():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre NOT LIKE '%Remake%' ORDER BY points DESC LIMIT 20;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getFullList():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute('SELECT * FROM gameslist ORDER BY points DESC;')
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestPCGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%PC%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestPS4Game():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%PS4%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestXBOGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%XBO%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestNSWGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%NSW%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBest3DSGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%3DS%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestVITAGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%VITA%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestMobileGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%iOS%' OR platform LIKE 'AND' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestActionGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Action%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestActionAdventureGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Action-Adventure%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestAdventureGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Adventure%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestRPGGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%RPG%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestShooterGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Shooter%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestRacingGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Racing%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestSportsGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Sports%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestStrategyGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Strategy%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestFightingGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Fighting%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestPuzzleGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Puzzle%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestVRGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%VR%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestRemakeGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Remake%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getFanFavorite():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, first FROM gameslist ORDER BY first DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def testUpdatePoints():
    loadGamesList()
    updatePoints('The Legend of Zelda: Breath of the Wild', 10, 'first')
    updatePoints('Super Mario Odyssey', 9, 'second')
    updatePoints("PLAYERUNKNOWN'S BATTLEGROUNDS", 8, 'third')
    updatePoints('Persona 5', 7, 'fourth')
    updatePoints('Night In The Woods', 6, 'fifth')
    updatePoints('Horizon: Zero Dawn', 5, 'sixth')
    updatePoints('Mass Effect: Andromeda', 4, 'seventh')
    updatePoints('Cuphead', 3, 'eighth')
    updatePoints('Wolfenstein II: The New Colossus', 2, 'ninth')
    updatePoints('Destiny 2', 1, 'tenth')
    updatePoints('Star Wars Battlefront II', 0, 'runnerup')
    getGOTY();

def testUpdatePointsWithRemakeVote():
    loadGamesList()
    updatePoints('The Legend of Zelda: Breath of the Wild', 10, 'first')
    updatePoints('Super Mario Odyssey', 9, 'second')
    updatePoints("PLAYERUNKNOWN'S BATTLEGROUNDS", 8, 'third')
    updatePoints('Persona 5', 7, 'fourth')
    updatePoints('Mario Kart 8 Deluxe', 6, 'fifth')
    updatePoints('Horizon: Zero Dawn', 5, 'sixth')
    updatePoints('Mass Effect: Andromeda', 4, 'seventh')
    updatePoints('Cuphead', 3, 'eighth')
    updatePoints('Wolfenstein II: The New Colossus', 2, 'ninth')
    updatePoints('Destiny 2', 1, 'tenth')
    updatePoints('Star Wars Battlefront II', 0, 'runnerup')
    getGOTY();

def testUpdatePointsWithNewGames():
    loadGamesList()
    updatePoints('The Legend of Zelda: Breath of the Wild', 10, 'first')
    updatePoints('Super Mario Odyssey', 9, 'second')
    updatePoints("PLAYERUNKNOWN'S BATTLEGROUNDS", 8, 'third')
    updatePoints('Persona 5', 7, 'fourth')
    updatePoints('Test Game', 6, 'fifth')
    updatePoints('Horizon: Zero Dawn', 5, 'sixth')
    updatePoints('Mass Effect: Andromeda', 4, 'seventh')
    updatePoints('Cuphead', 3, 'eighth')
    updatePoints('Wolfenstein II: The New Colossus', 2, 'ninth')
    updatePoints('Destiny 2', 1, 'tenth')
    updatePoints('Star Wars Battlefront II', 0, 'runnerup')
    getGOTY();

def testGetPCGame():
    loadGamesList()
    updatePoints('Divinity: Original Sin II', 10, 'first')
    updatePoints('Super Mario Odyssey', 9, 'second')
    updatePoints("PLAYERUNKNOWN'S BATTLEGROUNDS", 8, 'third')
    updatePoints('Persona 5', 7, 'fourth')
    updatePoints('Test Game', 6, 'fifth')
    updatePoints('Horizon: Zero Dawn', 5, 'sixth')
    updatePoints('Mass Effect: Andromeda', 4, 'seventh')
    updatePoints('Cuphead', 3, 'eighth')
    updatePoints('Wolfenstein II: The New Colossus', 2, 'ninth')
    updatePoints('Destiny 2', 1, 'tenth')
    updatePoints('Star Wars Battlefront II', 0, 'runnerup')
    getBestPCGame();

def testGetPS4Game():
    loadGamesList()
    updatePoints('Divinity: Original Sin II', 10, 'first')
    updatePoints('Super Mario Odyssey', 9, 'second')
    updatePoints("PLAYERUNKNOWN'S BATTLEGROUNDS", 8, 'third')
    updatePoints('Persona 5', 7, 'fourth')
    updatePoints('Test Game', 6, 'fifth')
    updatePoints('Horizon: Zero Dawn', 5, 'sixth')
    updatePoints('Mass Effect: Andromeda', 4, 'seventh')
    updatePoints('Cuphead', 3, 'eighth')
    updatePoints('Wolfenstein II: The New Colossus', 2, 'ninth')
    updatePoints('Destiny 2', 1, 'tenth')
    updatePoints('Star Wars Battlefront II', 0, 'runnerup')
    getBestPS4Game();

def testGetXBOGame():
    loadGamesList()
    updatePoints('Divinity: Original Sin II', 10, 'first')
    updatePoints('Super Mario Odyssey', 9, 'second')
    updatePoints("PLAYERUNKNOWN'S BATTLEGROUNDS", 8, 'third')
    updatePoints('Persona 5', 7, 'fourth')
    updatePoints('Test Game', 6, 'fifth')
    updatePoints('Horizon: Zero Dawn', 5, 'sixth')
    updatePoints('Mass Effect: Andromeda', 4, 'seventh')
    updatePoints('Cuphead', 3, 'eighth')
    updatePoints('Wolfenstein II: The New Colossus', 2, 'ninth')
    updatePoints('Destiny 2', 1, 'tenth')
    updatePoints('Star Wars Battlefront II', 0, 'runnerup')
    getBestXBOGame();

def testGetNSWGame():
    loadGamesList()
    updatePoints('Divinity: Original Sin II', 10, 'first')
    updatePoints('Super Mario Odyssey', 9, 'second')
    updatePoints("PLAYERUNKNOWN'S BATTLEGROUNDS", 8, 'third')
    updatePoints('Persona 5', 7, 'fourth')
    updatePoints('Test Game', 6, 'fifth')
    updatePoints('Horizon: Zero Dawn', 5, 'sixth')
    updatePoints('Mass Effect: Andromeda', 4, 'seventh')
    updatePoints('Cuphead', 3, 'eighth')
    updatePoints('Wolfenstein II: The New Colossus', 2, 'ninth')
    updatePoints('Destiny 2', 1, 'tenth')
    updatePoints('Star Wars Battlefront II', 0, 'runnerup')
    getBestNSWGame();

#testUpdatePoints()
#testUpdatePointsWithRemakeVote()
#testUpdatePointsWithNewGames()
testGetPCGame()
testGetPS4Game()
testGetXBOGame()
testGetNSWGame()

for x in range(len(final)):
    title = final[x][0]
    points = final[x][1]
    rank = place[points]
    if (place[points]<=0):
        rank = place[0]
    updatePoints(title, points, rank)
