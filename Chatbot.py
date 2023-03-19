import random
from datetime import datetime
import pytz
import re
import csv
from fuzzywuzzy import fuzz
import bs4
import requests
greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "howdy", "greetings", "salutations", "what's up", "bonjour", "hola", "ciao", "namaste", "salam", "kon'nichiwa", "guten tag", "merhaba", "sawasdee"]
acks = ['awesome', 'great', 'good', 'cool', 'excellent', 'fantastic', 'outstanding', 'impressive', 'terrific', 'wonderful', 'amazing', 'superb', 'phenomenal', 'brilliant', 'splendid', 'fabulous', 'marvelous', 'spectacular', 'nice', 'pleasant', 'satisfactory', 'adequate', 'fine', 'decent', 'fair', 'okay', 'ok']
byes = ['bye', 'goodbye', 'see ya', 'later', 'adios', 'ciao', 'cheerio', 'farewell', 'ta-ta', 'take care']
while True:
  answered = False
  inp = input(">>> ").lower()
  name = fuzz.ratio(inp, "what is your name")
  if name > 80:
    print("My name is ChickBot")
    answered = True
  cre = fuzz.ratio(inp, "who created you")
  if cre > 80:
    print("I was created by Arnav Malhotra")
    answered = True
  for ack in acks:
    sat = fuzz.ratio(inp, ack)
    if sat > 80:
      print("Glad to hear it!")
      answered = True
      break
  for bye in byes:
      far = fuzz.ratio(inp, bye)
      if far > 80:
        print(random.choice(byes))
        answered = True
        exit()
  hour = int(datetime.now(pytz.timezone('America/New_York')).strftime("%H"))
  for greeting in greetings:
    if re.search(f"^{greeting}", inp):
      if hour <= 13:
        print(random.choice(["hello", "hi", "hey", "howdy", "greetings", "salutations", "what's up", "good morning"]))
      if hour > 13 and hour < 18:
        print(random.choice(["hello", "hi", "hey", "howdy", "greetings", "salutations", "what's up", "good afternoon"]))
      if hour >= 18:
        print(random.choice(["hello", "hi", "hey", "howdy", "greetings", "salutations", "what's up", "good evening"]))
      answered = True
      break
  if answered:
    continue
  wi = re.match(r".*what is( a| an| the)?\s+(.+)$", inp)
  noun = ""
  article = ""
  ndk = False
  if wi:
    article = wi.group(1)
    noun = wi.group(2)
    if article == None:
      article = ""
    url = f"https://www.merriam-webster.com/dictionary/{noun}"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    defs = soup.find_all('span', class_='dtText')
    try:
        text = defs[0].text[2::]
        if text[-9::] == ": such as":
          text = text[0:-9]
        print(f"{article} {noun} is {text}")
        answered = True
    except:
        ndk = True
  if answered:
    continue
  whi = re.match(r".*who (was|is)\s+(.+)$", inp)
  woi = ""
  per = ""
  pdk = False
  if whi:
    woi = whi.group(1)
    per = whi.group(2)
    url = f"https://www.famousbirthdays.com/people/{per.replace(' ', '-')}.html"
    response = requests.get(url)
    try:
      soup = bs4.BeautifulSoup(response.content, 'html.parser')
      biol = soup.find('div', class_="bio col-sm-7 col-md-8 col-lg-6")
      bio = biol.find_all('p')[0].text
      print(f"{per} {woi} the {bio}")
      answered = True
    except:
      pdk = True
  if answered:
    continue
  if ndk:
    print(f"I don't know what {article} {noun} is")
  elif pdk:
    print(f"I don't know who {per} {woi}")
  else:
    print("I don't know what to say to that")