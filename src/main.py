import csv
import numpy as np
import requests
 
inputDir = '../resources/'
outputDir = '../out/'
inputRows = []
outputRows = []
headers = ['Player Id', 'First Name', 'Last Name', 'Position', 'Team', 'Opponent', 'Ownership']

contestId = input('Enter contest id: ')
inputFilename = input('Enter name of Yahoo player list file (located in ' + inputDir + '): ')
outputFilename = contestId + '_ownership.csv'

print ('Compiling ownership data...')

ownershipDict = {}

# reading csv file
with open(inputDir + inputFilename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)     
    fields = next(csvreader)

    for row in csvreader:
        # initialize player id ownership
        ownershipDict[row[0]] = -1.0
        # populate output csv info
        outputRows.append(row[0:6])


contestUrl = 'https://dfyql-ro.sports.yahoo.com/v2/contest/' + contestId
entriesUrl = 'https://dfyql-ro.sports.yahoo.com/v2/contestEntries?contestId=' + contestId + '&start={0}&limit={1}'
lineupsUrl = 'https://dfyql-ro.sports.yahoo.com/v2/contestEntry/{0}'

# calculate offset step for each iteration to get even distribution across contest
contestRequest = requests.get(contestUrl)
contestJson = contestRequest.json()
maxEntries = contestJson['contests']['result'][0]['entryLimit']
step = 50 if maxEntries <= 1000 else (int(maxEntries / 20))

playersPopulated = 0
offset = 0

# use yahoo api to fetch ownership data
while offset < maxEntries:
    # fetch entries for contest, 50 is the max number available per request
    entriesRequest = requests.get(entriesUrl.format(offset, offset + 50))
    entriesJson = entriesRequest.json()

    # get all entry ids
    entries = entriesJson['entries']['result']
    entryIds = [str(e['id']) for e in entries]

    # get data for each entry
    lineupsRequest = requests.get(lineupsUrl.format(','.join(entryIds)))
    lineupsJson = lineupsRequest.json()
    lineups = lineupsJson['entries']['result']

    # parse lineup/player data
    for lineup in lineups:
        players = lineup['lineupSlotList']
        for player in players:
            playerId = player['player']['code']
            if (ownershipDict.get(playerId) == -1):
                ownershipDict[playerId] = player['playerDraftPercent']
                playersPopulated += 1

    # get next set of entries
    offset += step
    print('.')

# populate ownership column
for row in outputRows:
    percentage = ownershipDict.get(row[0])
    if (percentage <= 0.1):
        percentage = '0.1'
    row.append(str(percentage))

# writing to csv file
with open(outputDir + outputFilename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(headers)     
    csvwriter.writerows(outputRows)

print(outputFilename + ' written to ' + outputDir)
