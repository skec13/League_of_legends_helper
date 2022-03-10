import requests
import json
import champId
from colorama import init
from colorama import Fore, Back, Style
from beautifultable import BeautifulTable


key = 'RGAPI-1fba2903-a6f6-48a1-a8ee-bb6b80925e9e'

init()


print(Fore.LIGHTCYAN_EX + '+---------------------------------------+')
print(Fore.LIGHTCYAN_EX + '|       League of Legends helper        |')
print(Fore.LIGHTCYAN_EX + '+---------------------------------------+')

while(1):
    print(Fore.LIGHTBLUE_EX + '-> Enter server name(eun1, euw1):')
    serverInput = input()
    if(serverInput == 'eun1' or serverInput == 'euw1'):
        break
    else:
        print(Fore.LIGHTRED_EX + 'Wrong server name!')


while(1):
    print(Fore.LIGHTBLUE_EX + '-> Enter summoner name:')
    summonerInput = input()
    encrypted_request = requests.get('https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'.format(serverInput, summonerInput, key))
    if(encrypted_request.status_code == 200):
        break
    else:
        print(Fore.LIGHTRED_EX + 'Wrong summoner name!')

encrypted_response = encrypted_request.text
encrypted_decoded = json.loads(encrypted_response)
summonerId = encrypted_decoded['id']


#requests
user_request = requests.get("https://eun1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{}".format(summonerId),
                 headers={
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29",
                     "Accept-Language": "en-US,en;q=0.9,sl;q=0.8",
                    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Origin": "https://developer.riotgames.com",
                    "X-Riot-Token": "{}".format(key)
})


#requests decode
user_response = user_request.text
user_decoded = json.loads(user_response)



chestAvailable = []
chestNotAvailable = []
championMastery = []
championLevel = []


for i in range(0, len(user_decoded), 1):
    if (user_decoded[i]['chestGranted'] == True):
        chestNotAvailable.append(champId.champs_dict[user_decoded[i]['championId']])
    else:
        chestAvailable.append(champId.champs_dict[user_decoded[i]['championId']])
    championMastery.append((champId.champs_dict[user_decoded[i]['championId']], user_decoded[i]['championPoints']))
    championLevel.append((champId.champs_dict[user_decoded[i]['championId']], user_decoded[i]['championLevel'], user_decoded[i]['tokensEarned']))

chestAvailable.sort()
chestNotAvailable.sort()


w = 7
h = int(len(chestNotAvailable)/7) + 1
h1 = int(len(chestAvailable)/7) + 1
h2 = int(len(user_decoded)/7) + 1
Matrix = [['' for x in range(w)] for y in range(h)]
Matrix1 = [['' for x in range(w)] for y in range(h1)]
Matrix2 = [['' for x in range(w)] for y in range(h2)]


j = 0
if(len(Matrix) == 1):
    for i in range(0, len(chestNotAvailable), 1):
        Matrix[j][i%7] = chestNotAvailable[i]
else:
    while(j < len(Matrix) - 1):
        for i in range(0, len(chestNotAvailable), 1):
            Matrix[j][i%7] = chestNotAvailable[i]
            if((i + 1)%7 == 0):
                j = j + 1



k = 0
while(k < len(Matrix1)-1):
    for i in range(0, len(chestAvailable), 1):
        Matrix1[k][i%7] = chestAvailable[i]
        if((i + 1)%7 == 0):
            k = k + 1

l = 0
while(l < len(Matrix2)-1):
    for i in range(0, len(user_decoded), 1):
        Matrix2[l][i%7] = championLevel[i][0] + '\nLevel:' + str(championLevel[i][1]) + '\nTokens:' + str(championLevel[i][2])
        if((i + 1)%7 == 0):
            l = l + 1




while(1):
    print(Fore.LIGHTCYAN_EX + '+---------------------------------------+')
    print(Fore.LIGHTBLUE_EX + '-> Press 1 for chest granted champs\n-> Press 2 for chest not granted champs\n-> Press 3 for individual champ\n-> Press 4 for champion level and tokens\n-> Press 0 for exit')
    inputChoice = input()
    if(inputChoice == '1'):
        table = BeautifulTable()
        for i in range(0, len(Matrix), 1):
            table.rows.append(Matrix[i])
        table.set_style(BeautifulTable.STYLE_DEFAULT)
        table.columns.alignment = BeautifulTable.ALIGN_LEFT
        table.columns.width = 16
        print(table)
    elif(inputChoice == '2'):
        table = BeautifulTable()
        for i in range(0, len(Matrix1), 1):
            table.rows.append(Matrix1[i])
        table.set_style(BeautifulTable.STYLE_DEFAULT)
        table.columns.alignment = BeautifulTable.ALIGN_LEFT
        table.columns.width = 16
        print(table)
    elif(inputChoice == '3'):
        print(Fore.LIGHTBLUE_EX + 'Champ name: ')
        champInput = input()
        if(chestNotAvailable.count(champInput) > 0):
            print(Fore.LIGHTBLUE_EX + 'Chest not available')
        elif(chestAvailable.count(champInput) > 0):
            print(Fore.LIGHTBLUE_EX + 'Chest available')
        else:
            print(Fore.LIGHTRED_EX + 'Invalid champ name!')
    elif(inputChoice == '4'):
        table = BeautifulTable()
        for i in range(0, len(Matrix2), 1):
            table.rows.append(Matrix2[i])
        table.set_style(BeautifulTable.STYLE_DEFAULT)
        table.columns.alignment = BeautifulTable.ALIGN_LEFT
        table.columns.width = 16
        print(table)

    elif(inputChoice == '0'):
        exit()

