#!/usr/bin/python

import random
import requests
from urllib import urlencode
from time import sleep

adjectives = []
with open('adjectives.txt', 'r') as f:
    for line in f:
        l = line.rstrip()
        if l:
            adjectives.append(l)

nouns = []
with open('nouns.txt', 'r') as f:
    for line in f:
        l = line.rstrip()
        if l:
            nouns.append(l)

first_names = []
with open('first-names.txt', 'r') as f:
    for line in f:
        l = line.rstrip()
        if l:
            first_names.append(l)

last_names = []
with open('last-names.txt', 'r') as f:
    for line in f:
        l = line.rstrip()
        if l:
            last_names.append(l)

def gen_bite_code():
    return random.choice(adjectives).lower() + " " + random.choice(nouns).lower() 

def gen_email_from_name(first, last):
    choice = random.randint(0, 2)
    email = None
    if choice == 0:
        email = first[0] + last
    elif choice == 1:
        email = last[0] + first
    elif choice == 2:
        email = last + str(random.randint(1, 100))

    choice = random.randint(0, 4)
    if choice in (0, 1):
        return email + "@uchicago.edu"
    elif choice == 2:
        return email + "@gmail.com"
    elif choice == 3:
        return email + "@yahoo.com"
    elif choice == 4:
        return email + "@hotmail.com"

def gen_full_name_and_email():
    fn = random.choice(first_names).capitalize()
    ln = random.choice(last_names).capitalize()
    full_name = fn + " " + ln
    return (full_name, gen_email_from_name(fn.lower(), ln.lower()))

def gen_phone_number():
    num = []
    num.append(random.randint(1, 9))
    for i in range(2):
        num.append(random.randint(0, 9)) 
    num.append(random.randint(1, 9))
    for i in range(6):
        num.append(random.randint(0, 9))

    num = "".join([str(x) for x in num])

    choice = random.randint(0, 2)
    style = None
    if choice == 0:
        style = "(%s) %s %s" 
    elif choice == 1:
        style = "%s %s %s"
    elif choice == 2:
        style = "%s-%s-%s"
    return style % (num[0:3], num[3:6], num[6:]) 

def gen_dorm():
    dorms = (
        'Breckinridge',
        'Broadview',
        'I-House',
        'Pierce',
        'Snell-Hitchcock',
        'Stony Island',
        'Blackstone',
        'Maclean',
        'Burton-Judson',
        'South Campus',
        'Off-Campus'
    )
    return random.choice(dorms)

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0",
    'Referer': "https://docs.google.com/forms/d/1p7VNinbXBGjgQayODkomRMTKOwVcPVuRf516-QAEt_A/viewform",
    'content-type': "application/x-www-form-urlencoded"
} # fake the user agent just in case

POST_URL = "https://docs.google.com/forms/d/1p7VNinbXBGjgQayODkomRMTKOwVcPVuRf516-QAEt_A/formResponse"

while True:
    full_name, email = gen_full_name_and_email()
    payload = [
        ('entry.1028291225', gen_bite_code()),
        ('entry.1267003877', full_name),
        ('entry.378817673', gen_dorm())
    ] 

    if random.randint(0, 1) == 1: # phone number
        payload.append(('entry.322695584', gen_phone_number()))
    if random.randint(0, 1) == 1: # email
        payload.append(('entry.147584741', email))
    if random.randint(0, 1) == 1: # add to listhost
        payload.append(('entry.1468720448', 'Be added to the HvZ Legion Listhost'))
    if random.randint(0, 1) == 1: # get texts
        payload.append(('entry.1468720448', 'Get My Texts'))
    
    payload.append(('draftResponse', '[]'))
    payload.append(('pageHistory', 0))
    payload.append(('submit', 'Submit'))

    print payload
    payload = urlencode(payload)
    r = requests.post(POST_URL, headers=HEADERS, data=payload)
    print "HTTP " + str(r.status_code)
    print r.text

    sleepTime = 5 + random.randint(0, 10)
    sleep(sleepTime)

