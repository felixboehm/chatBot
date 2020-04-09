from rocketchat import RocketChatBot, RocketChatClient
from time import sleep
import random
from instructions import showHelp

bot = RocketChatBot('botty','botty',server='localhost:3000',ssl=False)

roomIDs = {}      # Dictonary user -> roomId
gameRunning = False
players = set()   # Set for unique values
cards = {}
livesMax = 3
lives = livesMax
phase = 0
phases = {}
phases[1] = {"name": "Improved sensibility", "bonus": "none"}
phases[2] = {"name": "Increased empathy", "bonus": "star"}
phases[3] = {"name": "Widened awareness", "bonus": "live"}
phases[4] = {"name": "Sub-cognitive perception", "bonus": "none"}
phases[5] = {"name": "Group consciousness", "bonus": "star"}
phases[6] = {"name": "Mind perception", "bonus": "live"}
phases[7] = {"name": "Telepathic communication", "bonus": "none"}
phases[8] = {"name": "Out-of-body presence", "bonus": "star"}
phases[9] = {"name": "Quantum Awareness", "bonus": "live"}
phases[10] = {"name": "Separation from the space-time continuum", "bonus": "none"}
phases[11] = {"name": "Metaphysical Harmony", "bonus": "none"}
phases[12] = {"name": "Fusion of spirit and matter", "bonus": "none"}

def createDirectChat(user):
  def storeRoom(error, data):
    if not error:
      roomIDs[user] = data['rid']
  
  bot.client.call('createDirectMessage', [user], storeRoom)

def deleteMessage(id):
  def deleteCallback(error, data):
    return
  
  bot.client.call('deleteMessage', [{'_id': id}], deleteCallback)

def updateMessage(message):
  def updateCallback(error, data):
    return
  
  bot.client.call('updateMessage', [message], updateCallback)

def startGame(bot, message):
  global lives, livesMax, phase, players, cards, gameRunning  
  if gameRunning == False:  
    gameRunning = True
    phase = 0
    lives = livesMax
    players = set()
    cards = {}
  
  sender = message['u']['username']
  players.add(sender)

  for name in message['mentions']:
    players.add(name['username'])

  names = ""
  for name in players:
    createDirectChat(name)
    names += "@" + name + " "
  
  # bot.sendMessage(message['rid'], "[Mind] Added players: " + names)
  # deleteMessage(message['_id'])
  message['msg'] = "added players: " + names
  updateMessage(message)

def nextPhase(bot, message):
  global phase, gameRunning
  roomId = message['rid']
  deleteMessage(message['_id'])

  if gameRunning == False:
    bot.sendMessage(roomId, "[Mind] Please start game first using \"Play\"")
    return
  if len(players) < 2:
    bot.sendMessage(roomId, "[Mind] Playing alone? :nerd: Please add more players with \"Play\"")
    return
  
  phase += 1
  deck = list(range(1,101))
  
  for name in players:
    cards[name] = random.sample(deck, phase)
    cards[name].sort()
    for card in cards[name]:
      deck.remove(card)
  
    bot.sendMessage(roomIDs[name], "[Mind] Round " + str(phase) + ": Your Cards are")
    bot.sendMessage(roomIDs[name], str(cards[name]))
  bot.sendMessage(roomId, "[Mind] Starting Round " + str(phase) + " \"" + phases[phase]["name"] + "\"")

def playCard(bot, message):
  global lives, phase, gameRunning
  roomId = message['rid']
  sender = message['u']['username']

  if gameRunning == False:
    bot.sendMessage(roomId, "[Mind] Please start game first using \"Play\"")
    return
  
  card = cards[sender].pop(0)   #TODO: concurrent card removing throws error (pop from empty list)
  message['msg'] = str(card) + " played"
  updateMessage(message)

  # bot.sendMessage(roomId, "sender + " plays card: " + str(card))
  for name in players:
    remainingCards = list(cards[name])
    for x in remainingCards:
      if x < card:
        lives -= 1
        bot.sendMessage(roomId, "[Mind] " + name + " too slow: " + str(x) + " :cry: " + str(lives) + " lives remaining")
        cards[name].remove(x)

  remaining = 0
  for name in players:
    remaining += len(cards[name])

  if lives <= 0:      # Game Over ?
    bot.sendMessage(roomId, "[Mind] Game over! :zany_face:")
    gameRunning = False

  if remaining <= 0:  # Phase finished ?
    bot.sendMessage(roomId, "[Mind] Round finished! ")
    
    bonusCheck = phases[phase]["bonus"]     # Check Bonus
    if bonusCheck == "live":
      lives += 1
      bot.sendMessage(roomId, "[Mind] You got a bonus live :+1:" + str(lives) + " lives remaining")
    
    bot.sendMessage(roomId, "Starting next round with " + str(lives) + " lives :innocent:" )
    sleep(2)

def resetGame(bot, message):
  global gameRunning
  gameRunning = False
  bot.sendMessage(message['rid'], "[Mind] Re-Starting. All players removed. Please start a new game using \"Play\"")
  message['msg'] = "aborted the game"
  updateMessage(message)


bot.addPrefixHandler('rules', showHelp)
bot.addPrefixHandler('help', showHelp)
bot.addPrefixHandler('Rules', showHelp)
bot.addPrefixHandler('Help', showHelp)
bot.addPrefixHandler('Play', startGame)
bot.addPrefixHandler('play', startGame)
bot.addPrefixHandler('Start', nextPhase)
bot.addPrefixHandler('start', nextPhase)
bot.addPrefixHandler('Pp', playCard)
bot.addPrefixHandler('pp', playCard)
bot.addPrefixHandler('Reset', resetGame)
bot.addPrefixHandler('reset', resetGame)
bot.addPrefixHandler('Restart', resetGame)
bot.addPrefixHandler('restart', resetGame)

bot.start()
