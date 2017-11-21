# Import Libraries
import urllib.request
from bs4 import BeautifulSoup

# Define variables
allVotes = [[] for i in range(1000)]
userTotal = []
finalTally = [[] for i in range(500)]
tempVote = [0] * 2
userVote = 0
userNum = 0
gameNum = 0
doesExist = False;

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

# Collect posts/list items
posts = era_page.find_all("div", {"class" : "messageContent"})
for post in posts:
	hasQuote = post.find("div")
	if not hasQuote is None: # Skips quoted posts
		hasQuote.extract()
	post.append(post.get_text(strip=True))
	lists = post.find_all("li")
# Store votes in userTotal, then put userTotal as a list item in allVotes
	for list in lists:
		userTotal.append(list.contents[0])
	for i in range(len(userTotal)):
		allVotes[userNum].append(userTotal[i])
	userNum += 1
	userTotal = []
#print(allVotes)

# Tally the votes
for i in range(0, userNum):
	#print(i)
	for j in range(len(allVotes[i])):
		#print(allVotes[i][j])
		for x in range(len(finalTally)):
			if allVotes[i][j] in finalTally[x]:
				finalTally[x][1] += (10 - j)
				doesExist = True #Game was found in the list already, will bypass the following
		if not doesExist: # Adds game to list if not found already
			tempVote[0] = allVotes[i][j]
			tempVote[1] = (10-j)
			#print(tempVote)
			finalTally[gameNum].append(tempVote[0])
			finalTally[gameNum].append(tempVote[1])
			gameNum += 1
		doesExist = False
print(finalTally)