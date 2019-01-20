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
    with open('gameslist2018.csv', 'r') as f:
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
    print("Top 20 Games of 2018\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre NOT LIKE '%remake%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 20;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getFullList():
    print("Full Results\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT * FROM gameslist WHERE (points > 0 OR runnerup > 0) AND genre NOT LIKE '%nq%' ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC;")
    winners = c.fetchall()
    # for winner in winners
    #     print(winner)
    #     print('\n')

    with open('results.csv','w',newline='') as f:
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

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE platform LIKE '%pc%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestPS4Game():
    print("Best PS4 Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()
    
    c.execute("SELECT title, points, runnerup FROM gameslist WHERE platform LIKE '%ps4%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestXBOGame():
    print("Best Xbox One Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()
    
    c.execute("SELECT title, points, runnerup FROM gameslist WHERE platform LIKE '%xbo%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestNSWGame():
    print("Best Nintendo Switch Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE platform LIKE '%nsw%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestHandheldGame():
    print("Best Handheld Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE platform LIKE '%3ds%' OR platform LIKE '%vita%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestMobileGame():
    print("Best Mobile Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE platform LIKE '%mob%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestActionGame():
    print("Best Action Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%action%' AND genre NOT LIKE '%action adventure%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestActionAdventureGame():
    print("Best Action-Adventure Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%action adventure%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestAdventureGame():
    print("Best Adventure Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%adventure%' AND genre NOT LIKE '%action adventure%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestRPGGame():
    print("Best RPG Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%rpg%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestShooterGame():
    print("Best Shooter Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%shooter%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestHorrorGame():
    print("Best Horror Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%horror%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestRacingGame():
    print("Best Racing Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%racing%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestSportsGame():
    print("Best Sports Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%sports%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestStrategyGame():
    print("Best Strategy Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%strategy%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestFightingGame():
    print("Best Fighting Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%fighting%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestPuzzleGame():
    print("Best Puzzle Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%puzzle%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestBoardAndCardGame():
    print("Best Party, Rhythm, Board, And Card Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%prcb%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestVRGame():
    print("Best VR Games\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%vr%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestRemakeGame():
    print("Best Remakes")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%remake%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestSimulationGame():
    print("Best Simulators")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, points, runnerup FROM gameslist WHERE genre LIKE '%simulation%' and points > 0 ORDER BY points DESC, first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s = %i points, %i honorable mentions' % (count, winner[0], winner[1], winner[2]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getFanFavorite():
    print("Most Popular Games (Based on most #1 votes)\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT title, first FROM gameslist ORDER BY first DESC, second DESC, third DESC, fourth DESC, fifth DESC, sixth DESC, seventh DESC, eighth DESC, ninth DESC, tenth DESC, runnerup DESC LIMIT 10;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s, %i votes' % (count, winner[0], winner[1]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestPublisher():
    print("Best Publisher\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT publisher, sum(points) FROM gameslist GROUP BY publisher ORDER BY sum(points) DESC LIMIT 20;")
    winners = c.fetchall()

    count = 1
    for winner in winners:
        print('%i. %s, %i points' % (count, winner[0], winner[1]))
        count = count + 1

    con.commit()
    c.close()
    con.close()

def getBestConsole():
    print("Best Consoles\n")
    con = sqlite3.connect("goty.db")
    c = con.cursor()

    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%nsw%';")
    nsw = c.fetchall()
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%ps4%';")
    ps4 = c.fetchall()
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%xbo%';")
    xbo = c.fetchall()
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%pc%';")
    pc = c.fetchall()
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%wiiu%';")
    wiiu = c.fetchall()
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%ps3%';")
    ps3 = c.fetchall()
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%360%'")
    x360 = c.fetchall()
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%3ds%'")
    n3ds = c.fetchall()
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%vita%'")
    vita = c.fetchall()
    c.execute("SELECT sum(points) FROM gameslist WHERE platform LIKE '%mob%'")
    mob = c.fetchall()

    consoles = [("nsw", nsw), ("ps4", ps4), ("xbo", xbo), ("pc", pc), ("wiiu", wiiu), ("ps3", ps3), 
        ("360", x360), ("3ds", n3ds), ("vita", vita), ("mob", mob)]

    consoles = sorted(consoles, key=getKey, reverse=True)

    for console in consoles:
        print("%s %i points" % (console[0], console[1][0][0]))

    con.commit()
    c.close()
    con.close()

def checkVote(vote):
    if vote.find("marvel") != -1 or vote.find("spiderman") != -1 or vote.find("spider man") != -1:
        return "marvels spiderman"
    if vote.find("tomb raider") != -1:
        return "shadow of the tomb raider"
    elif vote.find("dragon ball") != -1 or vote.find("dragonball") != -1:
        return "dragonball fighterz"
    elif vote.find("dragon quest xi") != -1 or vote.find("dragon quest 11") != -1 or vote.find("echoes of an elusive age") != -1:
        return "dragon quest xi echoes of an elusive age"
    elif vote.find("yakuza 6") != -1:
        return "yakuza 6 the song of life"
    elif vote.find("red dead redemption") != -1 or vote.find("red red redemption") != -1 or vote.find("read dead redemption") != -1 or vote == "red" or vote == "red redemption 2" or vote == "red dead redeption 2":
        return "red dead redemption 2"
    elif vote.find("super smash") != -1 or vote.find("smash bros") != -1 or vote == "smash ultimate" or vote == "super smah bros ultimate" or vote == "super smas bros ultimate":
        return "super smash bros ultimate"
    elif vote.find("fortnite") != -1:
        return "fortnite battle royale"
    elif vote.find("god of") != -1 or vote == "of war":
        return "god of war"
    elif vote.find("astro bot") != -1 or vote.find("astrobot") != -1 or vote == "astro" or vote == "tro bot":
        return "astro bot rescue mission"
    elif vote.find("xenoblade") != -1:
        return "xenoblade chronicles 2 torna the golden country"
    elif vote.find("just shapes & beats") != -1:
        return "just shapes and beats"
    elif vote.find("ni no kuni") != -1:
        return "ni no kuni ii revenant kingdom"
    elif vote.find("obra dinn") != -1 or vote.find("orbra dinn") != -1:
        return "return of the obra dinn"
    elif vote.find("octopath") != -1:
        return "octopath traveler"
    elif vote.find("call of duty") != -1 or vote.find("black ops 4") != -1:
        return "call of duty black ops iiii"
    elif vote.find("mega man 11") != -1 or vote.find("mega man xi") != -1 or vote.find("megaman xi") != -1:
        return "megaman 11"
    elif vote.find("pokemon lets go") != -1 or vote.find("pokémon lets go") != -1 or vote.find("pókemon lets go") != -1:
        return "pokemon lets go pikachu and eevee"
    elif vote.find("farcry") != -1 or vote == "fary cry 5" or vote == "far":
        return "far cry 5"
    elif vote.find("pillars of eternity") != -1:
        return "pillars of eternity ii deadfire"
    elif vote.find("persona 3") != -1:
        return "persona 3 dancing moon night"
    elif vote.find("persona 4") != -1:
        return "persona 4 dancing all night"
    elif vote.find("persona 5") != -1:
        return "persona 5 dancing in starlight"
    elif vote.find("monster boy") != -1:
        return "monster boy and the cursed kingdom"
    elif vote.find("mutant year zero") != -1:
        return "mutant year zero road to eden"
    elif vote.find("detroit") != -1 or vote.find("become human") != -1:
        return "detroit become human"
    elif vote.find("battlefield") != -1:
        return "battlefield v"
    elif vote.find("soul calibur") != -1  or vote.find("soulcalibur") != -1:
        return "soulcalibur vi"
    elif vote.find("forza") != -1:
        return "forza horizon 4"
    elif vote.find("thronebreaker") != -1:
        return "thronebreaker the witcher tales"
    elif vote.find("tropical freeze") != -1:
        return "donkey kong country tropical freeze"
    elif vote.find("kiwami") != -1 or vote == "yakuza 2":
        return "yakuza kiwami 2"
    elif vote.find("divinity original sin") != -1:
        return "divinity original sin ii definitive edition"
    elif vote.find("delta rune") != -1:
        return "deltarune chapter 1"
    elif vote.find("the breach") != -1:
        return "into the breach"
    elif vote.find("valkyria chronicles 4") != -1 or vote.find("valkyria 4") != -1 or vote.find("valkyria chrinicles 4") != -1 or vote.find("chronicles 4") != -1 or vote == "valkyria chronicals 4":
        return "valkyria chronicles 4"
    elif vote.find("assassins creed") != -1 or vote.find("assassin´s creed") != -1 or vote.find("creed odyssey") != -1:
        return "assassins creed odyssey"
    elif vote.find("hollow knight") != -1 or vote == "hollow night":
        return "hollow knight"
    elif vote.find("banner saga") != -1:
        return "the banner saga 3"
    elif vote.find("yakuza 0") != -1:
        return "yakuza 0"
    elif vote.find("shadow of the") != -1 or vote.find("shadow of colossus") != -1:
        return "shadow of the colossus"
    elif vote.find("zone of the enders") != -1:
        return "zone of the enders vr"
    elif vote.find("hellblade") != -1:
        return "hellblade senuas sacrifice"
    elif vote.find("life is strange 2") != -1:
        return "life is strange 2 episode 1"
    elif vote.find("before the storm") != -1:
        return "life is strange before the storm farewell"
    elif vote.find("rush vr") != -1:
        return "rush"
    elif vote.find("no mans sky") != -1:
        return "no mans sky"
    elif vote.find("diablo") != -1:
        return "diablo iii the eternal collection"
    elif vote.find("captain spirit") != -1:
        return "the awesome adventures of captain spirit"
    elif vote == "mhw" or vote == "onster hunter world":
        return "monster hunter world"
    elif vote.find("ys viii") != -1:
        return "ys viii lacrimosa of dana"
    elif vote.find("moss") != -1:
        return "moss"
    elif vote.find("ead cells") != -1 or vote == "dead":
        return "dead cells"
    elif vote.find("bayonetta 1") != -1 or vote == "bayonetta":
        return "bayonetta"
    elif vote.find("the world ends with you") != -1:
        return "the world ends with you final remix"
    elif vote.find("street fighter 5") != -1:
        return "street fighter v arcade edition"
    elif vote.find("total war warhammer") != -1:
        return "total war warhammer ii rise of the tomb kings"
    elif vote.find("donkey kong country") != -1:
        return "donkey kong country tropical freeze"
    elif vote.find("dark souls") != -1:
        return "dark souls remastered"
    elif vote.find("strange journey redux") != -1:
        return "shin megami tensei strange journey redux"
    elif vote.find("unravel") != -1:
        return "unravel two"
    elif vote.find("gwent") != -1:
        return "gwent the witcher card game"
    elif vote.find("the missing") != -1:
        return "the missing jj macfield and the island of memories"
    elif vote.find("mario + rabbids") != -1:
        return "mario + rabbids kingdom battle donkey kong adventure"
    elif vote.find("darksiders") != -1:
        return "darksiders iii"
    elif vote.find("starlink") != -1 or vote.find("star link") != -1:
        return "starlink battle for atlas"
    elif vote.find("kingdom come") != -1:
        return "kingdom come deliverance"
    elif vote.find("gris") != -1:
        return "gris"
    elif vote.find("deltarune") != -1:
        return "deltarune chapter 1"
    elif vote.find("atelier lydie & suelle") != -1 or vote.find("atelier lydie and suelle") != -1:
        return "atelier lydie & suelle the alchemists and the mysterious paintings"
    elif vote.find("atelier rorona") != -1:
        return "atelier rorona the alchemist of arland dx"
    elif vote.find("atelier totori") != -1:
        return "atelier totori the alchemist of arland dx"
    elif vote.find("celeste") != -1:
        return "celeste"
    elif vote.find("wipeout") != -1:
        return "wipeout omega collection"
    elif vote == "into the beach":
        return "into the breach"
    elif vote == "guacamalee 2":
        return "guacamelee 2"
    elif vote.find("destiny 2") != -1:
        return "destiny 2 forsaken"
    elif vote.find("beat saber") != -1:
        return "beat saber"
    elif vote.find("vermintide") != -1:
        return "warhammer vermintide 2"
    elif vote.find("labyrinth of refrain") != -1:
        return "labyrinth of refrain coven of dusk"
    elif vote.find("the red strings club") != -1:
        return "the red strings club"
    elif vote.find("nintendo labo") != -1 or vote == "labo":
        return "nintendo labo"
    elif vote.find("shibuya scramble") != -1:
        return "428 shibuya scramble"
    elif vote.find("dragon quest builders") != -1:
        return "dragon quest builders"
    elif vote.find("yokus") != -1 or vote.find("island express") != -1:
        return "yokus island express"
    elif vote.find("trails of cold steel") != -1:
        return "the legend of heroes trails of cold steel ii"
    elif vote.find("civilization vi rise and fall") != -1:
        return "sid meiers civilization vi rise and fall"
    elif vote.find("tetris effect") != -1 or vote == "tetris" or vote == "tetris effec":
        return "tetris effect"
    elif vote.find("iconoclast") != -1:
        return "iconoclasts"
    elif vote.find("pubg") != -1 or vote == "player unknowns battlegrounds":
        return "playerunknowns battlegrounds"
    elif vote.find("deracine") != -1:
        return "déraciné"
    elif vote.find("donut country") != -1:
        return "donut county"
    elif vote.find("nier automata become as gods edition") != -1:
        return "nier automata"
    elif vote.find("street fighter v") != -1:
        return "street fighter v arcade edition"
    elif vote.find("sushi striker") != -1:
        return "sushi striker the way of sushido"
    elif vote.find("splatoon") != -1:
        return "splatoon 2 octo expansion"
    elif vote.find("the last remnant") != -1:
        return "the last remnant remastered"
    elif vote.find("resonance of fate") != -1:
        return "resonance of fate remastered"
    elif vote.find("cthulhu") != -1 or vote.find("cthuhlu") != -1:
        return "call of cthulhu the official videogame"
    elif vote.find("cross code") != -1:
        return "crosscode"
    elif vote.find("spyro") != -1:
        return "spyro reignited trilogy"
    elif vote.find("final fantasy xv") != -1:
        return "final fantasy xv windows edition"
    elif vote.find("reigns") != -1:
        return "reigns game of thrones"
    elif vote.find("blazeblue") != -1:
        return "blazblue cross tag battle"
    elif vote.find("over cooked 2") != -1:
        return "overcooked 2"
    elif vote.find("dissidia") != -1:
        return "dissidia final fantasy nt"
    elif vote.find("wario") != -1:
        return "warioware gold"
    elif vote.find("shenmue") != -1:
        return "shenmue i & ii"
    elif vote.find("sonic mania") != -1:
        return "sonic mania plus"
    elif vote == "forgotton anne":
        return "forgotten anne"
    elif vote.find("final fantasy xii") != -1:
        return "final fantasy xii the zodiac age"
    elif vote.find("shapeshifting") != -1:
        return "the shapeshifting detective"
    elif vote.find("mario tennis") != -1:
        return "mario tennis aces"
    elif vote == "electronaughts":
        return "electronauts"
    elif vote.find("jackbox") != -1:
        return "the jackbox party pack 5"
    elif vote.find("captain toad") != -1:
        return "captain toad treasure tracker"
    elif vote.find("hitman 2") != -1:
        return "hitman 2"
    elif vote.find("vampyr") != -1:
        return "vampyr"
    return vote

class HashTable:
    size = 16
    num = 0
    table = [None] * size

    def __init__(self, s):
        self.size = s
        self.table = [None] * self.size

    def insert(self, value):
        value = str(value)
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
        value = str(value)
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
thread = "https://www.resetera.com/threads/resetera-games-of-the-year-2018-voting-thread-read-the-op-ends-jan-20th-8-59am-est.87946/"
req = urllib.request.Request(
    thread,   
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
pages = era_page.find("li", {"class" : "pageNav-page "})
nav = pages.find("a")
numPages = int(nav.contents[0])
voterCount = 0

# print(numPages)

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
    users = era_page.find_all("a", {"class" : "username", "itemprop" : "name"})
    posts = era_page.find_all("div", {"class" : "bbWrapper"})
    startRange = 0
    if(p == 1):
        startRange = 1
    
    for i in range(startRange, len(posts)):
        # print("")
        # print(users[i])
        user = users[i]
        post = posts[i]
        if not voters.find(users[i]):
            hasQuote = posts[i].find_all("div", {"class": " bbCodeBlock bbCodeBlock--expandable bbCodeBlock--quote"})
            for quote in hasQuote: # Skips quoted posts
                quote.extract()
            vote_list = posts[i].find("ol")
            if vote_list is None or len(vote_list) == 0:
                continue
            lists = vote_list.find_all("li")
            # Gets the list and then calculates the votes using the query
            list_rank = 0
            for list in lists:
                if list.find('b') is None:
                    continue
                while list.find('b') is not None:
                    list = list.find("b")
                bold = list
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
                    bold.contents[0] = bold.contents[0].replace("‘", "")
                    bold.contents[0] = bold.contents[0].lower()
                    # print(bold.contents[0])
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
                list_rank = list_rank + 1
            if list_rank > 0:
                voters.insert(users[i])
                voterCount = voterCount + 1

getGOTY()
print("")
print("\nPlatform Awards")
getBestPCGame()
print("")
getBestPS4Game()
print("")
getBestXBOGame()
print("")
getBestNSWGame()
print("")
getBestHandheldGame()
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
getBestSimulationGame()
print("")
getBestRemakeGame()
print("")
getFanFavorite()
print("")
getBestPublisher()
print("")
getBestConsole()
print("Total Voters %i" % (voterCount))
getFullList()