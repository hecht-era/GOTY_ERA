# Import Libraries
import urllib.request
from bs4 import BeautifulSoup
import sqlite3, csv, re, string

length = 0

# Define variables
allVotes = [[] for i in range(2000)]
userTotal = []
finalTally = [[] for i in range(1000)]
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

for p in range(1, numPages):
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
                bold.contents[0] = bold.contents[0].string.rstrip(' -:<>b\\(.;,')
                bold.contents[0] = bold.contents[0].lstrip(' <>b')
                bold.contents[0] = bold.contents[0].lower()
                print(bold.contents[0])
                userTotal.append(bold.contents[0])
        for i in range(len(userTotal)):
            allVotes[userNum].append(userTotal[i])
        if(allVotes[userNum]!=[]):
           userNum += 1
        userTotal = []
# end for loop

# Tally the votes
for i in range(1, userNum):
    for j in range(len(allVotes[i])):
        for x in range(len(finalTally)):
            if allVotes[i][j] in finalTally[x]:
                if(j==0):
                    finalTally[x][1] += 4
                elif(j>=1 and j<=2):
                    finalTally[x][1] += 3
                elif(j>=3 and j<=5):
                    finalTally[x][1] += 2
                elif(j>=6 and j<=9):
                    finalTally[x][1] += 1
                else:
                    finalTally[x][1] += 0
                doesExist = True #Game was found in the list already, will bypass the following
        if not doesExist: # Adds game to list if not found already
            #print(allVotes[i][j])
            tempVote[0] = allVotes[i][j]
            if(j==0):
                    tempVote[1] = 4
            elif(j>=1 and j<=2):
                    tempVote[1] = 3
            elif(j>=3 and j<=5):
                    tempVote[1] = 2
            elif(j>=6 and j<=9):
                    tempVote[1] = 1
            else:
                    tempVote[1] = 0
            finalTally[gameNum].append(tempVote[0])
            finalTally[gameNum].append(tempVote[1])
            gameNum += 1
        #print(allVotes[i][j])
        doesExist = False
#print(allVotes)


list2 = [x for x in finalTally if x != []]

def getKey(item):
    return item[1]

final = sorted(list2, key = getKey, reverse=True)
print(final)

for j in range(len(final)):
    r = str(final[j][0])
    results.write(r)
    results.write(" - ")
    s = str(final[j][1])
    results.write(s)
    results.write("\n")
results.close()

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
