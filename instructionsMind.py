def showHelp(bot, message):
    helpText = """** HowTo Play "The Mind” **
    Commands:
    `Play` join the game
    `Play @user` invite yourself plus one or more players
    `Start` starts the game
    `Pp` play your lowest card
    `Reset` remove all players and stop a running game"""

    bot.sendMessage(message['rid'], helpText)

