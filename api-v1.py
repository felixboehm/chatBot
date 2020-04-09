from rocketchat import RocketChatBot, RocketChatClient

host = 'localhost:3000'
user = "botty"
password = "12345"
bot = RocketChatBot(user, password, server=host, ssl=False)

def wolf(bot, message):
  groups = bot.get("groups.list")
  for group in groups['data']['groups']:
    print("LULULU Groups ", group['name'], group['_id'])

  users = bot.get("users.list")
  for user in users['data']['users']:
    print("LULULU Users ", user['name'], user['_id'])

  invite = { 
    "roomId": "Cz9BHLq6e3gAieQtC",
    "userId": "GQxjDym8GMAW8oDN2"
  }
  print("LULULU Invite ", invite)
  answer = bot.post("groups.invite", invite)
  
  print("LULULU Invite", answer['data'])

def unwolf(bot, message):
  kick = { 
    "roomId": "Cz9BHLq6e3gAieQtC",
    "userId": "GQxjDym8GMAW8oDN2"
  }
  print("LULULU Kick ", kick)
  answer = bot.post("groups.kick", kick)
  
  print("LULULU Kick", answer['data'])

bot.addPrefixHandler('wolf', wolf)
bot.addPrefixHandler('unwolf', unwolf)

bot.start()
