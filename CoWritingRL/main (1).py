import numpy as np
import time
import random
from collections import defaultdict
import json
import math

import codecs

import os
import telebot

API = os.environ['API-KEY']

bot = telebot.TeleBot(API)


# Function 1. Reads the file, splits quotes and authors, returns a list of tuples that contain either (quote, author) or (quote)
def crt_tuples():
    lst_of_tuples = []
    with codecs.open('dataset.txt', encoding='utf-8-sig') as f:
        for line in f:
            lst = line.split('. ')
            lst = [x.replace("\r\n", "") for x in lst]
            lst_of_tuples.append(tuple(lst))
    return lst_of_tuples

def convert_kazakh_to_english(author_name):
  dictionary = {'Ь': '', 'Ъ': '', 'ъ': '', 'А': 'A', 'а': 'a', 'Ә': 'Ä', 'ә': 'ä', 'Б': 'B', 'б': 'b', 'В': 'V',
          'в': 'v', 'Г': 'G', 'г': 'g', 'Ғ': 'Ğ', 'ғ': 'ğ', 'Д': 'D', 'д': 'd', 'Е': 'E', 'е': 'e', 'Ё': 'E',
          'ё': 'e', 'Ж': 'J', 'ж': 'j', 'З': 'Z', 'з': 'z', 'И': 'I', 'и': 'i', 'Й': 'i',
          'й': 'i', 'K': 'K', 'к': 'k', 'Қ': 'Q', 'қ': 'q', 'Л': 'L', 'л': 'l', 'М': 'M', 'м': 'm', 'Н': 'N',
          'н': 'n', 'Ң': 'Ñ', 'ң': 'ñ', 'О': 'O', 'о': 'o', 'Ө': 'Ö', 'ө': 'ö', 'П': 'P', 'п': 'p', 'Р': 'R', 'р': 'r', 'С': 'S',
          'с': 's', 'Т': 'T', 'т': 't', 'У': 'U', 'у': 'u', 'Ұ': 'Ū', 'ұ': 'ū', 'Ү': 'Ü','ү': 'ü', 'Ф': 'F', 'ф': 'f', 'Х': 'H',
          'х': 'h', 'Һ': 'H', 'һ': 'h', 'Ц': 'S', 'ц': 's', 'Ч': 'Ş', 'ч': 'ş', 'Ш': 'Ş', 'ш': 'ş',
          'Щ': 'Ş', 'щ': 'ş', 'Ы': 'Y', 'ы': 'y', 'І': 'I', 'і': 'i', "ь": "'", 'Э': 'E', 'э': 'e', 'Ю': 'Iu',
          'ю': 'iu', 'Я': 'Ia', 'я': 'ia'}

  for kazakh, english in dictionary.items():
    author_name = author_name.replace(kazakh, english)
  return author_name




# supporting functions for kazakh language

def stringToList(string):
  list1=[]
  list1[:0]=string
  return list1

def listToString(s): 
  str1 = "" 
  return (str1.join(s))

def cyrToLat(letter):
  l = letter
# switch letter to a new one
  if (l == 'а' or l == 'А' or l == 'A' or l == 'a'):
    return 'a'
  elif (l == 'ә' or l == 'Ә'):
    return 'ä'
  elif (l == 'б' or l == 'Б'):
    return 'b'
  elif (l == 'в' or l == 'В'):
    return 'v'
  elif (l == 'г' or l == 'Г'):
    return 'g'
  elif (l == 'ғ' or l == 'Ғ'):
    return 'ğ'
  elif (l == 'д' or l == 'Д'):
    return 'd'
  elif (l == 'е' or l == 'Е'):
    return 'e'
  elif (l == 'ё' or l == 'Ё'):
    return 'e'
  elif (l == 'ж' or l == 'Ж'):
    return 'j'
  elif (l == 'з' or l == 'З'):
    return 'z'
  elif (l == 'и' or l == 'И'):
    return 'i'
  elif (l == 'й' or l == 'Й'):
    return 'i'
  elif (l == 'к' or l == 'К'):
    return 'k'
  elif (l == 'қ' or l == 'Қ'):
    return 'q'
  elif (l == 'л' or l == 'Л'):
    return 'l'
  elif (l == 'м' or l == 'М'):
    return 'm'
  elif (l == 'н' or l == 'Н'):
    return 'n'
  elif (l == 'ң' or l == 'Ң'):
    return 'ñ'
  elif (l == 'о' or l == 'О'):
    return 'o'
  elif (l == 'ө' or l == 'Ө'):
    return 'ö'
  elif (l == 'п' or l == 'П'):
    return 'p'
  elif (l == 'р' or l == 'Р'):
    return 'r'
  elif (l == 'с' or l == 'С'):
    return 's'
  elif (l == 'т' or l == 'Т'):
    return 't'
  elif (l == 'у' or l == 'У'):
    return 'u' 
  elif (l == 'ұ' or l == 'Ұ'):
    return 'ū'
  elif (l == 'ү' or l == 'Ү'):
    return 'ü'
  elif (l == 'ф' or l == 'Ф'):
    return 'f'
  elif (l == 'х' or l == 'Х'):
    return 'h'
  elif (l == 'һ' or l == 'Һ'):
    return 'h'
  elif (l == 'ц' or l == 'Ц'):
    return 's'
  elif (l == 'ч' or l == 'Ч'):
    return 'ş'
  elif (l == 'ш' or l == 'Ш'):
    return 'ş'
  elif (l == 'щ' or l == 'Щ'):
    return 'ş'
  elif (l == 'ъ' or l == 'Ъ'):
    return ''
  elif (l == 'ы' or l == 'Ы'):
    return 'y'
  elif (l == 'і' or l == 'І'):
    return 'ı'
  elif (l == 'ь' or l == 'Ь'):
    return ''
  elif (l == 'э' or l == 'Э'):
    return 'e'
  elif (l == 'ю' or l == 'Ю'):
    return 'ü'
  elif (l == 'я' or l == 'Я'):
    return 'ä'
  # if any other case is met, return simply same 'letter'
  else:
    return l ####


def wordCyrToLat(word):
  w = word
  new_w = stringToList(w)
  i = 0
  for letter in new_w:
    new_w[i] = cyrToLat(letter)
    i = i + 1
  return listToString(new_w)

def latToCyr(letter):
  l = letter
# switch letter to a new one
  if (l == 'a'):
    return 'а'
  elif (l == 'ä'):
    return 'ә'
  elif (l == 'b'):
    return 'б'
  elif (l == 'v'):
    return 'в'
  elif (l == 'g'):
    return 'г'
  elif (l == 'ğ'):
    return 'ғ'
  elif (l == 'd'):
    return 'д'
  elif (l == 'e'):
    return 'е'
  elif (l == 'j'):
    return 'ж'
  elif (l == 'z'):
    return 'з'
  elif (l == 'i'):
    return 'и'
  elif (l == 'i'):
    return 'и'
  elif (l == 'k'):
    return 'к'
  elif (l == 'q'):
    return 'қ'
  elif (l == 'l'):
    return 'л'
  elif (l == 'm'):
    return 'м'
  elif (l == 'n'):
    return 'н'
  elif (l == 'ñ'):
    return 'ң'
  elif (l == 'o'):
    return 'о'
  elif (l == 'ö'):
    return 'ө'
  elif (l == 'p'):
    return 'п'
  elif (l == 'r'):
    return 'р'
  elif (l == 's'):
    return 'с'
  elif (l == 't'):
    return 'т'
  elif (l == 'u'):
    return 'у' 
  elif (l == 'ū'):
    return 'ұ'
  elif (l == 'ü'):
    return 'ү'
  elif (l == 'f'):
    return 'ф'
  elif (l == 'h'):
    return 'х'
  elif (l == 'h'):
    return 'һ'
  elif (l == 'ş'):
    return 'ш'
  elif (l == 'y'):
    return 'ы'
  elif (l == 'ı'):
    return 'і'
  # if any other case is met, return simply same 'letter'
  else:
    return l

def upperKazakh(letter):
  l = letter
# switch letter to a new one
  if (l == 'a'):
    return 'A'
  elif (l == 'ä'):
    return 'Ä'
  elif (l == 'b'):
    return 'B'
  elif (l == 'v'):
    return 'V'
  elif (l == 'g'):
    return 'G'
  elif (l == 'ğ'):
    return 'Ğ'
  elif (l == 'd'):
    return 'D'
  elif (l == 'e'):
    return 'E'
  elif (l == 'j'):
    return 'J'
  elif (l == 'z'):
    return 'Z'
  elif (l == 'i'):
    return 'I'
  elif (l == 'i'):
    return 'I'
  elif (l == 'k'):
    return 'K'
  elif (l == 'q'):
    return 'Q'
  elif (l == 'l'):
    return 'L'
  elif (l == 'm'):
    return 'M'
  elif (l == 'n'):
    return 'N'
  elif (l == 'ñ'):
    return 'Ñ'
  elif (l == 'o'):
    return 'O'
  elif (l == 'ö'):
    return 'Ö'
  elif (l == 'p'):
    return 'P'
  elif (l == 'r'):
    return 'R'
  elif (l == 's'):
    return 'S'
  elif (l == 't'):
    return 'T'
  elif (l == 'u'):
    return 'U' 
  elif (l == 'ū'):
    return 'Ū'
  elif (l == 'ü'):
    return 'Ü'
  elif (l == 'f'):
    return 'F'
  elif (l == 'h'):
    return 'H'
  elif (l == 'h'):
    return 'H'
  elif (l == 'ş'):
    return 'Ş'
  elif (l == 'y'):
    return 'Y'
  elif (l == 'ı'):
    return 'I'
  # if any other case is met, return simply same 'letter'
  else:
    return l

def reversedLetters (word_entered, word_given, index):
  # if entered is less than given

  if (len(word_entered)<=len(word_given)):
    if (word_entered[index] != word_given[index]):
      # check first if there is any extra letter after this
      if (index+1 < len(word_entered)):
        if ((word_entered[index+1] == word_given[index]) and (word_entered[index] == word_given[index+1])):
          a = [word_entered[index], word_entered[index+1]]
          #print("REVERSED")
          return a
        else:
          return ''
      else:
        return ''

  # if entered is bigger than given
  else:
    if (word_entered[index] != word_given[index]):
      # check first if there is any extra letter after this
      if (index+1 < len(word_given)):
        if ((word_entered[index+1] == word_given[index]) and (word_entered[index] == word_given[index+1])):
          a = word_entered[index], word_entered[index+1]
          #print("REVERSED")
          return a
        else:
          return ''
      else:
        return ''

def missedLetter (word_entered, word_given, index):
  if (len(word_entered)<=len(word_given)):
    if (word_entered[index] != word_given[index]):
      # check first if there is any extra letter after this
      if (len(word_entered) == len(word_given)):
        i = index + 1
      else:
        i = index
      if (i < len(word_entered)):
        if (word_entered[index] == word_given[index+1]):
          a = word_given[index]
          #print("MISSEDLETTER")
          return a
        else:
          return ''
      else:
        return ''

  # if entered is bigger than given
  else:
    if (word_entered[index] != word_given[index]):
      # check first if there is any extra letter after this
      if (len(word_entered) == len(word_given)):
        i = index + 1
      else:
        i = index + 1
      if (i < len(word_given)):
        if (word_entered[index] == word_given[index+1]):
          a = [word_given[index]]
          #print("MISSEDLETTER")
          return a
        else:
          return ''
      else:
        return ''

def extraLetter (word_entered, word_given, index):
  if (len(word_entered)<=len(word_given)):
    if (word_entered[index] != word_given[index]):
      if (len(word_entered) == len(word_given)):
        i = index + 1
      else:
        i = index
      # check first if there is any extra letter after this
      if (i < len(word_entered)-1):
        if (word_entered[index+1] == word_given[index]):
          a = [word_given[index]]
          #print("EXTRALETTER")
          return a
        else:
          return ''
      else:
        return ''

  # if entered is bigger than given
  else:
    if (word_entered[index] != word_given[index]):
      if (len(word_entered) == len(word_given)):
        i = index + 1
      else:
        i = index
      # check first if there is any extra letter after this
      if (i < len(word_given)):
        if (word_entered[index+1] == word_given[index]):
          a = [word_given[index]]
          #print("EXTRALETTER")
          return a
        else:
          return ''
      else:
        return ''



def wrongLetters (word_entered, word_given):
  listOfMistakes = []
  word_entered = stringToList(word_entered)
  word_given = stringToList(word_given)

  i = 0;
  while(True):
    if (i == len(word_entered) or i == len(word_given)):
      break;
# if entered is less than given
    if (len(word_entered) <= len(word_given)):


      if (word_entered[i] != word_given[i]):
        if (reversedLetters(word_entered, word_given, i) != ''):
          # correct the word
          first = word_entered[i]
          word_entered[i] = word_entered[i+1]
          word_entered[i+1] = first
          listOfMistakes.append(word_entered[i])
          listOfMistakes.append(word_entered[i+1])
          i = i + 1
        else:
          if (missedLetter(word_entered, word_given, i) != ''):
            listOfMistakes.append(word_given[i])
            word_entered.insert(i, word_given[i])
            i = i + 1
          else:

            if (extraLetter(word_entered, word_given, i) != ''):
              listOfMistakes.append(word_entered[i])
              word_entered.pop(i)
              i = i - 1
            else:
              #print("MISSSPELLED")
              word_entered[i] = word_given[i]
              listOfMistakes.append(word_given[i])

  
# if entered is bigger than given
    else:


      if (word_entered[i] != word_given[i]):
        if (reversedLetters(word_entered, word_given, i) != ''):
          # correct the word
          first = word_entered[i]
          word_entered[i] = word_entered[i+1]
          word_entered[i+1] = first
          listOfMistakes.append(word_entered[i])
          listOfMistakes.append(word_entered[i+1])
          i = i + 1
        else:
          if (missedLetter(word_entered, word_given, i) != ''):
            listOfMistakes.append(word_given[i])
            word_entered.insert(i, word_given[i])
            i = i + 1
          else:

            if (extraLetter(word_entered, word_given, i) != ''):
              listOfMistakes.append(word_entered[i])
              word_entered.pop(i)
              i = i - 1;
            else:
              #print("MISSSPELLED")
              word_entered[i] = word_given[i]
              listOfMistakes.append(word_given[i])
    i = i + 1;
  if (len(word_entered) < len(word_given)):
    for i in range(len(word_entered), len(word_given)):
      #print("Extra")
      listOfMistakes.append(word_given[i])

  else:
    for i in range(len(word_given), len(word_entered)):
      #print("Extra")
      listOfMistakes.append(word_entered[i])


  return listOfMistakes


# suporting function to parse keys for loading Q values
def parseKey(key):
  state = key.split(' action ')[0]
  action = int(key[-1])
  return (state, action)

class OurEnvironment:
   #environment class goes here

  def loadQValues(self):
    with open('qValues' + str(self.id) + '.json') as fp:
      toLoad = json.load(fp)
      self.qValues = {parseKey(key) : toLoad[key] for key in toLoad}


  def saveQValues(self):
    toSave = {key[0] + ' action ' + str(key[1]) : self.qValues[key] for key in self.qValues}
    with open(f'qValues'+str(self.id) +'.json', 'w') as fp:
      json.dump(toSave, fp)

  def __init__(self, gender, id, adapt_to_gender = False):
    self.id = id
    if os.path.exists(str(id)+".txt"):
      self.logfile = open(str(self.id)+".txt", "a")
    else:
      self.logfile = open(str(self.id)+".txt", "w")
    self.gender = gender
    self.adapt_to_gender = adapt_to_gender
    self.gameIter = []
    self.actions = [0, 1, 2, 3]
    # self.actions = [0, 1, 2, 3, 4]    # actions: 0 - keep the theme and keep learning the problematic letter
                                      # 1 - keep the theme and explore words with new letters
                                      # 2 - change the theme and keep learning the problematic letter
                                      # 3 - change the theme and explore words with new letters
                                      # 4 - ask advice from adult

    if os.path.exists("qValues" + str(id)+".json"):
      self.loadQValues()
    else:
      self.qValues = defaultdict(float)
     # table of action-values (values of state x action pair)
    self.epsilon = 0.2    # hyperparameter used for epsilon-greedy policy. Indicates the probability of selecting a random action to explore
    self.discount = 0.99 # hypermarameter used for action-value update. Indicates how much future values are important to be considered
    self.alpha = 0.9        # hyperparameter used for   action-value update. Indicates how strongly will old values be overritten 
    self.done = False              # boolean variable indicating whether an episode (10 words) is ended
# iteration of episodes

    self.letters = np.zeros(31)         # list of letters: assigned to zeros for unexplored letters, ones for explored letters. Later override for kazakh alphabet
    self.kazakh_letters = ['a', 'ä', 'b', 'v', 'g', 'ğ', 'd', 'e', 'j', 'z', 'i', 'k', 'q', 'l', 'm', 'n', 'ñ', 'o', 'ö', 'p', 'r', 's', 't', 'u', 'ū', 'ü', 'f', 'h', 'ş', 'y', 'ı']
    self.challenges = 0                  # will indicate whether there were problematic letters
    self.time_elapsed = 0               # time spent by student to write a recent word
    self.time_total = 0                 # overall time for all words in one episode
    self.list_of_lists = []             # list of all given words
    self.list1 = crt_tuples()
    self.list_of_lists.append(self.list1)
    self.list2 = crt_tuples()
    self.list_of_lists.append(self.list2)
    self.list3 = crt_tuples()
    self.list_of_lists.append(self.list3)
    self.list4 = crt_tuples()
    self.list_of_lists.append(self.list4)
    self.list5 = crt_tuples()
    self.list_of_lists.append(self.list5)
    self.counter = 1                     # count words (if 10 -> new episode)
    self.actions_codes = ["keep the theme and keep learning the problematic letter", "keep the theme and explore words with new letters", "change the theme and keep learning the problematic letter", "change the theme and explore words with new letters", "ask advice from adult"]
    self.errors = []
    self.end_time = time.time()
    self.start_time = time.time()
    self.word = ""
    self.author = ""

 # this is a method for assessing a word to a student. Provide a word and wait him/her to rewrite it. Also count time for response
  # def interact(self, word):
  #   print(word)
  #   start_time = time.time()
  #   user_word = input("Please, write this word: ")
  #   end_time = time.time()
  #   time_lapsed = end_time - start_time
  #   return user_word, time_lapsed
 

  def start_episode(self, message):
    self.logfile.write("The interaction with user #" + str(self.id) + " begins: \n")
    if self.adapt_to_gender:        # if True -> apply predefined advice (apply specific theme for gender)
      self.logfile.write("Predefined advice is on. \n")
      #print("predefined advice is on")
      if self.gender == 0:
        self.theme = 0
      elif self.gender == 1:
        self.theme = 1
      else:
        self.theme = 2
    else:
      self.logfile.write("Predefined advice is off. \n")
      #print("predefined advice is off")
      self.theme = random.randint(0,len(self.list_of_lists)-1)
    if self.theme == 0:
      self.logfile.write("Theme: quotes was selected. \n")
      #print("theme: GIRLS was selected")
    elif self.theme == 1:
      self.logfile.write("Theme: quotes was selected. \n")
      #print("theme: BOYS was selected")
    else:
      self.logfile.write("Theme: Others was selected. \n")
      #print("theme: ANIMALS was selected")


    # select a random word in the given theme
    word_index = random.randint(0,len(self.list_of_lists[self.theme])-1)
    self.word = self.list_of_lists[self.theme][word_index][0]
    ###################################
    #self.word_copy = self.list_of_lists[self.theme][word_index][0]
    #self.word_help = []
    #for c in range(len(self.word_copy)):
    #  if c != ' ' and c != '?' and c!='–' and c != '.'and c != '-' and c != ',' and c != '!'and c != ':':
    #    self.word_help.append(self.word_copy[c])
    #self.word = listToString(self.word_help)
        ############################
    self.author = self.list_of_lists[self.theme][word_index][1]
    self.logfile.write("\n")
    self.logfile.write("The quote assigned by database: " + self.word + "\n")
    print("selected word: " + self.word)

    # indicate explored letters
    for c in self.word:
      if c != ' ' and c != '?' and c!='–' and c!='—' and c != '.' and c != ',':
        self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1    
    self.logfile.write("Updated list of remaining letters to explore: ")
    for idx in range(len(self.letters)):
      if self.letters[idx] == 0:
        self.logfile.write(self.kazakh_letters[idx] + " ")
        #print(chr(idx + ord('a')), end = " ")
    #print("")
    self.logfile.write("\n")
    


    # show the word to student, receive his/her response
    #time_total = 0
    #print(">>>>>interaction with student begins")
    if len(self.author) != 0:
      name = convert_kazakh_to_english(self.author)

      text1 = "Could you please rewrite " + name + "'s following quote in Kazakh-Latin alphabet: " + self.word
      text2 = "How the following quote of " + name + " would be written in Kazakh-Latin alphabet: "+ self.word
      text3 = "Please rewrite " + name + "'s quote in Kazakh-Latin alphabet: " + self.word

      random_text = random.choices([text1, text2, text3])
    sent = bot.send_message(message.chat.id, random_text)
    self.start_time = time.time()
    #self.logfile.close()
    bot.register_next_step_handler(sent, self.process)
  

  def process(self, message):
    user_word = message.text
    self.end_time = time.time()
    self.logfile.write("User's trial: " + user_word + "\n")
    time_elapsed = self.end_time - self.start_time
    self.logfile.write("Time of this interaction: " + str(time_elapsed) + "\n")
    self.time_total + time_elapsed

    # record errors of  the student 
    print_corr = []
    tmp = 0
    helper = []
    if (len(wordCyrToLat(user_word)) == len(wordCyrToLat(self.word))):
      if (wordCyrToLat(user_word) != wordCyrToLat(self.word)):
        helper = wrongLetters(user_word, wordCyrToLat(self.word))
        #helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))
        tmp = 1
    else:
      helper = wrongLetters(user_word, wordCyrToLat(self.word))
    #  helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))
      tmp = 1

    for i in range(len(helper)):
      if helper[i]!=' ' and helper[i] != '.' and helper[i]!='–' and helper[i]!= '—'  and helper[i] != '?'and helper[i] != '-'and helper[i] != ',' and helper[i] != '!'and helper[i] != ':'and helper[i] != ';':
        if helper[i] not in self.errors:
          self.errors.append(helper[i])
          self.challenges = self.challenges + 1

    for i in range(len(self.word)):
      if (cyrToLat(self.word[i]) not in helper):
        print_corr.append(cyrToLat(self.word[i]))
      else:
        print_corr.append(upperKazakh(cyrToLat(self.word[i])))

    self.logfile.write("Current problematic letters: ")
    for letter in self.errors:
      #print(letter, end = " ")
      self.logfile.write(letter + " ")
    #   self.score = self.score + 1
    #print("")
    self.logfile.write("\n")
    print_corr2 = ''
    if tmp==1:
      bot.send_message(message.chat.id, print_corr2.join(print_corr))
    else:
      bot.send_message(message.chat.id, "Correct!")
    #self.logfile.close()

    self.counter = self.counter + 1
    time_elapsed = time_elapsed//5
    if time_elapsed>10:
      time_elapsed = 10
    state = []
    state.append('num of letters: ' + str(31 - np.count_nonzero(self.letters)))
    state.append('time: ' + str(time_elapsed))
    state.append('num of errors: ' + str(len(self.errors)))
    state.append('theme: ' + str(self.theme))
    state.append('gender: ' + str(self.gender))
    state = ' '.join(state)
    
    action = self.act(state, self.epsilon)

    # done = False
    changed = False
    self.logfile.write("Action selected by agent: " + self.actions_codes[action] + "\n")
    #print("action selected: " + self.actions_codes[action])
    
    if action == 0:
      if not self.errors:
        self.qValues[(state, action)] = -math.inf
        action = 1
        changed = True
        self.logfile.write("No errors, action was changed to: " + self.actions_codes[action] + "\n")
      else:
        tmp = [idx for idx in self.list_of_lists[self.theme] if cyrToLat(idx[0][0].lower()) in self.errors]
        self.word = random.choice(tmp)[0]
        self.logfile.write("\n")
        self.logfile.write("Next selected word: " + self.word + " resolves problematic letter " + cyrToLat(self.word[0]) + "\n")
        self.errors.remove(cyrToLat(self.word[0].lower()))  # CORRECT THIS
        self.logfile.write("Remaining problematic letters: "+ str(self.errors) + "\n")
        print(self.word)
  #      self.score = self.score - 1
        for c in self.word:
          if c != ' ' and c != '.' and c!='–' and c!= '—'  and c != '?'and c != '-'and c != ',' and c != '!'and c != ':'and c != ';':
            self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1 
        self.logfile.write("Updated list of remaining letters to explore: ")
        for idx in range(len(self.letters)):
          if self.letters[idx] == 0:
            self.logfile.write(self.kazakh_letters[idx] + " ")
        self.logfile.write("\n")
 
    if action == 1:
      tmp = [idx for idx in self.list_of_lists[self.theme] if self.letters[self.kazakh_letters.index(cyrToLat(idx[0][0].lower()))] == 0] 
      self.word = random.choice(tmp)[0]
      self.logfile.write("\n")
      self.logfile.write("Next selected word: " + self.word + "\n")
      print(self.word)
      for c in self.word:
        if c != ' ' and c != '.' and c != '?'and c != '-' and c != ',' and c!='–'and c!='—' and c != '!'and c != ':'and c != ';':
          self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
      self.logfile.write("Updated list of remaining letters to explore: ")
      for idx in range(len(self.letters)):
        if self.letters[idx] == 0:
          self.logfile.write(self.kazakh_letters[idx] + " ")
      self.logfile.write("\n")
    
    if action == 2:
      if not self.errors:
        self.qValues[(state, action)] = -math.inf
        action = 3
        changed = True
        self.logfile.write("Action was changed to " + self.actions_codes[action] + "\n")
      else:
        self.logfile.write("Theme changed from " + str(self.theme))
        self.theme = random.randint(0, 2)
        self.logfile.write(" to " + str(self.theme) + "\n")
        tmp = [idx for idx in self.list_of_lists[self.theme] if cyrToLat(idx[0][0].lower()) in self.errors]
        self.word = random.choice(tmp)[0]
        self.logfile.write("\n")
        self.logfile.write("Next selected word: " + self.word + " resolves problematic letter " + cyrToLat(self.word[0]) + "\n")
        self.errors.remove(cyrToLat(self.word[0].lower()))
        print(self.word)
  #      self.score = self.score - 1
        for c in self.word:
          if c != ' ' and c != '.'  and c != '?'and c != '-'and c!='—'and c != ',' and c!='–' and c != '!'and c != ':'and c != ';':
            self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
        self.logfile.write("Updated list of remaining letters to explore:")
        for idx in range(len(self.letters)):
          if self.letters[idx] == 0:
            self.logfile.write(self.kazakh_letters[idx] + " ")
        self.logfile.write("\n")
    
    if action == 3:
      self.logfile.write("Theme changed from " + str(self.theme))
      self.theme = random.randint(0, 2)
      self.logfile.write(" to " + str(self.theme) + "\n")
      tmp = [idx for idx in self.list_of_lists[self.theme] if self.letters[self.kazakh_letters.index(cyrToLat(idx[0][0].lower()))] == 0]
      self.word = random.choice(tmp)[0]
      self.logfile.write("\n")
      self.logfile.write("Next selected word: " + self.word + "\n")
      print(self.word)
      for c in self.word:
        if c != ' ' and c!='–'and c!='—' and c != '.' and c != '?' and c != '-'and c != ',' and c != '!'and c != ':'and c != ';':
          self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
      self.logfile.write("Updated list of remaining letters to explore:")
      for idx in range(len(self.letters)):
        if self.letters[idx] == 0:
          self.logfile.write(self.kazakh_letters[idx] + " ")
      self.logfile.write("\n")
    
    # ask advice
    # if action == 4:
    #   bool_var = 0
    #   while bool_var == 0:
    #     word = input("Which word do you want to try now?")
    #     for t in range(len(self.list_of_lists) - 1):
    #       if word in self.list_of_lists[t]:
    #         self.word = word
    #         self.theme = t
    #         print("theme identified: " + str(self.theme))
    #         for c in self.word:
    #           self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
    #         print("updated list of remaining letters to explore:")
    #         for idx in range(len(self.letters)):
    #           if self.letters[idx] == 0:
    #             print(self.kazakh_letters[idx], end = " ")
    #         print("")
    #         bool_var = 1

    #print(">>>>>interaction with student begins")
    if len(self.author) != 0:
      name = convert_kazakh_to_english(self.author)

      text1 = "Could you please rewrite " + name + "'s following quote in Kazakh-Latin alphabet: " + self.word
      text2 = "How the following quote of " + name + " would be written in Kazakh-Latin alphabet: "+ self.word
      text3 = "Please rewrite " + name + "'s quote in Kazakh-Latin alphabet: " + self.word

      random_text = random.choices([text1, text2, text3])
    sent2 = bot.send_message(message.chat.id, random_text)
    self.start_time = time.time()
    self.logfile.close()
    bot.register_next_step_handler(sent2, self.process2, action, state)

  def process2(self, message, action, state):
    self.logfile = open(str(self.id)+".txt", "a")
    user_word = message.text
    self.logfile.write("User's trial: " + user_word + "\n")
    self.end_time = time.time()
    time_elapsed = self.end_time - self.start_time
    self.logfile.write("Time of this interaction: " + str(time_elapsed) + "\n")
    self.time_total = self.time_total + time_elapsed

    print_corr = []
    tmp = 0
    helper = []
    if (len(wordCyrToLat(user_word)) == len(wordCyrToLat(self.word))):
      if (wordCyrToLat(user_word) != wordCyrToLat(self.word)):
        helper = wrongLetters(user_word, wordCyrToLat(self.word))
        #helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))
        tmp = 1
    else:
      helper = wrongLetters(user_word, wordCyrToLat(self.word))
      #helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))
      tmp = 1

    for i in range(len(helper)):
      if helper[i]!=' ' and helper[i] != '.' and helper[i]!='–' and helper[i]!= '—'  and helper[i] != '?'and helper[i] != '-'and helper[i] != ',' and helper[i] != '!'and helper[i] != ':'and helper[i] != ';':
        if helper[i] not in self.errors:
          self.errors.append(helper[i])
          self.challenges = self.challenges + 1

    for i in range(len(self.word)):
      if (cyrToLat(self.word[i]) not in helper):
        print_corr.append(cyrToLat(self.word[i]))
      else:
        print_corr.append(upperKazakh(cyrToLat(self.word[i])))
    
    self.logfile.write("Current problematic letters: ")
    for letter in self.errors:
      self.logfile.write(letter + " ")
    #   self.score = self.score + 1
    self.logfile.write("\n")
    print_corr2 = ''

    if tmp==1:
      bot.send_message(message.chat.id, print_corr2.join(print_corr))
    else:
      bot.send_message(message.chat.id, "Correct!")

    next_state = []
    next_state.append('num of letters: ' + str(26 - np.count_nonzero(self.letters)))
    next_state.append('time: ' + str(time_elapsed))
    next_state.append('num of errors: ' + str(len(self.errors)))
    next_state.append('theme: ' + str(self.theme))
    next_state.append('gender: ' + str(self.gender))
    next_state = ' '.join(next_state)
    
    

    self.counter = self.counter + 1
    # if self.counter == 10:
    #   done = True

    # reward implementations here
  #  total = 0
  #  for ele in range(0, len(self.letters)):
   #   total = total + self.letters[ele]
    if time_elapsed <60 and time_elapsed> 5:
      reward = 10
    else:
      reward = -50
    self.logfile.write("reward: " + str(reward) +"\n")

    # if done:
    #   self.time_total = 0
    # if changed:
    #   self.qValues[(state, action)] = -math.inf
    #   action = changed_action
    self.gameIter.append((state, action, reward, next_state))
    state = next_state
    action = self.act(state, self.epsilon)
    self.logfile.write("Action selected by agent: " + self.actions_codes[action] + "\n")
    if action == 0:
      if not self.errors:
        self.qValues[(state, action)] = -math.inf
        action = 1
        changed = True
        self.logfile.write("No errors, action was changed to: " + self.actions_codes[action] + "\n")
      else:
        tmp = [idx for idx in self.list_of_lists[self.theme] if cyrToLat(idx[0][0].lower()) in self.errors]
        self.word = random.choice(tmp)[0]
        self.logfile.write("\n")
        self.logfile.write("Next selected word: " + self.word + " resolves problematic letter " + cyrToLat(self.word[0]) + "\n")
        self.errors.remove(cyrToLat(self.word[0].lower()))
        self.logfile.write("Remaining problematic letters: "+ str(self.errors) + "\n")
        print(self.word)
  #      self.score = self.score - 1
        for c in self.word:
          if c != ' ' and c!='–' and c!='—' and c != '?'and c != '.'and c != '-' and c != ',' and c != '!'and c != ':'and c != ';' :
            self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1 
        self.logfile.write("Updated list of remaining letters to explore: ")
        for idx in range(len(self.letters)):
          if self.letters[idx] == 0:
            self.logfile.write(self.kazakh_letters[idx] + " ")
        self.logfile.write("\n")
 
    if action == 1:
      tmp = [idx for idx in self.list_of_lists[self.theme] if self.letters[self.kazakh_letters.index(cyrToLat(idx[0][0].lower()))] == 0] 
      self.word = random.choice(tmp)[0]
      self.logfile.write("\n")
      self.logfile.write("Next selected word: " + self.word + "\n")
      print(self.word)
      for c in self.word:
        if c != ' 'and c!='—' and c!='–' and c != '?' and c != '.' and c != '-'and c != ',' and c != '!'and c != ':'and c != ';':
          self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
      self.logfile.write("Updated list of remaining letters to explore: ")
      for idx in range(len(self.letters)):
        if self.letters[idx] == 0:
          self.logfile.write(self.kazakh_letters[idx] + " ")
      self.logfile.write("\n")
    
    if action == 2:
      if not self.errors:
        self.qValues[(state, action)] = -math.inf
        action = 3
        changed = True
        self.logfile.write("Action was changed to " + self.actions_codes[action] + "\n")
      else:
        self.logfile.write("Theme changed from " + str(self.theme))
        self.theme = random.randint(0, 2)
        self.logfile.write(" to " + str(self.theme) + "\n")
        tmp = [idx for idx in self.list_of_lists[self.theme] if cyrToLat(idx[0][0].lower()) in self.errors]
        self.word = random.choice(tmp)[0]
        self.logfile.write("\n")
        self.logfile.write("Next selected word: " + self.word + " resolves problematic letter " + cyrToLat(self.word[0]) + "\n")
        self.errors.remove(cyrToLat(self.word[0].lower()))
        print(self.word)
  #      self.score = self.score - 1
        for c in self.word:
          if c != ' ' and c!='–'and c!='—' and c != '.' and c != '?' and c != '-'and c != ',' and c != '!'and c != ':'and c != ';':
            self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
        self.logfile.write("Updated list of remaining letters to explore:")
        for idx in range(len(self.letters)):
          if self.letters[idx] == 0:
            self.logfile.write(self.kazakh_letters[idx] + " ")
        self.logfile.write("\n")
    
    if action == 3:
      self.logfile.write("Theme changed from " + str(self.theme))
      self.theme = random.randint(0, 2)
      self.logfile.write(" to " + str(self.theme) + "\n")
      sublist = []
      for j in range(len(self.kazakh_letters)):
        if self.letters[j]==0:
          sublist.append(self.kazakh_letters[j])
      if len(sublist)!=0:
        tmp = [idx for idx in self.list_of_lists[self.theme] if random.choice(sublist) in idx[0]]
        if len(tmp) != 0:
          self.word = random.choice(tmp)[0]
        else:
          self.word = self.word = random.choice( self.list_of_lists[self.theme])[0]
      else:
        self.word = random.choice( self.list_of_lists[self.theme])[0]
      self.logfile.write("\n")
      self.logfile.write("Next selected word: " + self.word + "\n")
      print(self.word)
      for c in self.word:
        if c != ' ' and c!='–'and c!='—' and c != '.'  and c != '?'and c != '-'and c != ',' and c != '!'and c != ':'and c != ';':
          self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
      self.logfile.write("Updated list of remaining letters to explore:")
      for idx in range(len(self.letters)):
        if self.letters[idx] == 0:
          self.logfile.write(self.kazakh_letters[idx] + " ")
      self.logfile.write("\n")
    
    # ask advice
    # if action == 4:
    #   bool_var = 0
    #   while bool_var == 0:
    #     word = input("Which word do you want to try now?")
    #     for t in range(len(self.list_of_lists) - 1):
    #       if word in self.list_of_lists[t]:
    #         self.word = word
    #         self.theme = t
    #         print("theme identified: " + str(self.theme))
    #         for c in self.word:
    #           self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
    #         print("updated list of remaining letters to explore:")
    #         for idx in range(len(self.letters)):
    #           if self.letters[idx] == 0:
    #             print(self.kazakh_letters[idx], end = " ")
    #         print("")
    #         bool_var = 1

    #print(">>>>>interaction with student begins")
    

    self.logfile.close()
    if self.counter < 10:
      if len(self.author) != 0:
        name = convert_kazakh_to_english(self.author)

        text1 = "Could you please rewrite " + name + "'s following quote in Kazakh-Latin alphabet: " + self.word
        text2 = "How the following quote of " + name + " would be written in Kazakh-Latin alphabet: "+ self.word
        text3 = "Please rewrite " + name + "'s quote in Kazakh-Latin alphabet: " + self.word

        random_text = random.choices([text1, text2, text3])
      sent2 = bot.send_message(message.chat.id, random_text)
      self.start_time = time.time()
      bot.register_next_step_handler(sent2, self.process2, action, state)
    else:
      self.saveQValues()
      bot.send_message(message.chat.id, "Thank you for your time!")
    #return state, changed, action, reward, done



#   def end_episode(self):
# # additional reward implementation
#     reward = - len(self.errors) - (self.letters.size - np.count_nonzero(self.letters)) + self.challenges
#     print("additional reward: " + str(reward))
#     return reward

# actions = [0, 1, 2, 3, 4]    # actions: 0 - keep the theme and keep learning the problematic letter
#                                   # 1 - keep the theme and explore words with new letters
#                                   # 2 - change the theme and keep learning the problematic letter
#                                   # 3 - change the theme and explore words with new letters
#                                   # 4 - ask advice from adult

# qValues = defaultdict(float) # table of action-values (values of state x action pair)
# env = OurEnvironment(gender, adapt_to_gender)      # set the CoWriting environment. Specify the gender of a student and whether it needs to be considered as a pre-advice

  def act(self, state, epsilon):
      # this is an implementation of epsilon-greedy policy
      if random.random() < epsilon:
        #return random.randint(0, 4)
        return random.randint(0, 3)
  
      qValues = [self.qValues.get((state, action), 0) for action in self.actions]
  
      if np.all((qValues == 0)):
        #return random.randint(0, 4)
        return random.randint(0, 3)
      else:
        return np.argmax(qValues)



@bot.message_handler(commands = ['learn'])
def episode_start(message):
  env = OurEnvironment(0, message.chat.id)
  env.start_episode(message)
  
  

bot.polling()


# for i in range(500):
#   state = env.start_episode()
#   print("--------------------end of iteration---------------------------")
#  gameIter = []           # this is a list where transitions are stored in order to be updated again at the end of an episode
  # while True:
  #   action = act(state, epsilon)
  #   next_state, changed_action, changed, reward, done = env.perform(action)
  #   if changed:
  #     qValues[(state, action)] = -math.inf
  #     action = changed_action
      
  #   gameIter.append((state, action, reward, next_state))    # store the transition
  #   state = next_state
  #   print("--------------------end of iteration---------------------------")
  #   if done:
  #     print("-----------------------end of episode--------------------------")
  #     break
  # add_reward = self.env.end_episode()
  # for (state, action, reward, nextState) in gameIter[::-1]:    
  #   reward = reward + add_reward
  #   nextQValues = [qValues.get((nextState, nextAction), 0) for nextAction in actions]
  #   nextValue = max(nextQValues)
  #   qValues[(state, action)] = (1 - alpha) * qValues.get((state, action), 0) \
  #                                   + alpha * (reward + discount * nextValue)
  # input("Press Enter to continue...")   # to start new episode user have to activate it
