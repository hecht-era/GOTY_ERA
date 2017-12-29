# Import Libraries
import urllib.request
from bs4 import BeautifulSoup
import sqlite3, csv, re, string

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
    title = checkVote(title)
    query1 = 'SELECT * FROM gameslist WHERE title = \"%s\";' % (title)

    con = sqlite3.connect("goty.db")
    con.row_factory = sqlite3.Row
    c = con.cursor()
    c.execute(query1)
    row = c.fetchone()

    if row is None:
        length = length + 1
        query3 = "INSERT INTO gameslist (num, title, platform, publisher, genre, points, first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, runnerup) VALUES (%i, '%s', 'pc', 'other', 'action', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);" % (length, title)
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

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre NOT LIKE '%remake%' ORDER BY points DESC LIMIT 20;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getFullList():
    print("Full Results\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute('SELECT * FROM gameslist WHERE points > 0 OR runnerup > 0 ORDER BY points DESC;')
    winners = c.fetchall();

    csvWriter = csv.writer(open("results.csv", "w"))
    with open('results.csv','w') as f:
        writer = csv.writer(f, delimiter =',')
        writer.writerows(winners)

    con.commit()
    c.close()
    con.close()

def getBestPCGame():
    print("Best PC Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%pc%' ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestPS4Game():
    print("Best PS4 Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()
    
    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%ps4%' ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestXBOGame():
    print("Best Xbox One Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()
    
    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%xbo%' ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestNSWGame():
    print("Best Nintendo Switch Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%nsw%' ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBest3DSGame():
    print("Best 3DS Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%3ds%' ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestVITAGame():
    print("Best Vita Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%vita%' ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestMobileGame():
    print("Best Mobile Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%ios%' OR platform LIKE 'AND' ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestActionGame():
    print("Best Action Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%action%' AND genre NOT LIKE '%action adventure%' ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestActionAdventureGame():
    print("Best Action-Adventure Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%action adventure%' ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestAdventureGame():
    print("Best Adventure Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%adventure%' AND genre NOT LIKE '%action adventure%' ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestRPGGame():
    print("Best RPG Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%rpg%' ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestShooterGame():
    print("Best Shooter Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%shooter%' ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestHorrorGame():
    print("Best Horror Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%horror%' and points > 0 ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestRacingGame():
    print("Best Racing Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%racing%' and points > 0 ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestSportsGame():
    print("Best Sports Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%sports%' and points > 0 ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestStrategyGame():
    print("Best Strategy Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%strategy%' and points > 0 ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestFightingGame():
    print("Best Fighting Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%fighting%' and points > 0 ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestPuzzleGame():
    print("Best Puzzle Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%puzzle%' and points > 0 ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestBoardAndCardGame():
    print("Best Board And Card Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%board+Card%' and points > 0 ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestVRGame():
    print("Best VR Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%vr%' and points > 0 ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestRemakeGame():
    print("Best Remakes")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%remake%' ORDER BY points DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getFanFavorite():
    print("Most Popular Games (Based on most #1 votes)\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, first FROM gameslist ORDER BY first DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i votes' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestPublisher():
    print("Best Publisher\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT publisher, sum(points) FROM gameslist GROUP BY publisher ORDER BY sum(points) DESC;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i votes' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def checkVote(vote):
    if vote.find("zelda") != -1 or vote.find("botw") != -1 or vote.find("breath of the wild") != -1:
        return "the legend of zelda breath of the wild"
    elif vote.find("resident evil") != -1:
        return "resident evil vii biohazard"
    elif vote.find("wolfenstein") != -1:
        return "wolfenstein ii the new colossus"
    elif vote.find("mario odyssey") != -1:
        return "super mario odyssey"
    elif vote.find("assassins creed") != -1:
        return "assassins creed origins"
    elif vote.find("playerunknown") != -1 or vote.find("pubg") != -1 or vote.find("battleground") != -1:
        return "playerunknowns battlegrounds"
    elif vote.find("nier") != -1:
        return "nier automata"
    elif vote.find("horizon zero") != -1:
        return "horizon zero dawn"
    elif vote.find("persona") != -1:
        return "persona 5"
    elif vote.find("divinity") != -1:
        return "divinity original sin ii"
    elif vote.find("rabbids") != -1:
        return "mario + rabbids kingdom battle"
    elif vote.find("mario kart") != -1:
        return "mario kart 8 deluxe"
    elif vote.find("hellblade") != -1:
        return "hellblade senuas sacrifice"
    elif vote.find("uncharted") != -1:
        return "uncharted the lost legacy"
    elif vote.find("splatoon") != -1:
        return "splatoon 2"
    elif vote.find("doki doki") != -1:
        return "doki doki literature club"
    elif vote.find("ys viii") != -1:
        return "ys viii lacrimosa of dana"
    elif vote.find("nex machina") != -1:
        return "nex machina death machine"
    elif vote.find("danganronpa") != -1:
        return "danganronpa v3 killing harmony"
    elif vote.find("xenoblade") != -1:
        return "xenoblade chronicles 2"
    elif vote.find("pokemon ultra") != -1:
        return "pokemon ultra sun ultra moon"
    elif vote.find("snipperclips") != -1:
        return "snipperclips cut it out together"  
    elif vote.find("forza") != -1 and vote.find("7") != -1:
        return "forza motorsport 7"  
    elif vote.find("etrian") != -1:
        return "etrian odyssey v beyond the myth"  
    elif vote.find("xcom") != -1:
        return "xcom 2 war of the chosen"
    elif vote.find("friday") != -1:
        return "friday the 13th the game"  

    return vote

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

length = 399
loadGamesList()

# Define variables
allVotes = [[] for i in range(2000)]
userTotal = []
finalTally = [[] for i in range(1000)]
voters = HashTable(2048)
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
    'https://www.resetera.com/threads/resetera-games-of-the-year-2017-voting-thread-read-the-op-ends-jan-21st-8-59am-est.11841/', 
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

thread = "https://www.resetera.com/threads/resetera-games-of-the-year-2017-voting-thread-read-the-op-ends-jan-21st-8-59am-est.11841/"
print(numPages)

for p in range(1, numPages + 1):
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
    users = era_page.find_all("div", {"class" : "messageUserBlock"})
    posts = era_page.find_all("div", {"class" : "messageContent"})
    for i in range(0, len(posts)):
        if not voters.find(users[i].find("a", {"class": "username"}).get_text(strip=True)):
            hasQuote = posts[i].find("div")
            if not hasQuote is None: # Skips quoted posts
                hasQuote.extract()
            posts[i].append(posts[i].get_text(strip=True))
            lists = posts[i].find_all("li")
            # Gets the list and then calculates the votes using the query
            list_rank = 0
            for list in lists:
                while list.find('b') is not None:
                    list = list.find("b")
                bold = list;
                if(bold is not None):
                    bold.contents[0] = bold.contents[0].string.rstrip(' -:<>b\\(.;,')
                    bold.contents[0] = bold.contents[0].lstrip(' <>b')
                    bold.contents[0] = bold.contents[0].replace("'", "")
                    bold.contents[0] = bold.contents[0].replace(":", "")
                    bold.contents[0] = bold.contents[0].replace(" - ", " ")
                    bold.contents[0] = bold.contents[0].replace("-", " ")
                    bold.contents[0] = bold.contents[0].replace(";", "")
                    bold.contents[0] = bold.contents[0].replace('"', "")
                    bold.contents[0] = bold.contents[0].replace("\\", " ")
                    bold.contents[0] = bold.contents[0].replace("/", " ")
                    bold.contents[0] = bold.contents[0].replace("<", " ")
                    bold.contents[0] = bold.contents[0].replace(">", " ")
                    bold.contents[0] = bold.contents[0].replace("’", "")
                    bold.contents[0] = bold.contents[0].replace("(", "")
                    bold.contents[0] = bold.contents[0].replace(")", "")
                    bold.contents[0] = bold.contents[0].replace("!", "")
                    bold.contents[0] = bold.contents[0].replace(",", "")
                    bold.contents[0] = bold.contents[0].replace(".", "")
                    bold.contents[0] = bold.contents[0].lower()
                    points = 0
                    if list_rank < 10:
                        points = points + 1
                    if list_rank < 6:
                        points = points + 1
                    if list_rank < 3:
                        points = points + 1
                    if list_rank == 0:
                        points = points + 1
                    updatePoints(bold.contents[0], points, getRank(list_rank))
                list_rank = list_rank + 1;
            if list_rank > 0:
                    voters.insert(users[i].get_text(strip=True))
        
# end for loop

# # Tally the votes
# for i in range(1, userNum):
#     for j in range(len(allVotes[i])):
#         for x in range(len(finalTally)):
#             if allVotes[i][j] in finalTally[x]:
#                 if(j==0):
#                     finalTally[x][1] += 4
#                 elif(j>=1 and j<=2):
#                     finalTally[x][1] += 3
#                 elif(j>=3 and j<=5):
#                     finalTally[x][1] += 2
#                 elif(j>=6 and j<=9):
#                     finalTally[x][1] += 1
#                 else:
#                     finalTally[x][1] += 0
#                 doesExist = True #Game was found in the list already, will bypass the following
#         if not doesExist: # Adds game to list if not found already
#             #print(allVotes[i][j])
#             tempVote[0] = allVotes[i][j]
#             if(j==0):
#                     tempVote[1] = 4
#             elif(j>=1 and j<=2):
#                     tempVote[1] = 3
#             elif(j>=3 and j<=5):
#                     tempVote[1] = 2
#             elif(j>=6 and j<=9):
#                     tempVote[1] = 1
#             else:
#                     tempVote[1] = 0
#             finalTally[gameNum].append(tempVote[0])
#             finalTally[gameNum].append(tempVote[1])
#             gameNum += 1
#         #print(allVotes[i][j])
#         doesExist = False
# #print(allVotes)


# list2 = [x for x in finalTally if x != []]

getGOTY()
print("")
print("\nPlatform Awards")
getBestPCGame()
print("")
getBestPS4Game()
print("")
getBestVITAGame()
print("")
getBestXBOGame()
print("")
getBestNSWGame()
print("")
getBest3DSGame()
print("")
getBestMobileGame()
print("")
getBestVRGame()
print("")
print("\n Genre Awards")
getBestActionGame()
print("")
getBestActionAdventureGame()
print("")
getBestAdventureGame()
print("")
getBestRPGGame()
print("")
getBestHorrorGame()
print("")
getBestPuzzleGame()
print("")
getBestFightingGame()
print("")
getBestShooterGame()
print("")
getBestSportsGame()
print("")
getBestStrategyGame()
print("")
getBestRacingGame()
print("")
getBestBoardAndCardGame()
print("")
getBestRemakeGame()
print("")
getFanFavorite()
print("")
getBestPublisher()
print("")
getFullList()



def getKey(item):
    return item[1]

# final = sorted(list2, key = getKey, reverse=True)
# print(final)

# for j in range(len(final)):
#     r = str(final[j][0])
#     results.write(r)
#     results.write(" - ")
#     s = str(final[j][1])
#     results.write(s)
#     results.write("\n")
# results.close()

# End Vote Collection
# Begin Tallying


#for x in range(len(final)):
    #title = final[x][0]
    #points = final[x][1]
    #rank = place[points]
    #if (place[points]<=0):
        #rank = place[0]
    #final[x][1] = final[x][1]/2-1
    ##updatePoints(title, points, rank)
