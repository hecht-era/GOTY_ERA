

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
        print "Inserting " + title
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
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getFullList():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute('SELECT * FROM gameslist ORDER BY points DESC;')
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestPCGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%PC%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestPS4Game():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%PS4%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestXBOGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%XBO%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestNSWGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%NSW%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBest3DSGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%3DS%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestVITAGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%VITA%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestMobileGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE platform LIKE '%iOS%' OR platform LIKE 'AND' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestActionGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Action%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestActionAdventureGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Action-Adventure%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestAdventureGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Adventure%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestRPGGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%RPG%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestShooterGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Shooter%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestRacingGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Racing%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestSportsGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Sports%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestStrategyGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Strategy%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestFightingGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Fighting%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestPuzzleGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Puzzle%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestVRGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%VR%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getBestRemakeGame():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points FROM gameslist WHERE genre LIKE '%Remake%' ORDER BY points DESC LIMIT 10;")
    print c.fetchall()

    con.commit()
    c.close()
    con.close()

def getFanFavorite():
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, first FROM gameslist ORDER BY first DESC LIMIT 10;")
    print c.fetchall()

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