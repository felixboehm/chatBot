class PlayerList:
  def __init__(self):
    self.names = set()
    self.infos = {}
  
  def add(self, name):
    self.names.add(name)
    self.infos['alive'] = True
  
  def remove(self, name):
    self.names.remove(name)

  def removeAll(self):
    self.names = set()
  
  def count(self):
    return len(names)

  def countAlive(self):
    alive = 0
    for name in names:
      if info[name]['alive'] == True:
        alive += 1
    return alive
  
  def isAlive(self, name):
    return self.infos[name]['alive'] == True
  
  def kill(self, name):
    self.infos[name]['alive'] = False

  def set(self, name, attr, value):
    self.infos[name][attr] = value
  
  def get(self, name, attr):
    return self[name][attr]
