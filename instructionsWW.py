def showHelpW(bot, message):
    helpText = """** HowTo Play "Werwolf” **
    Commands:
    `Join` trete dem Spiel bei
    `Join @player` lade dich und einen anderen Spieler ein
    `Go` starte das Spiel
    `bite @player` Werwölfe töten ihr Opfer
    `hang @player` Dorfbewohner hängen den Verdächtigen
    `restart` stopt das Spiel und löscht alle Teilnehmer"""

    bot.sendMessage(message['rid'], helpText)