import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client()

unhappy_words = [ "shitty", "depressive", "depressed", "unhappy", "worry", "bad", "bored", "sad", ]

call = ["$bot", "ohayoo", "hey bot"]

starter_discouragements = ["don't be sad we love you", "Life is beautiful, be happy"]

answer = ["Hey!.", "Hey! my dear", "Yeah. i am here"]

fruit_list = ["apple"]

buku_list = ["give 21-30 litres water to apple every 2-3 day", "i like apples"]

wink_list = ["😉"]

wink_hate = ["oh you are so charismathic", "you look funny"]

clown_list = ["🤡"]

clown_hate = ["You are so funny. always be happy:)"]

poop_list = ["💩"]

poop_hate = ["Be gentle", "Don't use this"]

if "quba" not in db.keys():
  db["quba"] = True

if "helptime" not in db.keys():
  db["helptime"] = "1"

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_discouragements(discouraging_message):
  if "discouragements" in db.keys():
    discouragements = db["discouragements"]
    discouragements.append(discouraging_message)
    db["discouragements"] = discouragements
  else:
    db["discouragements"] = [discouraging_message]

def delete_discouragement(index):
  discouragements = db["discouragements"]
  if len(discouragements) > index:
    del discouragements[index]
    db["discouragements"] = discouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.author.bot:
    return
#  print(message.content)
  msg = message.content

  if msg.startswith('$hello'):
    await message.channel.send('Hello!')

  if msg.startswith('$cherry'):
    await message.channel.send('https://www.britannica.com/plant/cherry')

  if msg.startswith('$apple'):
    await message.channel.send('https://www.fast-growing-trees.com/pages/apple-trees-guide')
    
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["quba"]:

    options = starter_discouragements
    if "discouragements" in db.keys():
      options.append(db["encouragements"]) 

    if any(word in msg.casefold() for word in unhappy_words):
      options = options + [get_quote()]
      await message.channel.send(random.choice(options))

    if any(word in msg.casefold() for word in call):
      await message.channel.send(random.choice(answer))
    
    if any(word in msg for word in fruit_list):
      await message.channel.send(random.choice(buku_list))
    
    if any(word in msg for word in wink_list):
      await message.channel.send(random.choice(wink_hate))

    if any(word in msg for word in clown_list):
      await message.channel.send(random.choice(clown_hate))
    
    if any(word in msg for word in poop_list):
      await message.channel.send(random.choice(poop_hate))


  if msg.startswith("$new"):
    discouraging_message = msg.split("$new ",1)[1]
    update_discouragements(discouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    discouragements = []
    if "discouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_discouragement(index)
      discouragements = db["discouragements"]
    await message.channel.send(discouragements)

  if msg.startswith("$list"):
    discouragements = []
    if "discouragements" in db.keys():
      discouragements = db["discouragements"]
    await message.channel.send(discouragements)

  if msg.startswith("$quba"):
    value = msg.split("$quba ",1)[1]

    if value.lower() == "true":
      db["quba"] = True
      await message.channel.send("Time to talk some good things.")
    else:
      db["quba"] = False
      await message.channel.send("Stopping talking...")
  
  if msg.startswith("$help"):
    await message.channel.send("```diff\n"
    "- Commands:\n"
    "+      $help - this menu\n"
    "+      $mean - show random mean quote\n"
    "+      $new New mean quote. - adds 'New mean quote.' to DB\n"
    "-           Example: $new life loves you.\n"
    "+      $list - lists quotes in DB\n"
    "+      $del ID# - removes quote from DB by ID (starts at 0)\n\n"
    "-      $quba true - Talk things.\n"
    "-      $quba false - Stop talking things.\n"
    "```")

keep_alive()
client.run(os.getenv('TOKEN'))