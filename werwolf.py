from rocketchat import RocketChatBot, RocketChatClient
import time
import random
from instructionsWW import showHelpW

server = 'localhost:3000'
botUser = 'botty'
botPass = 'botty'

bot = RocketChatBot(botUser, botPass, server=server, ssl=False)

#Variables
roomIDs = {}      # Dictonary user -> roomId
players = set()   # Set for unique values
playerInfo = {}   # Dictonary user -> character
characters = ["Werwolf", "Dorfbewohner", "Dorfbewohner", "Dorfbewohner", "Seher", "Beschützer"]

def getUsers():
  users = bot.get("users.list")
  if users['data'] and len(users['data']) > 0:
    for user in users['data']['users']:
      print("User ", user['username'], user['_id'])
      roomIDs[user['username']] = user['_id']

def getChannels():
  groups = bot.get("groups.list")
  if groups['data'] and len(groups['data']) > 0:
    for group in groups['data']['groups']:
      print("Group ", group['name'], group['_id'])
      roomIDs[group['name']] = group['_id']
  
  channels = bot.get("channels.list")
  if channels['data'] and len(channels['data']) > 0:
    for channel in channels['data']['channels']:
      print("Channel ", channel['name'], channel['_id'])
      roomIDs[channel['name']] = channel['_id']

def createDirectChat(name):
  def storeRoom(error, data):
    if not error:
      roomIDs[name] = data['rid']
  if not name in roomIDs:
    bot.client.call('createDirectMessage', [name], storeRoom)

def createChannel(name):
  def storeRoom(error, data):
    if not error:
      roomIDs[name] = data['rid']
  if not name in roomIDs:
    bot.client.call('createChannel', [name, [botUser], False], storeRoom)

def createPrivateChat(name):
  def storeRoom(error, data):
    if not error:
      roomIDs[name] = data['rid']
  if not name in roomIDs:
    bot.client.call('createPrivateGroup', [name, []], storeRoom)

def deleteMessage(id):
  def deleteCallback(error, data):
    return
  bot.client.call('deleteMessage', [{'_id': id}], deleteCallback)

def updateMessage(message):
  def updateCallback(error, data):
    return
  bot.client.call('updateMessage', [message], updateCallback)

def listGroupMembers(group):
  return bot.get('groups.members?roomId=' + roomIDs[group])

def inviteToGroup(group, name):
  invite = {
    "roomId": roomIDs[group],
    "userId": roomIDs[name]
  }
  answer = bot.post('groups.invite', invite)
  print("LULULU Invite", answer)

def kickFromGroup(group, name):
  invite = {
    "roomId": roomIDs[group],
    "userId": roomIDs[name]
  }
  bot.post("groups.kick", invite)

def checkChannel(message, channel):
  return roomIDs[channel] == message['rid']

def isAlive(message):
  name = message['u']['username']
  return playerInfo[name]['alive'] == True

def startGame(bot, message): # Adding players
  global players
  if not checkChannel(message, 'Werwolf'):
    return
  
  sender = message['u']['username']
  players.add(sender)

  for name in message['mentions']:
    players.add(name['username'])

  names = ""
  for name in players:
    createDirectChat(name)
    names += "@" + name + " "
  
  message['msg'] = "[Werwolf] Spieler hinzugefügt: " + names
  updateMessage(message)


def resetGame(bot, message):  # Reset game
  global players
  if not checkChannel(message, 'Werwolf'):
    return
  
  players = set()

  bot.sendMessage(message['rid'], "[Werwolf] Re-Starting. Alle Spieler gelöscht. Starte ein neues Spiel mit \"Join\"")
  message['msg'] = "Spiel abbrechen"
  updateMessage(message)


def nextRound (bot, message):
  bot.sendMessage(message['rid'], "[Werwolf] Es wird Nacht in Cavallino und die Werwölfe treffen sich im #Wölfe chat.")


def setup (bot, message):  # Setup
  global players, playerInfo, characters
  if not checkChannel(message, 'Werwolf'):
    return
  
  createChannel("Werwolf")
  createPrivateChat('Woelfe')
  roomIDs['Werwolf'] = message['rid']

  if len(players) < 6:
    a = 6 - len(players)
    bot.sendMessage(message['rid'], "Zu wenig Spieler. Noch " + str(a) + " Spieler")
    return

  message['msg'] = "[Werwolf] Los geht's!"
  updateMessage(message)

  setupCharacters()

  playerInfo = {}
  for name in players:  
    playerInfo[name] = {
      "character": random.choice(characters),
      "alive": True
    }
    if playerInfo[name]['character'] == "Werwolf":
      inviteToChannel('Woelfe', name)
    
    characters.remove(playerInfo[name]['character'])
    bot.sendMessage(roomIDs[name], "[Werwolf] Deine Rolle: " + playerInfo[name]['character']) 

  nextRound(bot, message)


def setupCharacters():
  characters = ["Werwolf", "Dorfbewohner", "Dorfbewohner", "Dorfbewohner", "Seher", "Beschützer"]
  if len(players) >=7:
    characters.append("Dorfbewohner")
  if len(players) >=8:
    characters.append("Werwolf")
  if len(players) >=9:
    characters.append("Dorfbewohner")
  if len(players) >=10:
    characters.append("Werwolf")

def killVictim (bot, message):
  if checkChannel(message, 'Woelfe'):
    bot.sendMessage(message['rid'], "[Werwolf] Hier wird nicht gebissen")
    return
  
  if not isAlive(message):
    bot.sendMessage(message['rid'], "[Werwolf] Du bist schon tot")
    return
  
  if len(message['mentions']) != 1:
    bot.sendMessage(message['rid'], "[Werwolf] Wen wollt ihr beißen?")
    return

  name = message['mentions'][0]['username']
  if playerInfo[name]['alive'] == False:
    bot.sendMessage(message['rid'], "[Werwolf] Diser Spieler ist schon tot")
    return
  
  playerInfo[name]['alive'] = False
  bot.sendMessage(roomIDs['Werwolf'], "[Werwolf] " + name + " wurde gebissen")


def hangSuspect (bot, message): 
  name = message['mentions'][0]['username']
  playerInfo[name]['alive'] = False
  
  bot.sendMessage(message['rid'], "[Werwolf] " + name['username'] + "wurde gehängt")
  nextRound(bot, message)


bot.addPrefixHandler('rules', showHelpW)
bot.addPrefixHandler('help', showHelpW)
bot.addPrefixHandler('Rules', showHelpW)
bot.addPrefixHandler('Help', showHelpW)

bot.addPrefixHandler('Join', startGame)
bot.addPrefixHandler('join', startGame)

bot.addPrefixHandler('Go', setup)
bot.addPrefixHandler('go', setup)

bot.addPrefixHandler('Reset', resetGame)
bot.addPrefixHandler('reset', resetGame)
bot.addPrefixHandler('Restart', resetGame)
bot.addPrefixHandler('restart', resetGame)

bot.addPrefixHandler('Bite', killVictim)
bot.addPrefixHandler('bite', killVictim)

bot.addPrefixHandler('Hang', hangSuspect)
bot.addPrefixHandler('hang', hangSuspect)

def testi (bot, message):
  wolves = listGroupMembers('Woelfe')
  print("LULULU List ", wolves)

  # inviteToGroup('Woelfe', 'admin')
  kickFromGroup('Woelfe', 'admin')

bot.addPrefixHandler('test', testi)

def onLogin(data):
  getUsers()
  getChannels()
  createChannel("Werwolf")
  createPrivateChat('Woelfe')

bot.client.on('logged_in', onLogin)

bot.debug = False
bot.start()
