# Import Libraries
import urllib.request
from bs4 import BeautifulSoup

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

# Request Webpage
req = urllib.request.Request(
    'http://23.91.70.28/~resetera/index.php?threads/the-resetera-goty-2017-voting-thread.63/', 
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

thread = "http://23.91.70.28/~resetera/index.php?threads/the-resetera-goty-2017-voting-thread.63/"

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
    
