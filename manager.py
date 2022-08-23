import requests
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import pickle, pyfiglet
from colorama import init, Fore
import os, random
from time import sleep

init()

lg = Fore.LIGHTGREEN_EX
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
r = Fore.RED
n = Fore.RESET
colors = [lg, r, w, cy, ye]

def banner():
    f = pyfiglet.Figlet(font='slant')
    banner = f.renderText('TelegramBot')
    print(f'{random.choice(colors)}{banner}{n}')
    print(r+'  Version: 1.0 | Auteur : Hugo'+n+'\n')


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

while True:
    clr()
    #print(r)
    banner()
    #print(n)
    print(lg+'[1] Ajouter un compte'+n)
    print(lg+'[2] Filtrer tous les comptes bannis'+n)
    print(lg+'[3] Liste des comptes'+n)
    print(lg+'[4] Supprimer un compte'+n)
    #print(lg+'[5] Update your Genisys'+n)
    print(lg+'[5] Quitter')
    a = int(input(f'\nEntrez votre choix : {r}'))
    if a == 1:
        with open('vars.txt', 'ab') as g:
            newly_added = []
            while True:
                a = int(input(f'\n{lg}API ID : {r}'))
                b = str(input(f'{lg}API Hash : {r}'))
                c = str(input(f'{lg}Numéro de téléphone : {r}'))
                p = ''.join(c.split())
                pickle.dump([a, b, p], g)
                newly_added.append([a, b, p])
                ab = input(f'\nVoulez-vous ajouter un autre compte ? [y/n] : ')
                if 'y' in ab:
                    pass
                else:
                    print('\n'+lg+'[i] Enregistrement des comptes dans => vars.txt'+n)
                    g.close()
                    sleep(3)
                    clr()
                    print(lg + '[*] Connexion à un compte ...\n')
                    for added in newly_added:
                        c = TelegramClient(f'sessions/{added[2]}', added[0], added[1])
                        try:
                            c.start()
                            print(f'n\n{lg}[+] Connecter - {added[2]}')
                            c.disconnect()
                        except PhoneNumberBannedError:
                            print(f'{r}[!] {added[2]} est bannis ! Filtrer le compte !')
                            continue
                        print('\n')
                    input(f'\n{lg}Appuyez sur [entrer] pour revenir')
                    break
        g.close()
    elif a == 2:
        accounts = []
        banned_accs = []
        h = open('vars.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(h))
            except EOFError:
                break
        h.close()
        if len(accounts) == 0:
            print(r+'[!] Aucun compte, veuillez réessayer !')
            sleep(3)
        else:
            for account in accounts:
                api_id = int(account[0])
                api_hash = str(account[1])
                phone = str(account[2])
                client = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
                client.connect()
                if not client.is_user_authorized():
                    try:
                        client.send_code_request(phone)
                        client.sign_in(phone, input('[+] Code de vérification : '))
                    except PhoneNumberBannedError:
                        print(r+str(phone) + ' est bannis !'+n)
                        banned_accs.append(account)
            if len(banned_accs) == 0:
                print(lg+'Bravo ! Aucun compte bannis !')
                input('\nAppuyez sur [entrer] pour revenir')
            else:
                for m in banned_accs:
                    accounts.remove(m)
                with open('vars.txt', 'wb') as k:
                    for a in accounts:
                        Id = a[0]
                        Hash = a[1]
                        Phone = a[2]
                        pickle.dump([Id, Hash, Phone], k)
                k.close()
                print(lg+'[i] Compte(s) bannis supprimés !'+n)
                input('\nAppuyez sur [entrer] pour revenir')
    elif a == 3:
        display = []
        j = open('vars.txt', 'rb')
        while True:
            try:
                display.append(pickle.load(j))
            except EOFError:
                break
        j.close()
        print(f'\n{lg}')
        print(f'API ID  |            API Hash              |    N° Tél')
        print(f'==========================================================')
        i = 0
        for z in display:
            print(f'{z[0]} | {z[1]} | {z[2]}')
            i += 1
        print(f'==========================================================')
        input('\nAppuyez sur [entrer] pour revenir')

    elif a == 4:
        accs = []
        f = open('vars.txt', 'rb')
        while True:
            try:
                accs.append(pickle.load(f))
            except EOFError:
                break
        f.close()
        i = 0
        print(f'{lg}[i] Choissisez le compte à supprimer\n')
        for acc in accs:
            print(f'{lg}[{i}] {acc[2]}{n}')
            i += 1
        index = int(input(f'\n{lg}[+] Entrer votre choix : {n}'))
        phone = str(accs[index][2])
        session_file = phone + '.session'
        if os.name == 'nt':
            os.system(f'del sessions\\{session_file}')
        else:
            os.system(f'rm sessions/{session_file}')
        del accs[index]
        f = open('vars.txt', 'wb')
        for account in accs:
            pickle.dump(account, f)
        print(f'\n{lg}[+] Compte supprimé !{n}')
        input(f'{lg}Appuyez sur [entrer] pour revenir{n}')
        f.close()
    elif a == 5:
        clr()
        banner()
        quit()