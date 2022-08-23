from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
from telethon.tl.functions.channels import JoinChannelRequest
import csv
import time
import keyboard
import random
import pyfiglet
from colorama import init, Fore
import os
import pickle
import traceback
'''
try:
    import beepy
except ImportError:
    if os.name == 'nt':
        os.system('pip install beepy')
    else:
        pass
'''
init()

r = Fore.RED
lg = Fore.GREEN
rs = Fore.RESET
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [r, lg, w, ye, cy]
info = lg + '(' + w + 'i' + lg + ')' + rs
error = lg + '(' + r + '!' + lg + ')' + rs
success = w + '(' + lg + '*' + w + ')' + rs
INPUT = lg + '(' + cy + '~' + lg + ')' + rs
plus = lg + '(' + w + '+' + lg + ')' + rs
def banner():
    f = pyfiglet.Figlet(font='slant')
    logo = f.renderText('TelegramBot')
    print(random.choice(colors) + logo + rs)
    print(f'{r}   Version: {w}1.0 {r}| Auteur : {w}Hugo{rs}')


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
global scraped_grp
with open('target_grp.txt', 'r') as f:
    scraped_grp = f.readline()
f.close()

clr()
banner()
users = []
input_file = 'members\\members.csv'
with open(input_file, 'r', encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter=',', lineterminator='\n')
    next(reader, None)
    for row in reader:
        user = {}
        user['username'] = row[0]
        user['user_id'] = row[1]
        user['access_hash'] = row[2]
        user['group'] = row[3]
        user['group_id'] = row[4]
        users.append(user)
accounts = []
f = open('vars.txt', 'rb')
while True:
    try:
        accounts.append(pickle.load(f))
    except EOFError:
        break
print('\n' + info + lg + ' Creation des sessions pour les comptes ...' + rs)
for a in accounts:
    iD = int(a[0])
    Hash = str(a[1])
    phn = str(a[2])
    clnt = TelegramClient(f'sessions\\{phn}', iD, Hash)
    clnt.connect()
    banned = []
    if not clnt.is_user_authorized():
        try:
            clnt.send_code_request(phn)
            code = input(f'{INPUT}{lg} Entrer le code pour {w}{phn}{cy}[s pour passer]:{r}')
            if 's' in code:
                accounts.remove(a)
            else:
                clnt.sign_in(phn, code)
        except PhoneNumberBannedError:
            print(f'{error}{w}{phn} {r}est bannis !{rs}')
            banned.append(a)
    for z in banned:
        accounts.remove(z)
        print('\n'+info+lg+'Compte bannis supprimé'+rs)
    time.sleep(0.5)
    clnt.disconnect()


print(info+' Sessions créés !')
time.sleep(2)
print(f'{plus}{lg} Entrer le nom exact du groupe {w}[sans @]')
g = input(f'{INPUT}{lg} Username [Ex: GroupeTelegram]: {r}')
group = 't.me/' + str(g)
#print('\n')
print(f'{info}{lg} Connexion depuis les comptes...{rs}')
for account in accounts:
    api_id = int(account[0])
    api_hash = str(account[1])
    phone = str(account[2])
    client = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
    client.connect()
    try:
        username = client.get_entity(group)
        client(JoinChannelRequest(username))
        print(f'{success}{lg} Connecté depuis {phone}')
    except:
        print(f'{error}{r} Erreur de connexion depuis {phone}')
        accounts.remove(account)
    client.disconnect()
time.sleep(2)
clr()
number = len(accounts)
print(f'{info}{lg} Total des comptes : {w}{number}')
print(f'{info}{lg} Il est recommandé d\'utiliser le plus de comptes possible !')
a = int(input(f'{plus}{lg} Nombre de comptes à utiliser : {r}'))
to_use = []
print(f'\n{info}{lg} Chargement CSV ...{rs}')
time.sleep(2)
for i in accounts[:a]:
    done = []
    to_use.append(i)
    file = 'members\\members' + str(accounts.index(i)) + '.csv'
    with open(file, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
        for user in users[:60]:
            writer.writerow([user['username'], user['user_id'], user['access_hash'], user['group'], user['group_id']])
            done.append(user)
    f.close()
    del_count = 0
    while del_count != len(done):
        del users[0]
        del_count += 1
    if len(users) == 0:
        break
if not len(users) == 0:
    with open('members\\members.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
        for user in users:
            writer.writerow([user['username'], user['user_id'], user['access_hash'], user['group'], user['group_id']])
    f.close()
    m = str(len(users))
    print(f'{info}{lg} Il reste {m} utilisateurs dans {w}members.csv')
for acc in to_use:
    accounts.remove(acc)
with open('vars.txt', 'wb') as f:
    for acc in accounts:
        pickle.dump(acc, f)
    for k in to_use:
        pickle.dump(k, f)
    f.close()
'''
with open('resume.txt', 'w') as f:
    f.write(scraped_grp)
    f.close()
'''
print(f'{info}{lg} Chargement CSV complet !{rs}')
time.sleep(2)
clr()
if not os.name == 'nt':
    print(f'{error}{r} Windows seulement')
    sys.exit()

program = 'usradder.py'
o = str(len(to_use))
print(f'\n{info}{r} Execution entièrement automatique.')
print(f'{info}{r} Ne touchez pas à votre clavier pendant l\'éxecution !')
input(f'\n{plus}{lg} Appuyez sur [entrer] pour continuer ...{rs}')
print(f'\n{info}{lg} Lancement depuis {o} comptes...{rs}\n')
for i in range(5, 0, -1):
    print(random.choice(colors) + str(i) + rs)
    time.sleep(1)
for account in to_use:
    api_id = str(account[0])
    api_hash = str(account[1])
    phone = str(account[2])
    file = 'members\\members' + str(to_use.index(account)) + '.csv'
    os.system('Démarrage du CMD')
    time.sleep(1.5)
    keyboard.write('python' + ' ' + program + ' ' + api_id + ' ' + api_hash + ' ' + phone + ' ' + file + ' ' + group + ' ' + str(scraped_grp))
    keyboard.press_and_release('Enter')
    print(f'{plus}{lg} Ajout de {phone}')
#beepy.beep(sound='ping')
