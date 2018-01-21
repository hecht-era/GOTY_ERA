# Import Libraries
import urllib.request
from bs4 import BeautifulSoup
import sqlite3, csv, re, string

def getKey(item):
    return item[1][0][0]

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
    c.executescript("""DROP TABLE IF EXISTS gameslist; CREATE TABLE gameslist (title TEXT, platform TEXT, publisher TEXT, genre TEXT, points INTEGER, first INTEGER, second INTEGER, third INTEGER, fourth INTEGER, fifth INTEGER, sixth INTEGER, seventh INTEGER, eighth INTEGER, ninth INTEGER, tenth INTEGER, runnerup INTEGER);""")
    with open('gameslist.csv', 'r') as f:
        dr = csv.DictReader(f)
        to_db = [(i['Title'], i['Platform'], i['Publisher'], 
                i['Genre'], i['Points'], i['First'], i['Second'], i['Third'], 
                i['Fourth'], i['Fifth'], i['Sixth'], i['Seventh'], i['Eighth'], 
                i['Ninth'], i['Tenth'], i['Runner Up']) for i in dr]
        length = len(to_db)

    c.executemany("INSERT INTO gameslist (title, platform, publisher, genre, points, first, "
        + "second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, runnerup) VALUES "
        + "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
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
        query3 = "INSERT INTO gameslist (title, platform, publisher, genre, points, first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, runnerup) VALUES ('%s', 'pc', 'other', 'action', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);" % (title)
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

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre NOT LIKE '%remake%' OR genre NOT LIKE '%nq%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 20;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getFullList():
    print("Full Results\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT * FROM gameslist WHERE (points > 0 OR runnerup > 0) AND genre NOT LIKE '%nq%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC;")
    winners = c.fetchall();

    csvWriter = csv.writer(open("results.csv", "w"))
    with open('results.csv','w') as f:
        writer = csv.writer(f, delimiter =',')
        writer.writerow(['Title', 'Platforms', 'Publisher', 'Genre', 'Points', 'First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth', 'Ninth', 'Tenth', 'Runner-up'])
        writer.writerows(winners)

    con.commit()
    c.close()
    con.close()

def getBestPCGame():
    print("Best PC Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE platform LIKE '%pc%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestPS4Game():
    print("Best PS4 Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()
    
    c.execute("SELECT title, points, runnerup FROM gameslist WHERE platform LIKE '%ps4%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestXBOGame():
    print("Best Xbox One Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()
    
    c.execute("SELECT title, points, runnerup FROM gameslist WHERE platform LIKE '%xbo%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestNSWGame():
    print("Best Nintendo Switch Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE platform LIKE '%nsw%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBest3DSGame():
    print("Best 3DS Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE platform LIKE '%3ds%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestVITAGame():
    print("Best Vita Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE platform LIKE '%vita%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestMobileGame():
    print("Best Mobile Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE platform LIKE '%ios%' OR platform LIKE 'AND' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestActionGame():
    print("Best Action Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%action%' AND genre NOT LIKE '%action adventure%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestActionAdventureGame():
    print("Best Action-Adventure Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%action adventure%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestAdventureGame():
    print("Best Adventure Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%adventure%' AND genre NOT LIKE '%action adventure%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestRPGGame():
    print("Best RPG Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%rpg%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestShooterGame():
    print("Best Shooter Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%shooter%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestHorrorGame():
    print("Best Horror Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%horror%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestRacingGame():
    print("Best Racing Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%racing%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestSportsGame():
    print("Best Sports Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%sports%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestStrategyGame():
    print("Best Strategy Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%strategy%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestFightingGame():
    print("Best Fighting Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%fighting%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestPuzzleGame():
    print("Best Puzzle Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%puzzle%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestBoardAndCardGame():
    print("Best Board And Card Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%board+Card%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestVRGame():
    print("Best VR Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%vr%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestRemakeGame():
    print("Best Remakes")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%remake%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestRhythmGame():
    print("Best Rhythm Games")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%rhythm%' AND points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestSimulationGame():
    print("Best Simulators")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%simulation%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getFanFavorite():
    print("Most Popular Games (Based on most #1 votes)\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, first FROM gameslist ORDER BY first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
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

    c.execute("SELECT publisher, sum(points) FROM gameslist GROUP BY publisher ORDER BY sum(points) DESC LIMIT 20;")
    winners = c.fetchall();

    count = 1;
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]));
        count = count + 1;

    con.commit()
    c.close()
    con.close()

def getBestConsole():
    print("Best Consoles\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%nsw%';")
    nsw = c.fetchall();
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%ps4%';")
    ps4 = c.fetchall();
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%xbo%';")
    xbo = c.fetchall();
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%pc%';")
    pc = c.fetchall();
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%wiiu%';")
    wiiu = c.fetchall();
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%ps3%';")
    ps3 = c.fetchall();
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%360%'")
    x360 = c.fetchall();
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%3ds%'")
    n3ds = c.fetchall();
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%vita%'")
    vita = c.fetchall();
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%ios%'")
    ios = c.fetchall();
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%and%'")
    gand = c.fetchall();

    consoles = [("nsw", nsw), ("ps4", ps4), ("xbo", xbo), ("pc", pc), ("wiiu", wiiu), ("ps3", ps3), 
        ("360", x360), ("3ds", n3ds), ("vita", vita), ("ios", ios), ("and", gand)]

    consoles = sorted(consoles, key=getKey, reverse=True)

    for console in consoles:
        print("%s: %i points" % (console[0], console[1][0][0]))

    con.commit()
    c.close()
    con.close()

def checkVote(vote):
    if vote.find("zelda") != -1 or vote.find("botw") != -1 or vote.find("breath of the wild") != -1:
        return "the legend of zelda breath of the wild"
    elif (vote.find("resident evil") != -1 and (vote.find("vii") != -1 or vote.find("7") != -1)) or vote.find("biohazard") != -1 or vote.find("resident") != -1:
        return "resident evil vii biohazard"
    elif vote.find("wolfenstein") != -1 or vote.find("wolfenstien") != -1 or vote.find("colossus") != -1:
        return "wolfenstein ii the new colossus"
    elif vote.find("mario od") != -1 or (vote.find("super mario") != -1 and vote.find("run") == -1) or vote == "super" or vote == "mario switch":
        return "super mario odyssey"
    elif vote.find("assassins creed") != -1 or vote.find("origins") != -1:
        return "assassins creed origins"
    elif vote.find("unknown") != -1 or vote.find("pubg") != -1 or vote.find("battleground") != -1 :
        return "playerunknowns battlegrounds"
    elif vote.find("nier") != -1 or vote.find("automata") != -1:
        return "nier automata"
    elif vote.find("horizon zero") != -1 or (vote.find("horizon") != -1 and vote.find("forza") == -1):
        return "horizon zero dawn"
    elif vote.find("persona") != -1:
        return "persona 5"
    elif vote.find("divinity") != -1:
        return "divinity original sin ii"
    elif vote.find("rabbids") != -1 or vote.find("rabbits") != -1 or vote.find("rabids") != -1 or vote.find("mario +") != -1:
        return "mario + rabbids kingdom battle"
    elif vote.find("mario kart") != -1:
        return "mario kart 8 deluxe"
    elif vote.find("hellblade") != -1 or vote.find("senuas") != -1 or vote.find("hell") != -1:
        return "hellblade senuas sacrifice"
    elif vote.find("uncharted") != -1 or vote == 'ucll':
        return "uncharted the lost legacy"
    elif vote.find("splatoon") != -1:
        return "splatoon 2"
    elif vote.find("doki doki") != -1:
        return "doki doki literature club"
    elif vote.find("ys viii") != -1 or vote.find("ys 8") != -1:
        return "ys viii lacrimosa of dana"
    elif vote.find("nex machin") != -1:
        return "nex machina death machine"
    elif vote.find("danga") != -1:
        return "danganronpa v3 killing harmony"
    elif vote.find("xenoblade") != -1:
        return "xenoblade chronicles 2"
    elif vote.find("pokemon ultra") != -1 or vote.find("pokémon") != -1:
        return "pokemon ultra sun ultra moon"
    elif vote.find("snipperclips") != -1:
        return "snipperclips cut it out together"  
    elif vote.find("forza") != -1 and vote.find("7") != -1:
        return "forza motorsport 7"  
    elif vote.find("etrian") != -1:
        return "etrian odyssey v beyond the myth"  
    elif vote.find("xcom") != -1 or vote.find("x com") != -1:
        return "xcom 2 war of the chosen"
    elif vote.find("friday") != -1:
        return "friday the 13th the game"  
    elif vote.find("crash") != -1:
        return "crash bandicoot n sane trilogy"
    elif vote.find("skyrim") != -1 and vote.find("vr") != -1:
        return "the elder scrolls v skyrim vr"
    elif vote.find("skyrim") != -1 or vote.find("the elder scrolls v") != -1:
        return "the elder scrolls v skyrim"
    elif vote.find("steam") != -1 and vote.find("world") != -1:
        return "steamworld dig 2"    
    elif vote.find("knack") != -1:
        return "knack ii"    
    elif vote.find("evil within") != -1:
        return "the evil within 2"  
    elif vote.find("15") != -1 and vote.find("25") != -1:
        return "kingdom hearts hd 15 + 25 remix"  
    elif vote.find("fire emblem echoes") != -1 or vote.find("valentia") != -1:
        return "fire emblem echoes shadows of valentia"  
    elif vote.find("total war") != -1:
        return "total war warhammer ii"  
    elif vote.find("binding") != -1:
        return "the binding of isaac afterbirth+"
    elif vote.find("madden") != -1:
        return "madden nfl 18"
    elif vote.find("yakuza zero") != -1 or vote.find("yakuza 0") != -1:
        return "yakuza 0" 
    elif vote.find("battlefront") != -1:
        return "star wars battlefront ii" 
    elif vote.find("fifa") != -1:
        return "fifa 18" 
    elif vote.find("puyo") != -1:
        return "puyo puyo tetris"
    elif vote.find("night in the woods") != -1:
        return "night in the woods"
    elif vote.find("ghost recon") != -1:
        return "tom clancys ghost recon wildlands"
    elif vote.find("finding paradise") != -1:
        return "finding paradise"
    elif vote.find("ys vii") != -1:
        return "ys viii lacrimosa of dana"
    elif vote.find("final fantasy xiv") != -1 or vote.find("final fantasy 14") != -1 or vote.find("ffxiv") != -1:
        return "final fantasy xiv stormblood"
    elif vote.find("final fantasy xii") != -1 or vote.find("final fantasy 12") != -1 or vote.find("ffxii") != -1:
        return "final fantasy xii the zodiac age"
    elif vote.find("path of exile") != -1:
        return "path of exile the fall of oriath"
    elif vote.find("trails in the sky") != -1:
        return "the legend of heroes trails in the sky the 3rd"
    elif vote.find("tales") != -1:
        return "tales of berseria"
    elif vote.find("cup") != -1 and vote.find("head") != -1:
        return "cuphead"
    elif vote.find("magikarp") != -1:
        return "pokemon magikarp jump"
    elif vote.find("wonder") != -1:
        return "wonder boy the dragons trap"
    elif vote.find("hearthstone") != -1:
        return "hearthstone expansions"
    elif vote.find("28") != -1 or vote.find("ii8") != -1:
        return "kingdom hearts hd 28 final chapter"
    elif vote.find("dragon quest heroes") != -1:
        return "dragon quest heroes ii"
    elif vote.find("sonic mania") != -1:
        return "sonic mania"
    elif vote.find("blazblue") != -1:
        return "blazblue central fiction"
    elif vote.find("atelier sophie") != -1:
        return "atelier sophie the alchemist of the mysterious book"
    elif vote.find("battle garegga") != -1:
        return "battle garegga rev 2016"
    elif vote.find("call of duty") != -1 or vote.find("cod wwii") != -1 or vote.find("cod ww2") != -1:
        return "call of duty wwii"
    elif vote.find("dark souls") != -1:
        return "dark souls iii the ringed city"
    elif vote.find("destiny") != -1:
        return "destiny 2"
    elif vote.find("diablo") != -1:
        return "diablo iii rise of the necromancer"
    elif vote.find("disgaea") != -1:
        return "disgaea 5 complete"
    elif vote.find("doom") != -1 and vote.find("vfr") == -1:
        return "doom"
    elif vote.find("dishonored") != -1:
        return "dishonored death of the outsider"
    elif vote.find("dragon quest vii") != -1 or vote.find("dragon quest 8") != -1:
        return "dragon quest viii journey of the cursed king"
    elif vote.find("dragon quest xi") != -1 or vote.find("dragon quest 11") != -1:
        return "dragon quest xi"
    elif vote.find("dream daddy") != -1:
        return "dream daddy a dad dating simulator"
    elif vote.find("elite dangerous") != -1:
        return "elite dangerous"
    elif vote.find("farpoint") != -1:
        return "farpoint"
    elif vote.find("fire pro") != -1:
        return "fire pro wrestling world"
    elif vote.find("getting over it") != -1:
        return "getting over it with bennett foddy"
    elif vote.find("golf story") != -1:
        return "golf story"
    elif vote.find("gran turismo") != -1 or vote.find("gt sport") != -1:
        return "gran turismo sport"
    elif vote.find("gravity rush") != -1 or vote.find("gravity daze") != -1:
        return "gravity rush 2"
    elif vote.find("hollow knight") != -1:
        return "hollow knight"
    elif vote.find("hq") != -1:
        return "hq"
    elif vote.find("injustice 2") != -1:
        return "injustice 2"
    elif vote.find("jackbox") != -1 and vote.find("4") != -1:
        return "the jackbox party pack 4"
    elif vote.find("mass effect") != -1:
        return "mass effect andromeda"
    elif vote.find("metroid") != -1 or vote.find("samus") != -1:
        return "metroid samus returns"
    elif vote.find("nba 2k18") != -1:
        return "nba 2k18"
    elif vote.find("nioh") != -1:
        return "nioh"
    elif vote.find("overcooked") != -1:
        return "overcooked"
    elif vote.find("parappa") != -1:
        return "parappa the rapper remastered"
    elif vote.find("prey")!= -1:
        return "prey"
    elif vote.find("pro evo") != -1:
        return "pro evolution soccer 2018"
    elif vote.find("pyre") != -1:
        return "pyre"
    elif vote.find("rock of ages") != -1:
        return "rock of ages 2 bigger and boulder"
    elif vote.find("shovel knight") != -1 and vote.find("spec") != -1:
        return "shovel knight specter of torment"
    elif vote.find("snake") != -1:
        return "snake pass"
    elif vote.find("fractured but whole") != -1 or vote == 'south park':
        return "south park the fractured but whole"
    elif vote.find("stardew valley") != -1 or vote.find("stared valley") != -1:
        return "stardew valley"
    elif vote.find("superhot vr") != -1 or vote.find("super hot vr") != -1:
        return "superhot vr"
    elif vote.find("thimbleweed park") != -1:
        return "thimbleweed park"
    elif vote.find("tokyo xanadu") != -1:
        return "tokyo xanadu ex+"
    elif vote.find("mask of deception") != -1:
        return "utawarerumono mask of deception"
    elif vote.find("what remains") != -1 or vote.find("edith finch") != -1:
        return "what remains of edith finch"
    elif vote.find("zero escape") != -1 or vote.find("the nonary games") != -1:
        return "zero escape the nonary games"
    elif vote.find("zwei") != -1:
        return "zwei the ilvard insurrection"
    elif vote.find("dawn of war") != -1:
        return "warhammer 40000 dawn of war iii"
    elif vote.find("disney") != -1:
        return "the disney afternoon collection"
    elif vote.find("little nightmares") != -1:
        return "little nightmares"
    elif vote.find("rainbow six") != -1:
        return "tom clancys rainbow six siege year 2"
    elif vote.find("bayonetta") != -1:
        return "bayonetta"
    elif vote.find("ever") != -1 and vote.find("golf") != -1:
        return "everybodys golf"
    elif vote.find("xrd") != -1:
        return "guilty gear xrd rev 2"
    elif vote.find("gundam") != -1:
        return "gundam versus"
    elif vote.find("hitman") != -1:
        return "hitman patient zero"
    elif vote.find("marvel") != -1:
        return "marvel vs capcom infinite"
    elif vote.find("shadow of war") != -1:
        return "middle earth shadow of war"
    elif vote.find("observer") != -1:
        return "observer"
    elif vote.find("outlast") != -1:
        return "outlast 2"
    elif vote.find("pinball") != -1:
        return "pinball fx 3"
    elif vote.find("shadow tactics") != -1:
        return "shadow tactics blades of the shogun"
    elif vote.find("taiko") != -1:
        return "taiko no tatsujin session de dodon ga don"
    elif vote.find("paperclips") != -1:
        return "universal paperclips"
    elif vote.find("white day") != -1:
        return "white day a labyrinth named school"
    elif vote.find("undertale") != -1:
        return "undertale"
    elif vote.find("tacoma") != -1:
        return "tacoma"
    elif vote.find("cosmic star") != -1:
        return "cosmic star heroine"
    elif vote.find("ark surv") != -1:
        return "ark survival evolved"
    elif vote.find("pillars of the earth") != -1:
        return "ken folletts the pillars of the earth"
    elif vote.find("la noire") != -1:
        return "la noire"
    elif vote.find("mario & luigi") != -1:
        return "mario & luigi superstar saga + bowsers minions"
    elif vote.find("minecraft nintendo") != -1:
        return "minecraft nintendo switch edition"
    elif vote.find("rain w") != -1:
        return "rain world"
    elif vote.find("trails of cold steel") != -1:
        return "the legend of heroes trails of cold steel"
    elif vote.find("valkyria") != -1:
        return "valkyria revolution"
    elif vote.find("windjammers") != -1:
        return "windjammers"
    elif vote.find("wipeout") != -1:
        return "wipeout omega collection"
    elif vote.find("rez") != -1:
        return "rez infinite";
    elif vote.find("pillars of eternity") != -1:
        return "pillars of eternity complete edition"
    elif vote.find("night war") != -1:
        return "battle chasers nightwar"
    elif vote.find("gorogoa") != -1:
        return "gorogoa"
    elif vote.find("dragons dogma") != -1:
        return "dragons dogma dark arisen"
    elif vote.find("life is strange") != -1:
        return "life is strange before the storm"

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
            self.rebuildTable()

        place = 0
        for i in range(0, len(value)):
            place = place + ord(value[i])

        place = place % self.size
        
        while self.table[place] is not None:
            place = place + 1
            if(place >= self.size):
                place = 0
        self.table[place] = value
        self.num = self.num + 1

    def rebuildTable(self):
        self.size = self.size * 2
        newTable = [None] * self.size
        for item in self.table:
            if item is not None:
                place = 0
                for i in range(0, len(item)):
                    place = place + ord(item[i])
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
voterCount = 0;

thread = "https://www.resetera.com/threads/resetera-games-of-the-year-2017-voting-thread-read-the-op-ends-jan-21st-8-59am-est.11841/"
#print(numPages)

for p in range(1, numPages + 1):
    thread2 = thread + "page-" + str(p)
    #print(thread2)
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
    startRange = 0;
    if(p == 1):
        startRange = 1;
    
    for i in range(startRange, len(posts)):
        #print("")
        #print(users[i].find("a", {"class": "username"}).get_text(strip=True))
        if not voters.find(users[i].find("a", {"class": "username"}).get_text(strip=True)):
            hasQuote = posts[i].findAll("div", {"class": "bbCodeBlock bbCodeQuote"})
            for quote in hasQuote: # Skips quoted posts
                quote.extract()
            vote_list = posts[i].find_all("ol")
            if len(vote_list) == 0:
                continue
            lists = vote_list[0].find_all("li")
            # Gets the list and then calculates the votes using the query
            list_rank = 0
            for list in lists:
                # if list.find('b') is None:
                #     continue
                while list.find('b') is not None:
                    list = list.find("b")
                bold = list;
                if(bold is not None):
                    bold.contents[0] = bold.contents[0].string.rstrip(' -:<>\\(.;,')
                    bold.contents[0] = bold.contents[0].lstrip(' <>')
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
                    #print(bold.contents[0])
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
                voters.insert(users[i].find("a", {"class": "username"}).get_text(strip=True))
                voterCount = voterCount + 1

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
getBestRhythmGame()
print("")
getBestSimulationGame()
print("")
getBestRemakeGame()
print("")
getFanFavorite()
print("")
getBestPublisher()
print("")
getBestConsole()
print("Total Voters: %i" % (voterCount))
getFullList()