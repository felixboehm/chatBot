def showHelp(bot, message):
    helpText = """** HowTo Play "Werwolf” **
    Commands:
    `join` trete dem Spiel bei
    `join @player` lade dich und einen anderen Spieler ein
    `go` starte das Spiel
    `bite @player` Werwölfe töten ihr Opfer
    `hang @player` Dorfbewohner hängen den Verdächtigen
    `restart` stopt das Spiel und löscht alle Teilnehmer"""

    bot.sendMessage(message['rid'], helpText)