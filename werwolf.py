import time
import random
from chatbot import ChatBot
# from playerlist import PlayerList
from instructionsWW import showHelp

server = 'localhost:3000'
botUser = 'botty'
botPass = 'botty'

CHANNEL_WOLF = 'Woelfe'
CHANNEL_PLAYER = 'Werwolf'

players = set()   # Set for unique values
playerInfo = {}   # Dictonary user -> character

def removeWolves(bot):
  wolves = bot.listGroupMembers(CHANNEL_WOLF)
  for member in wolves['data']['members']:
    name = member['username']
    if name != 'botty':
      bot.kickFromGroup(CHANNEL_WOLF, name)

def setupInfo():
  return {
    "character": "?",
    "alive": True
  }

def setupCharacters(bot):
  global players, playerInfo
  characters = ["Werwolf", "Dorfbewohner", "Dorfbewohner", "Dorfbewohner", "Seher", "Beschützer"]
  if len(players) >=7:
    characters.append("Dorfbewohner")
  if len(players) >=8:
    characters.append("Werwolf")
  if len(players) >=9:
    characters.append("Dorfbewohner")
  if len(players) >=10:
    characters.append("Werwolf")
  
  playerInfo = {}
  removeWolves(bot)

  for name in players:
    playerInfo[name] = setupInfo()
    playerInfo[name]['character'] = random.choice(characters)
    if playerInfo[name]['character'] == "Werwolf":
      bot.inviteToGroup(CHANNEL_WOLF, name)
    
    characters.remove(playerInfo[name]['character'])
    bot.sendMessage(bot.id(name), "[Werwolf] Deine Rolle: " + playerInfo[name]['character']) 

def isAlive(name):
  return playerInfo[name]['alive'] == True

### COMMANDS ###

def addPlayers(bot, message): # Adding players
  global players, playerInfo
  if not bot.checkId(CHANNEL_PLAYER, message['rid']):  # Written in channel CHANNEL_PLAYER?
    return
  
  sender = message['u']['username']   # Add sender of 'start' to players
  players.add(sender)
  playerInfo[sender] = setupInfo()

  for user in message['mentions']:   # Add all mentions to players
    name = user['username']
    players.add(name)
    playerInfo[name] = setupInfo()

  names = ""
  for name in players:   # Creates direct Chat with all players
    bot.createDirectChat(name)
    names += "@" + name + " "
  
  message['msg'] = "[Players] Spieler hinzugefügt: " + names
  bot.updateMessage(message)


def resetGame(bot, message):  # Reset game
  global players, playerInfo
  if not bot.checkId('Werwolf', message['rid']):
    return

  players = set()
  setupCharacters(bot)

  bot.sendMessage(bot.id(CHANNEL_PLAYER), "[Werwolf] Re-Starting. Tritt der nächsten Runde bei mit: 'join [@user]'")
  message['msg'] = "Spiel abbrechen"
  bot.updateMessage(message)


def nextRound (bot, message):
  bot.sendMessage(bot.id(CHANNEL_PLAYER), "[Werwolf] Es wird Nacht in Cavallino und die Werwölfe treffen sich im #" + CHANNEL_WOLF + " chat.")
  bot.sendMessage(bot.id(CHANNEL_WOLF), "[Werwolf] Wählt aus: 'bite @username'")

def setup(bot, message):  # Setup
  global players, playerInfo
  if not bot.checkId('Werwolf', message['rid']):
    return

  bot.storeChannelId('Werwolf', message['rid'])

  if len(players) < 6:
    a = 6 - len(players)
    bot.sendMessage(message['rid'], "Zu wenig Spieler. Noch " + str(a) + " Spieler")
    return

  message['msg'] = "[Werwolf] Los geht's!"
  bot.updateMessage(message)

  setupCharacters(bot)
  nextRound(bot, message)

def killVictim(bot, message):
  if not bot.checkId(CHANNEL_WOLF, message['rid']):   # Correct channel?
    bot.sendMessage(message['rid'], "[Werwolf] Hier wird nicht gebissen")
    return
  
  if len(message['mentions']) != 1:   # Only/at least one mentioned?
    bot.sendMessage(message['rid'], "[Werwolf] Wen wollt ihr beißen?")
    return
  
  name = message['mentions'][0]['username']   # Player to kill alive?
  print(name)
  print(playerInfo)
  if playerInfo[name]['alive'] == False:
    bot.sendMessage(message['rid'], "[Werwolf] Diser Spieler ist schon tot")
    return
  
  playerInfo[name]['alive'] = False
  bot.sendMessage(bot.id('Werwolf'), "[Werwolf] Ein neuer Tag in Cavallino. " + name + " wurde gebissen")
  bot.sendMessage(bot.id('Werwolf'), "[Werwolf] " + name + " war " + playerInfo[name]['character'])

  if playerInfo[name]['character'] == 'Werwolf':   # Kickgroup if WerwolCHANNEL_WOLFSf
    bot.kickFromGroup(CHANNEL_WOLF, name)

  if endCheck(bot, message):
    return

  time.sleep(2)
  bot.sendMessage(bot.id('Werwolf'), "[Werwolf] Entscheidet nun gemeinsam wen ihr hängen wollt.")

def hangSuspect(bot, message): 
  if not bot.checkId('Werwolf', message['rid']):   # Correct channel?
    bot.sendMessage(message['rid'], "[Werwolf] Falscher Channel. Spiele Werwolf in #" + CHANNEL_PLAYER)
    return
  
  sender = message['u']['username']   # Writer alive?
  if not isAlive(sender):
    bot.sendMessage(bot.id(CHANNEL_PLAYER), "[Werwolf] Du bist schon tot")
    return

  if len(message['mentions']) != 1:   # Only/at least one mentioned?
    bot.sendMessage(bot.id(CHANNEL_PLAYER), "[Werwolf] Wen wollt ihr hängen?")
    return

  name = message['mentions'][0]['username']   # Player to hang alive?
  if playerInfo[name]['alive'] == False:
    bot.sendMessage(bot.id(CHANNEL_PLAYER), "[Werwolf] Diser Spieler ist schon tot")
    return

  name = message['mentions'][0]['username']
  playerInfo[name]['alive'] = False
  
  if playerInfo[name]['character'] == 'Werwolf':   # Kick from group if Werwolf
    bot.kickFromGroup(CHANNEL_WOLF, name)

  bot.sendMessage(bot.id(CHANNEL_PLAYER), "[Werwolf] " + name + " wurde gehängt")
  bot.sendMessage(bot.id(CHANNEL_PLAYER), "[Werwolf] " + name + " war " + playerInfo[name]['character'])

  if endCheck(bot, message):
    return
  
  time.sleep(2)
  nextRound(bot, message)

def endCheck(bot, message): 
  aliveCount = 0
  wolfsCount = 0
  othersCount = 0

  for player in players:
    if playerInfo[player]['alive']:
        aliveCount += 1
        if playerInfo[player]['character'] == "Werwolf":
            wolfsCount += 1
        else:
            othersCount += 1

  if wolfsCount == 0:
    bot.sendMessage(bot.id(CHANNEL_PLAYER), "[Werwolf] Die Dorfbewohner haben gewonnen, alle Werwölfe sind tot!")
    resetGame(bot, message)
    return True
  
  if othersCount == 0:
    bot.sendMessage(bot.id(CHANNEL_PLAYER), "[Werwolf] Die Werwölfe haben gewonnen, alle Dorfbewohner wurden getötet!")
    resetGame(bot, message)
    return True
  
  return False

def makeMeWolf(bot, message):
  global playerInfo
  if not bot.checkId(CHANNEL_PLAYER, message['rid']):
    return
  removeWolves(bot)
  sender = message['u']['username']
  character = playerInfo[sender]['character']
  playerInfo[sender]['character'] = "Werwolf"
  bot.inviteToGroup(CHANNEL_WOLF, sender)
  for name in players:
    if playerInfo[name]['character'] == "Werwolf" and name != sender:
      playerInfo[name]['character'] = character
      return

def addall(bot, message):
  global players, playerInfo
  if not bot.checkId(CHANNEL_PLAYER, message['rid']):
    return
  players = set(['admin', 'felix', 'tina', 'user1', 'user2', 'user3'])
  for name in players:
    playerInfo[name] = setupInfo()
  bot.sendMessage(bot.id(CHANNEL_PLAYER), "[Players] " + str(len(players)))

def listPlayers(bot, message):
  global players, playerInfo
  if not bot.checkId(CHANNEL_PLAYER, message['rid']):
    return
  bot.sendMessage(bot.id(CHANNEL_PLAYER), "[Players] " + str(len(players)))
  for name in players:
    s = "[Players]"
    if playerInfo[name] and playerInfo[name]['alive']:
      s += " :innocent: "
    else:
      s += " :ghost: "
    # if playerInfo[name] and playerInfo[name]['character']:
    #   s += " is a " + str(playerInfo[name]['character'])
    bot.sendMessage(bot.id(CHANNEL_PLAYER), s + name)
  
def main():
  bot = ChatBot(botUser, botPass, server=server, ssl=False)
  bot.debug = False

  def onLogin(data):
    bot.getUsers()
    bot.getGroups()
    bot.getChannels()
    bot.createChannel(CHANNEL_PLAYER)
    bot.createPrivateChat(CHANNEL_WOLF)
    removeWolves(bot)

  bot.client.on('logged_in', onLogin)
  
  bot.addPrefixHandler('wolf', makeMeWolf)
  bot.addPrefixHandler('addall', addall)
  bot.addPrefixHandler('list', listPlayers)

  bot.addPrefixHandler('rules', showHelp)
  bot.addPrefixHandler('help', showHelp)
  bot.addPrefixHandler('Rules', showHelp)
  bot.addPrefixHandler('Help', showHelp)

  bot.addPrefixHandler('Join', addPlayers)
  bot.addPrefixHandler('join', addPlayers)

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

  bot.start()

if __name__ == '__main__':
  main()