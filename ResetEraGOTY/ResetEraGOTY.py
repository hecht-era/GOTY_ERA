# Import Libraries
import urllib.request
from bs4 import BeautifulSoup
import sqlite3, csv

#query methods

def getRank(num):
    return {
        0:"first",
        1:"second",
        2:"third",
        3:"fourth",
        4:"fifth",
        5:"sixth",
        6:"seventh",
        7:"eighth",
        8:"ninth",
        9:"tenth",
    }.get(num, "runnerup")

def loadGamesList():
    global length
    con = sqlite3.connect("goty.db")
    con.text_factory = str
    c = con.cursor()
    c.executescript("""DROP TABLE IF EXISTS gameslist; CREATE TABLE gameslist (num INTEGER, title TEXT, platform TEXT, publisher TEXT, genre TEXT, points INTEGER, first INTEGER, second INTEGER, third INTEGER, fourth INTEGER, fifth INTEGER, sixth INTEGER, seventh INTEGER, eighth INTEGER, ninth INTEGER, tenth INTEGER, runnerup INTEGER, PRIMARY KEY (num));""")
    with open('gameslist.csv', 'r') as f:
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
    print("Top 20 Games of 2017\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre NOT LIKE '%Remake%' ORDER BY points DESC LIMIT 20;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getFullList():
    print("Full Results\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute('SELECT * FROM gameslist ORDER BY points DESC;')
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestPCGame():
    print("Best PC Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%PC%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestPS4Game():
    print("Best PS4 Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%PS4%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestXBOGame():
    print("Best Xbox One Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%XBO%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestNSWGame():
    print("Best Nintendo Switch Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%NSW%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBest3DSGame():
    print("Best 3DS Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%3DS%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestVITAGame():
    print("Best Vita Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%VITA%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestMobileGame():
    print("Best Mobile Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%iOS%' OR platform LIKE 'AND' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestActionGame():
    print("Best Action Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Action%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestActionAdventureGame():
    print("Best Action-Adventure Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Action-Adventure%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestAdventureGame():
    print("Best Adventure Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Adventure%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestRPGGame():
    print("Best RPG Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%RPG%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestShooterGame():
    print("Best Shooter Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Shooter%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestRacingGame():
    print("Best Racing Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Racing%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestSportsGame():
    print("Best Sports Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Sports%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestStrategyGame():
    print("Best Strategy Games\n")
    print(Bes)
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Strategy%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestFightingGame():
    print("Best Fighting Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Fighting%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestPuzzleGame():
    print("Best Puzzle Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Puzzle%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestBoardAndCardGame():
    print("Best Puzzle Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Board+Card%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestVRGame():
    print("Best VR Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%VR%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getBestRemakeGame():
    print("Best Remakes")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Remake%' ORDER BY points DESC LIMIT 10;")
    print(c.fetchall())

    con.commit()
    c.close()
    con.close()

def getFanFavorite():
    print("Most Popular Games (Based on most #1 votes)\n")
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

class HashTable:
    size = 16
    num = 0
    table = [None] * size

    def __init__(self, s):
        self.size = s
        self.table = [None] * self.size

    def insert(self, value):
        if self.num >= self.size / 2:
            rebuildTable()

        place = 0
        for i in range(0, len(value)):
            print(value[i])
            place = place + ord(value[i])

        place = place % self.size
        
        while self.table[place] is not None:
            place = place + 1
            if(place >= self.size):
                place = 0
        self.table[place] = value

    def rebuildTable(self):
        self.size = self.size * 2
        newTable = [None] * self.size
        for item in self.table:
            if item is not None:
                place = 0
                for i in range(0, len(value)):
                    place = place + ord(value[i])
                place = place % self.size

                while newTable[place] is not None:
                    place = place + 1
                    if(place >= self.size):
                        place = 0
                newTable[place] = item
        self.table = newTable

    def find(self, value):
        place = 0
        for i in range(0, len(value)):
            place = place + ord(value[i])

        place = place % self.size
        while self.table[place] is not None:
            if self.table[place] == value:
                return True
            place = place + 1
            if(place >= self.size):
                place = 0
        return False



#voting calculations
length = 0
loadGamesList()

voters = HashTable(20)
results = open("results.txt","w")

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
    users = era_page.find_all("a", {"class" : "username"})
    posts = era_page.find_all("div", {"class" : "messageContent"})
    for i in range(0, 50):
        if not voters.find(users[i].get_text(strip=True)):
            hasQuote = posts[i].find("div")
            if not hasQuote is None: # Skips quoted posts
                hasQuote.extract()
            posts[i].append(posts[i].get_text(strip=True))
            lists = posts[i].find_all("li")
            # Gets the list and then calculates the votes using the query
            list_rank = 0
            for list in lists:
                bold = list.find("b")
                if(bold is not None):
                    updatePoints(bold.contents[0], 0 if list_rank > 10 else 10 - list_rank, getRank(list_rank))
                list_rank = list_rank + 1
            if list_rank > 0:
                voters.insert(users[i].get_text(strip=True))
                
# end for loop

getGOTY()

def getKey(item):
    return item[1]

# End Vote Collection
# Begin Tallying

#testUpdatePoints()
#testUpdatePointsWithRemakeVote()
#testUpdatePointsWithNewGames()
#testGetPCGame()
#testGetPS4Game()
#testGetXBOGame()
#testGetNSWGame()
