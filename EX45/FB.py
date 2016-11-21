from sys import exit
from random import randint
import time


# a basic class for all "Character" related functions
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
    self.name = 'the Graphorn'
    self.health = randint(1, player.health)

#player information

def goeson():
    print "Your options are 'attack', 'flee', or 'quit'"
    while p.state != "normal":
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


class Player(Character):

      def __init__(self):
        Character.__init__(self)
        self.state = 'normal'
        self.health = 10
        self.health_max = 10

      def quit(self):
        print "%s can't find the way back home, and is shocked by a roaming spell in the fights\nR.I.P." % self.name
        self.health = 0
        quit()

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
          print "%s cautiously moves on" % self.name
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
        if self.state != 'fight': print "%s fires a spell into the air, without notable results." % self.name; self.tired()
        else:
          if self.do_damage(self.enemy):
            print "%s shock spells %s!" % (self.name, self.enemy.name)
            self.enemy = None
            self.state = 'normal'
            if randint(0, self.health) < 10:
              self.health = self.health + 1
              self.health_max = self.health_max + 1
              print "%s has become stronger" % self.name
          else: self.enemy_attacks()

      def enemy_attacks(self):
        if self.enemy.do_damage(self): print "%s was hit by a spell from the %s!!!\nR.I.P." %(self.name, self.enemy.name)

p = Player()
p.name = raw_input("""Welcome to the MACUSA-Office for the containment of Magicalbeasts. Please
#enter you name to procede!""")

#a basic input commandline just in case the player needs information
Commands = {
  'quit': Player.quit,
  'help': Player.help,
  'status': Player.status,
  'rest': Player.rest,
  'explore': Player.explore,
  'flee': Player.flee,
  'attack': Player.attack,
  }

#basic class for scene to utilize in functions
class Scene(object):

    def enter(self):
        print "Placeholder implement enter()."
        exit(1)


#engine for the map system used in planet percal

class Engine(object):

    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        current_scene = self.scene_map.opening_scene()
        last_scene = self.scene_map.next_scene('finished')

        while current_scene != last_scene:
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)

        current_scene.enter()


#a default gameOver Scene
class gameOver(Scene):

    def enter(self):
        print "You have failed."
        exit(1)


#opening scene one out of two central crossroads

class IntroScene(Scene):

    def enter(self):
        if 1:
            print "is attacked by the Augury"
            p.enemy = Enemy(p)
            p.state = 'fight'
            p.enemy_attacks()
            goeson()
        else:
            return 'avenue'


#1. Szene
class Entrance(Scene):

    def enter(self):
        print "Good morning %s" % p.name
        print "You have two important meetings today."
        print "Do you prefer to go to your office first or meet with"
        print "president Picquery right away?"

        action = raw_input("> ")

        if action == "meet":
            print "The telephonecell you entered starts to rotate around you"
            print "A second later you are transported by the fleepowdernetwork"
            print "in the hallway to Mrs Picquery's office"
            return 'picquery'

        elif action == "office":
            print "The telephonecell you entered starts to rotate around you"
            print "Just a brief moment later you arive at your office."
            return 'office'

        else:
            print "Please repeat your request and speak loud and clearly."
            print "meet or office?"
            return 'office'

class Picquery(Scene):

    def enter(self):
        print "As you stand in front of the office door you notice that there"
        print "Is still soot on your robe."
        print "Do you clean it of before you enter?"
        return 'picquery_office'

        action = raw_input("> ")

        if action == "clean":
            print "You clean yourself of and walk in after politly knocking"
            print "on the door."
            return 'picquery_office'

        elif action == "enter":
            print "You enter the president's office without cleaning your robe."
            print "Hello %s" % p.name
            print "You look unpleasent today.. you realize this is the president's"
            print "office you just walked into right?"
            return 'picquery_office'

        else:
            print "That would make no sense here enter or clean?"
            return 'picquery_office'

class PicqueryOffice(Scene):

    def enter(self):
        print "Hello %s" % p.name
        print "We have bad news there has been an article 3A we need all Aurors"
        print "in Mr Graves office asap!"
        return 'graves'

class Office(Scene):

    def enter(self):
        print "There is y huge pile of paperwork left from yesterday"
        print "as well as new mail arriving continously through the"
        print "magical in house delivery service."
        time.sleep(4)
        print "It knocks and before you can respond a seemingly shocked"
        print "woman enters"
        print "There has been an article 3 A in the 32th avenue every"
        print "Auror has to report to Mister Graves immediatly!"
        print "Do you follow her right away or do you want to ask questions first?"

        action = raw_input("> ")

        if action == "questions":
            print "What is it %s we have to report to Graves asap!?" % p.name

        elif action == "follow":
            print "Both of you head out onto Graves' office"
            return 'graves'

        else:
            print "We don't have time for this %s" % p.name

class Graves(Scene):

    def enter(self):
        print "As you enter Graves office all the other Aurors are already gathered up."
        print "And ready to head out on the the 32th avenue."
        print "You and the the small witch called Berta who entered you office before"
        print "you join them for the briefing."
        return 'avenue'


class Avenue(Scene):


    def enter(self):
        if 1:
            print "is attacked by the Augury"
            p.enemy = Enemy(p)
            p.state = 'fight'
            p.enemy_attacks()
            goeson()
        else:
            return 'avenue'

        print " --------------- Chapter ONE 1 ----------------"
        print "As you have been told Mister Newt Scamander is on the look out for two of his magical beasts"
        print "that incidentally went lose the Augury and one of the last two breading"
        print "Graphorns, which is why you know have to capture him and bring him into custody."


        print "You find yourself running into Ms Scamander as he apparats right in front"
        print "of you on the 32th street as you leave your office."
        print "Attack him(1), try to capture(2) him or try talking to him(3)?"

        action = raw_input("> ")

        if action == "1":
            print "Scamander deflects your spell"
            print "and hits you with the stupor spell."
            return 'game_over'

        elif action == "2":
            print "Scamander evades your spell and disappartes"
            return 'game_over'

        elif action == "3":
            print "After interrogating Mrs Scamander he follows you to the MACUSA"
            print "office in exchange for the protection of his magical beasts."
            return 'finished'

        else:
            print "You are clearly talking nonsense"
            return 'avenue'


class Finished(Scene):

    def enter(self):
        print "You did it the creatures are save."
        return 'finished'

class Map(object):

    scenes = {
        'intro_scene': IntroScene(),
        'avenue': Avenue(),
        'game_over': gameOver(),
        'finished': Finished(),
        'entrance': Entrance(),
        'office': Office(),
        'picquery': Picquery(),
        'graves': Graves(),
        'picquery_office': PicqueryOffice(),
    }

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        val = Map.scenes.get(scene_name)
        return val

    def opening_scene(self):
        return self.next_scene(self.start_scene)

a_map = Map('entrance')
a_game = Engine(a_map)
a_game.play()
