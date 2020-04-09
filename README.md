<<<<<<< HEAD
# Instructions for MindGame

Welcome to The Mind!
This is a community game, probably the most cooperative game of all. You must leave your individuality behind and think and act as one. Find the group consciousness!
About the rules:
There are cards from 1 to 100 inclusive.
Depending on the round, you each receive a corresponding number of cards. 1 each in the first round, 2 in the second, and so on.
Then you must discard your card(s), but in the correct overall order. 
The group has 3 lives, every time someone makes a mistake, one life is deducted.
You get one life added if you pass round 3, 6 and 9.
Good luck!

Commands:
- Play - join the game
- Play @user - invite yourself plus one or more players
- Start - starts the game    
- Pp - play your lowest card
- Reset - remove all players and stop a running game

# Rocket.Chat Python Bot Playground


Based on a Python Connector SDK for RocketChat Realtime API.
Thanks to https://github.com/diegodorgam/python-rocketchat-bot


## Development Setup for the bot 

Tested with python3.
- `pip3 install python-meteor`
- `pip3 install requests`
- `python3 run.py`


## Rocket.Chat Setup

Start a Rocket.Chat, if you don't have one already...
- `docker-compose up -d`

This will create a folder `data` for volume data, which you can delete after
- `docker-compose down`

If anything needs debugging, open logs
- `docker-compose logs -f`

Create user with Role Bot, and update the login in `run.py`
- username and password 
- your rocket.chat url:port

