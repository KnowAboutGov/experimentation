import re
import json
DEFAULT_URL = "https://www.senate.gov/senators/index.htm"
DEFAULT_NAME = "Last, First (D-PA)"

# open the downloaded html file
web_file = open("senate.txt", "r+")
json_file = open("newtest.json", "x")
# put the web_file as a string in memory
senate_page_html = web_file.read()
# have the file in memory so dont need the file open anymore
web_file.close()

# split the file into lines
senate_lines = senate_page_html.splitlines()
# create list of table rows
senate_rows = []
senators = []

# iterate through the lines and append the rows to senate_rows
for i in range(len(senate_lines)):
    if (senate_lines[i].startswith('<td>')):
        senate_rows.append(senate_lines[i])

# extract the senator url from the row string
def extractUrl(tableRow):
    # regex search for http://xxxxxx.gov OR http://xxxxxx.gov/
    reMatch = re.search("http://.+(.gov/|.gov)", tableRow)
    if (not reMatch == None):
        return reMatch.group(0)
    else:
        return DEFAULT_URL

def extractNameString(tableRow):
    reMatch = re.search("[A-Za-z]+\,.+\(.+\)", tableRow)
    if (not reMatch == None):
        return reMatch.group(0)
    else:
        return DEFAULT_NAME

def extractName(nameString):
    name = {}
    commaPos = nameString.find(",")
    leftP = nameString.find("(")
    lastName = nameString[:commaPos]
    firstName = nameString[commaPos+1:leftP].strip()
    name["lastName"] = lastName
    name["firstName"] = firstName
    return name

def extractStateAndParty(tableRow):
    stateAndParty = {}
    reMatch = re.search("<td>[A-Za-z\s]{3,}</td><td>[A-Za-z]{3,}</td>", tableRow)
    innerText = re.findall("[A-Za-z\s]{4,}", reMatch.group(0))
    stateAndParty["state"] = innerText[0]
    stateAndParty["party"] = innerText[1]
    return stateAndParty

def extractClass(tableRow):
    reMatch = re.search("Class\s\w{1,3}", tableRow)
    return reMatch.group(0)

def buildSenatorDict(tableRow):
    thisNameString = extractNameString(tableRow)
    thisName = extractName(thisNameString)
    thisStateAndParty = extractStateAndParty(tableRow)
    senator = {}
    senator["name"] = {}
    senator["name"]["first"] = thisName["firstName"]
    senator["name"]["last"] = thisName["lastName"]
    senator["state"] = thisStateAndParty["state"]
    senator["party"] = thisStateAndParty["party"]
    senator["class"] = extractClass(tableRow)
    return senator


for i in range(len(senate_rows)):
    senators.append(buildSenatorDict(senate_rows[i]))

jsonContainer = {
    "senators" : senators
}

json.dump(jsonContainer, json_file)







