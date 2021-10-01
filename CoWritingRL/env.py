import numpy as np
import time
import random
from collections import defaultdict
from state import State
from format import Format

class CoWriting:
  #environment class goes here
  def __init__(self, gender, adapt_to_gender = False):
    self.gender = gender
    self.adapt_to_gender = adapt_to_gender
    self.letters = np.zeros(26)         # list of letters: assigned to zeros for unexplored letters, ones for explored letters. Later override for kazakh alphabet
#    self.score = 0                      # will indicate whether there is a problematic letter that is still not learned.
    self.time_elapsed = 0               # time spent by student to write a recent word
    self.time_total = 0                 # overall time for all words in one episode
    self.list_of_lists = []             # list of all given words
    self.list1 = ['girl', 'princess', 'crown', 'ring', 'yogurt', 'alice', 'barbi', 'doll', 'elza', 'frozen', 'ginger', 'hermione', 'izabella', 'jewellery', 'kpop', 'lady', 'moana', 'nurse', 'princess', 'qpop', 'silk', 'tangled', 'umbrella', 'violet', 'wanda', 'xavier', 'zara']   # will be updated
    self.list_of_lists.append(self.list1)
    self.list2 = ['boy', 'hero', 'sword', 'shield', 'yoyo', 'archer', 'cool', 'dagger', 'ghost', 'elf', 'helmet', 'ironman', 'joker', 'falcon', 'kick', 'loki', 'megamind', 'neutron', 'omnitrix', 'power', 'robin', 'spiderman', 'tank', 'unit','qazaq', 'vulverine', 'werewolf', 'xmen', 'zorro']
    self.list_of_lists.append(self.list2)
    self.list3 = ['animal', 'tiger', 'deer', 'elephant', 'bird', 'crocodile', 'frog', 'horse', 'goose', 'iguana', 'jeiran', 'kitty', 'lion', 'monkey', 'narnia', 'ostrix', 'pantera', 'qazaqstan', 'rhino', 'snake', 'utka', 'vorona', 'wolf', 'xmen', 'young', 'zebra' ]
    self.list_of_lists.append(self.list3)
    self.counter = 1                     # count words (if 10 -> new episode)
    self.actions_codes = ["keep the theme and keep learning the problematic letter", "keep the theme and explore words with new letters", "change the theme and keep learning the problematic letter", "change the theme and explore words with new letters", "ask advice from adult"]
    self.errors = []

 # this is a method for assessing a word to a student. Provide a word and wait him/her to rewrite it. Also count time for response
  def interact(self):
    print(self.word)
    start_time = time.time()
    user_word = input("Please, write this word: ")
    end_time = time.time()
    time_lapsed = end_time - start_time
    return user_word, time_lapsed


  def start(self):
    if self.adapt_to_gender:        # if True -> apply predefined advice (apply specific theme for gender)
      print("predefined advice is on")
      if self.gender == 0:
        self.theme = 0
      elif self.gender == 1:
        self.theme = 1
      else:
        self.theme = 2
    else:
      print("predefined advice is off")
      self.theme = random.randint(0,len(self.list_of_lists)-1)
    if self.theme == 0:
      print("theme: GIRLS was selected")
    elif self.theme == 1:
      print("theme: BOYS was selected")
    else:
      print("theme: ANIMALS was selected")
  

    # select a random word in the given theme
    word_index = random.randint(0,len(self.list_of_lists[self.theme])-1)
    self.word = self.list_of_lists[self.theme][word_index]
    print("selected word: " + self.word)

    # indicate explored letters
    for c in self.word:
      self.letters[ord(c) - ord('a')] = 1
    print("updated list of remaining letters to explore:")
    for idx in range(len(self.letters)):
      if self.letters[idx] == 0:
        print(chr(idx + ord('a')), end = " ")
    print("")
    


    # show the word to student, receive his/her response
    self.time_total = 0
    print(">>>>>interaction with student begins")
    user_word, self.time_elapsed = self.interact()
    print(">>>>>interaction with student stops")
    self.time_total = self.time_total + self.time_elapsed

    # record errors of  the student 
    for i in range(len(self.word)):
      if (self.word[i] != user_word[i]): 
        print(Format.underline + self.word[i] + Format.end, end = "")  
        if self.word[i] not in self.errors: # important, don't store duplicates!!! Shamil, attention!!!
          self.errors.append(self.word[i])
      else:
        print(self.word[i], end ="") 
    print("problematic letters:")
    for letter in self.errors:
      print(letter, end = " ")
   #   self.score = self.score + 1
    print("")

    self.counter = self.counter + 1


    state = State(26 - np.count_nonzero(self.letters), self.time_total, self.time_elapsed, len(self.errors), self.theme, self.gender)
    state.print_info()
    return state


  def step(self, action):
    # actions implementations here
    done = False
    changed = False
    print("action selected: " + self.actions_codes[action])
    
    if action == 0:
      if not self.errors:
        action = 1
        changed = True
        print("action was changed to " + self.actions_codes[action])
      else:
        tmp = [idx for idx in self.list_of_lists[self.theme] if idx[0].lower() in self.errors]
        self.word = random.choice(tmp)
        print("next selected word: " + self.word + " resolves problematic letter " + self.word[0])
        self.errors.remove(self.word[0])
        print("remaining problematic letters: ")
        print(self.errors)
  #      self.score = self.score - 1
        for c in self.word:
          self.letters[ord(c) - ord('a')] = 1
        print("updated list of remaining letters to explore:")
        for idx in range(len(self.letters)):
          if self.letters[idx] == 0:
            print(chr(idx + ord('a')), end = " ")
        print("")
 
    if action == 1:
      tmp = [idx for idx in self.list_of_lists[self.theme] if self.letters[ord(idx[0].lower()) - ord('a')] == 0]
      self.word = random.choice(tmp)
      print("next selected word: " + self.word)
      for c in self.word:
        self.letters[ord(c) - ord('a')] = 1
      print("updated list of remaining letters to explore:")
      for idx in range(len(self.letters)):
        if self.letters[idx] == 0:
          print(chr(idx + ord('a')), end = " ")
      print("")
    
    if action == 2:
      if not self.errors:
        action = 3
        changed = True
        print("action was changed to " + self.actions_codes[action])
      else:
        print("theme changed from " + str(self.theme), end = " ")
        self.theme = random.randint(0, 2)
        print("to " + str(self.theme))
        tmp = [idx for idx in self.list_of_lists[self.theme] if idx[0].lower() in self.errors]
        self.word = random.choice(tmp)
        print("next selected word: " + self.word + " resolves problematic letter " + self.word[0])
        self.errors.remove(self.word[0])
  #      self.score = self.score - 1
        for c in self.word:
          self.letters[ord(c) - ord('a')] = 1
        print("updated list of remaining letters to explore:")
        for idx in range(len(self.letters)):
          if self.letters[idx] == 0:
            print(chr(idx + ord('a')), end = " ")
        print("")
    
    if action == 3:
      print("theme changed from " + str(self.theme), end = " ")
      self.theme = random.randint(0, 2)
      print("to " + str(self.theme))
      tmp = [idx for idx in self.list_of_lists[self.theme] if self.letters[ord(idx[0].lower()) - ord('a')] == 0]
      self.word = random.choice(tmp)
      print("next selected word: " + self.word)
      for c in self.word:
        self.letters[ord(c) - ord('a')] = 1
      print("updated list of remaining letters to explore:")
      for idx in range(len(self.letters)):
        if self.letters[idx] == 0:
          print(chr(idx + ord('a')), end = " ")
      print("")
    
    # ask advice
    if action == 4:
      bool_var = 0
      while bool_var == 0:
        word = input("Please, help me! Which word should we try?")
        for t in range(len(self.list_of_lists) - 1):
          if word in self.list_of_lists[t]:
            self.word = word
            self.theme = t
            print("theme identified: " + str(self.theme))
            for c in self.word:
              self.letters[ord(c) - ord('a')] = 1
            print("updated list of remaining letters to explore:")
            for idx in range(len(self.letters)):
              if self.letters[idx] == 0:
                print(chr(idx + ord('a')), end = " ")
            print("")
            bool_var = 1

    print(">>>>>interaction with student begins")
    user_word, self.time_elapsed = self.interact()
    print(">>>>>interaction with student stops")
    self.time_total = self.time_total + self.time_elapsed

    for i in range(len(self.word)):
      if (self.word[i] != user_word[i]):   
        print(Format.underline + self.word[i] + Format.end, end = "")
        if self.word[i] not in self.errors:  # important, don't store duplicates!!! Shamil, attention!!!
          self.errors.append(self.word[i])
      else:
        print(self.word[i], end ="")
    print("")
    print("problematic letters:")
    for letter in self.errors:
      print(letter, end = " ")
    #  self.score = self.score + 1
    print("")

    state = State(26 - np.count_nonzero(self.letters), self.time_total, self.time_elapsed, len(self.errors), self.theme, self.gender)
    state.print_info()

    self.counter = self.counter + 1
    if self.counter == 10:
      done = True

    # reward implementations here
    total = 0
    for ele in range(0, len(self.letters)):
      total = total + self.letters[ele]
    if ((600*30)/(self.time_total*(26 - total +1) * self.time_elapsed))>0.8 or ((600*30)/(self.time_total*(26 - total +1) * self.time_elapsed))<0.3:
      reward = 10
    else:
      reward = -50
    print("reward: " + str(reward))

    if done:
      self.time_total = 0

    return state, changed, action, reward, done



  def end(self):
# additional reward implementation
    reward = 0
    if len(self.errors) > 5:
      reward = reward - 50
    else:
      reward = reward + 50
    reward = reward + np.count_nonzero(self.letters)*10
    print("additional reward: " + str(reward))
    return reward
