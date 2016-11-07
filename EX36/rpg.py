from random import randint
import time
import random
print ""
print "H M S - Zombie"
print ""


class Character:
  def __init__(self):
    self.name = ""
    self.health = 1
    self.health_max = 1
  def do_damage(self, enemy):
    damage = min(
        max(randint(0, self.health) - randint(0, enemy.health), 0),
        enemy.health)
    enemy.health = enemy.health - damage
    if damage == 0: print "%s dodges %s's attack." % (enemy.name, self.name)
    else: print "%s hurts %s!" % (self.name, enemy.name)
    return enemy.health <= 0

class Enemy(Character):
  def __init__(self, player):
    Character.__init__(self)
    self.name = 'a Zombie'
    self.health = randint(1, player.health)

class Player(Character):
  def __init__(self):
    Character.__init__(self)
    self.state = 'normal'
    self.health = 10
    self.health_max = 10
  def quit(self):
    print "%s can't find the way back home, and is overwhelmed by the zombie hords.\nR.I.P." % self.name
    self.health = 0
  def help(self): print Commands.keys()
  def status(self): print "%s's health: %d/%d" % (self.name, self.health, self.health_max)
  def tired(self):
    print "%s feels tired." % self.name
    self.health = max(1, self.health - 1)
  def rest(self):
    if self.state != 'normal': print "%s can't rest now!" % self.name; self.enemy_attacks()
    else:
      print "%s rests." % self.name
      if randint(0, 1):
        self.enemy = Enemy(self)
        print "%s is rudely awakened by %s!" % (self.name, self.enemy.name)
        self.state = 'fight'
        self.enemy_attacks()
      else:
        if self.health < self.health_max:
          self.health = self.health + 1
        else: print "%s slept too much." % self.name; self.health = self.health - 1
  def explore(self):
    if self.state != 'normal':
      print "%s is too busy right now!" % self.name
      self.enemy_attacks()
    else:
      print "%s cautiously moves down the hallway." % self.name
      if randint(0, 1):
        self.enemy = Enemy(self)
        print "%s encounters %s!" % (self.name, self.enemy.name)
        self.state = 'fight'
      else:
        if randint(0, 1): self.tired()
  def flee(self):
    if self.state != 'fight': print "%s runs in circles for a while." % self.name; self.tired()
    else:
      if randint(1, self.health + 5) > randint(1, self.enemy.health):
        print "%s flees from %s." % (self.name, self.enemy.name)
        self.enemy = None
        self.state = 'normal'
      else: print "%s couldn't escape from %s!" % (self.name, self.enemy.name); self.enemy_attacks()
  def attack(self):
    if self.state != 'fight': print "%s swats the air, without notable results." % self.name; self.tired()
    else:
      if self.do_damage(self.enemy):
        print "%s executes %s!" % (self.name, self.enemy.name)
        self.enemy = None
        self.state = 'normal'
        if randint(0, self.health) < 10:
          self.health = self.health + 1
          self.health_max = self.health_max + 1
          print "%s has become even more ruthless" % self.name
      else: self.enemy_attacks()
  def enemy_attacks(self):
    if self.enemy.do_damage(self): print "%s was bitten by %s!!!\nR.I.P." %(self.name, self.enemy.name)



Commands = {
  'quit': Player.quit,
  'help': Player.help,
  'status': Player.status,
  'rest': Player.rest,
  'explore': Player.explore,
  'flee': Player.flee,
  'attack': Player.attack,
  }

p = Player()
p.name = raw_input("Hello, welcome to HMS-Z what is your name?")
print "(type help to get a list of actions)\n"
print "It is tuesday morining and you are AGAIN running late!"
print "As you are riding your bike as fast a you can"
print "you don't even take note of the streets being unusally"
print "empty for it being that early in the day."
print ""
print "After running couple of red lights you finally reach HMS"
print "and leave your bike at the front door."
print ""
time.sleep (15)
print "hmm that's really strange.."
time.sleep (3)
print "There is still nobody around not even on campus.. for a brief moment you hesitate"
time.sleep (3)

def choosePath () :
    path = ""
    while path != "1" and path != "2":
        path = input ("Are you going to take the stairs (1) or the elevator (2)? (1 or 2): ")

        return path

def checkPath (chosenPath) :
    print "You shrug of the hesitation and head on to class"

    correctPath = random.randint(1, 2)

    if chosenPath == str(correctPath) :
        print "You reach the second floor"
        print "Sweet almost there!"
    else:
        print "But as you enter the hallway you hear a fearinducing noise..."
        print "(type help to get a list of actions)\n"

choice = choosePath ()
checkPath (choice)

while(p.health > 0):
  line = raw_input("> ")
  args = line.split()
  if len(args) > 0:
    commandFound = False
    for c in Commands.keys():
      if args[0] == c[:len(args[0])]:
        Commands[c](p)
        commandFound = True
        break
    if not commandFound:
      print "%s doesn't understand the suggestion." % p.name
