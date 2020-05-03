from rocketchat import RocketChatBot

class ChatBot(RocketChatBot):
    def __init__(self, user, password, server='open.rocket.chat', ssl=True):
        super().__init__(user, password, server, ssl)
    
        self.roomIDs = {} # Dictonary for caching chat ids

    def storeChannelId(self, name, id):
        self.roomIDs[name] = id
    
    def id(self, name):
        return self.roomIDs[name]

    def checkId(self, name, id):
        return self.roomIDs[name] == id

    def getUsers(self):
        users = self.get("users.list")
        if users and users['data'] and len(users['data']) > 0:
            for user in users['data']['users']:
                self.storeChannelId(user['username'], user['_id'])
                if self.debug:
                    print("User ", user['username'], user['_id'])

    def getGroups(self):
        groups = self.get("groups.list")
        if groups and groups['data'] and len(groups['data']) > 0:
            for group in groups['data']['groups']:
                self.storeChannelId(group['name'], group['_id'])
                if self.debug:
                    print("Group ", group['name'], group['_id'])
    
    def getChannels(self):
        channels = self.get("channels.list")
        if channels and channels['data'] and len(channels['data']) > 0:
            for channel in channels['data']['channels']:
                self.storeChannelId(channel['name'], channel['_id'])
                if self.debug:
                    print("Channel ", channel['name'], channel['_id'])

    def createDirectChat(self, name):
        def storeRoom(error, data):
            if not error:
                self.storeChannelId(name, data['rid'])
        if not name in self.roomIDs:
            self.client.call('createDirectMessage', [name], storeRoom)

    def createChannel(self, name):
        def storeRoom(error, data):
            if not error:
                self.storeChannelId(name, data['rid'])
        if not name in self.roomIDs:
            self.client.call('createChannel', [name, [botUser], False], storeRoom)

    def createPrivateChat(self, name):
        def storeRoom(error, data):
            if not error:
                self.storeChannelId(name, data['rid'])
        if not name in self.roomIDs:
            self.client.call('createPrivateGroup', [name, []], storeRoom)

    def listGroupMembers(self, group):
        return self.get('groups.members?roomId=' + self.roomIDs[group])

    def inviteToGroup(self, group, name):
        invite = {
            "roomId": self.roomIDs[group],
            "userId": self.roomIDs[name]
        }
        answer = self.post('groups.invite', invite)

    def kickFromGroup(self, group, name):
        invite = {
            "roomId": self.roomIDs[group],
            "userId": self.roomIDs[name]
        }
        self.post("groups.kick", invite)

    def deleteMessage(self, id):
        def deleteCallback(error, data):
            return
        self.client.call('deleteMessage', [{'_id': id}], deleteCallback)

    def updateMessage(self, message):
        def updateCallback(error, data):
            return
        self.client.call('updateMessage', [message], updateCallback)
