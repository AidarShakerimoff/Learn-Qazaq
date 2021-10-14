import numpy as np
import time
import random
from collections import defaultdict
from state import State
from format import Format

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
  if (l == 'а' or l == 'A'):
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
    return l

import numpy as np

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
  

def reversedLetters (word_entered, word_given, index):
  # if entered is less than given

  if (len(word_entered)<=len(word_given)):
    if (word_entered[index] != word_given[index]):
      # check first if there is any extra letter after this
      if (index+1 < len(word_entered)):
        if ((word_entered[index+1] == word_given[index]) and (word_entered[index] == word_given[index+1])):
          a = [word_entered[index], word_entered[index+1]]
          print("REVERSED")
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
          print("REVERSED")
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
          print("MISSEDLETTER")
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
          print("MISSEDLETTER")
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
      if (i < len(word_entered)):
        if (word_entered[index+1] == word_given[index]):
          a = [word_given[index]]
          print("EXTRALETTER")
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
          print("EXTRALETTER")
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
              print("MISSSPELLED")
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
              print("MISSSPELLED")
              word_entered[i] = word_given[i]
              listOfMistakes.append(word_given[i])
    i = i + 1;
  if (len(word_entered) < len(word_given)):
    for i in range(len(word_entered), len(word_given)):
      print("Extra")
      listOfMistakes.append(word_given[i])

  else:
    for i in range(len(word_given), len(word_entered)):
      print("Extra")
      listOfMistakes.append(word_entered[i])


  return listOfMistakes

class CoWriting:
  #environment class goes here
  def __init__(self, gender, adapt_to_gender = False):
    self.gender = gender
    self.adapt_to_gender = adapt_to_gender
    #!
    self.letters = np.zeros(31)         # list of letters: assigned to zeros for unexplored letters, ones for explored letters. Later override for kazakh alphabet
    #!
    self.kazakh_letters = ['a', 'ä', 'b', 'v', 'g', 'ğ', 'd', 'e', 'j', 'z', 'i', 'k', 'q', 'l', 'm', 'n', 'ñ', 'o', 'ö', 'p', 'r', 's', 't', 'u', 'ū', 'ü', 'f', 'h', 'ş', 'y', 'ı']
    self.score = 0                      # will indicate whether there is a problematic letter that is still not learned.
    self.time_elapsed = 0               # time spent by student to write a recent word
    self.time_total = 0                 # overall time for all words in one episode
    self.list_of_lists = []             # list of all given words
    #!
    self.list1 = ['апа', 'әже', 'бал', 'ваза', 'гүл', 'ғажап', 'дана', 'ерік', 'жауап', 'заман', 'ине', 'і', 'көмек', 'қасық', 'лас', 'мамыр', 'неке', 'ң', 'осал', 'өрт', 'патша', 'рақым', 'сәуле', 'таза', 'ушу', 'ұя', 'үй', 'фарш', 'хат', 'шаш', 'ш', 'ыдыс', 'ірімшік']
    self.list_of_lists.append(self.list1)
    #!
    self.list2 = ['аға', 'әке', 'бала','вагон', 'гу', 'ғарыш', 'дау', 'ереже', 'жігіт', 'заң', 'ит', 'i', 'кеңес', 'қылыш', 'лай', 'мақсат', 'намыс', 'ң', 'от', 'өкім', 'піл', 'ру', 'сергек', 'тас', 'уәде', 'ұл', 'үй', 'факт', 'хабар', 'һ', 'шарт', 'ш', 'ырыс', 'із']
    self.list_of_lists.append(self.list2)
    #!
    self.list3 = ['аргумент', 'барби', 'вальс', 'генерал', 'ғ', 'джем', 'евро', 'ж', 'зомби', 'интернет', 'i', 'конвертер', 'қ', 'лимон', 'мама', 'нота', 'ң', 'окей', 'ө', 'папа', 'робот', 'снайпер', 'танк', 'университет', 'ұ', 'ү', 'ф', 'фильм', 'хакер', 'ы', 'і', 'шоппинг']
    self.list_of_lists.append(self.list3)
    #!
    self.list4 = ['ауф', 'әйи', 'буу', 'вах', 'гыа', 'ғаф', 'дей', 'ефу', 'жае', 'зим', 'исе', 'кук', 'қаң', 'лаф', 'мах', 'нао', 'ңа', 'фао', 'өйи', 'паф', 'рут', 'саю', 'тац', 'уей', 'ұп', 'үф', 'фаш', 'хас', 'һа', 'шуй', 'ымм', 'іди']
    self.list_of_lists.append(self.list4)
    #!
    self.list5 = ['асқабақ', 'әлеуметтік', 'білезік', 'валенттілік', 'гуманитарлық', 'ғаламтор', 'денсаулық', 'егемендік', 'жүгері', 'заңдылық', 'и', 'игілік', 'кәсіптік', 'қанағаттандыру', 'лүпілдек', 'мүмкіндік', 'нәсихаттау', 'ң', 'одақтастыру', 'өзімшілдік', 'пікірлес', 'рәміздер', 'сәулетті', 'тітіркендіру', 'уылдырық', 'ұсақтау', 'үлпілдек', 'фракцияшылдық', 'хәзірет', 'шаруашылық', 'ынтымақ', 'ізгілік']
    self.list_of_lists.append(self.list5)
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
        #!
        self.theme = randint(2, 4) 
    else:
      print("predefined advice is off")
      self.theme = random.randint(0,len(self.list_of_lists)-1)
    if self.theme == 0:
      print("theme: GIRLS was selected")
    elif self.theme == 1:
      print("theme: BOYS was selected")
    else:
      #!
      print("theme: English words or nonsense words or difficult words was selected") 
  
# no change is done
    # select a random word in the given theme
    word_index = random.randint(0,len(self.list_of_lists[self.theme])-1)
    self.word = self.list_of_lists[self.theme][word_index]
    print("selected word: " + self.word)

#!
    # indicate explored letters
    for c in self.word:
      self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1     
    print("updated list of remaining letters to explore:")
    for idx in range(len(self.letters)):
      if self.letters[idx] == 0:
#!
          print(self.kazakh_letters[idx], end = " ")
    print("")


    # show the word to student, receive his/her response
    self.time_total = 0
    print(">>>>>interaction with student begins")
    user_word, self.time_elapsed = self.interact()
    print(">>>>>interaction with student stops")
    self.time_total = self.time_total + self.time_elapsed

    # record errors of  the student 
    #!
    helper = []
    if (len(wordCyrToLat(user_word)) == len(wordCyrToLat(self.word))):
      if (wordCyrToLat(user_word) != wordCyrToLat(self.word)):
        helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))
    else:
      helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))

    for i in range(len(helper)):
      if helper[i] not in self.errors:
        self.errors.append(helper[i])

    # for underlining and printing the letters
    #!
    
    for i in range(len(self.word)):
      checker = False
      for j in range(len(helper)):

        if (helper[j] == self.word[i]):
          checker = True
      if (checker == True):
        print(Format.underline + self.word[i] + Format.end, end = "")  
      else:
        print(self.word[i], end ="")

    print("problematic letters:")
    for letter in self.errors:
      print(letter, end = " ")
      self.score = self.score + 1
    print("")

    self.counter = self.counter + 1


    state = State(31 - np.count_nonzero(self.letters), self.time_total, self.time_elapsed, len(self.errors), self.theme, self.gender)
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
      #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        tmp = [idx for idx in self.list_of_lists[self.theme] if cyrToLat(idx[0].lower()) in self.errors]
        self.word = random.choice(tmp)
        print("next selected word: " + self.word + " resolves problematic letter " + cyrToLat(self.word[0]))
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.errors.remove(cyrToLat(self.word[0]))
        print("remaining problematic letters: ")
        print(self.errors)
        self.score = self.score - 1
        for c in self.word:
    #!
          self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1 
        print("updated list of remaining letters to explore:")
        for idx in range(len(self.letters)):
          if self.letters[idx] == 0:
    #!
            print(self.kazakh_letters[idx], end = " ")
        print("")
 
    if action == 1:
      #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      tmp = [idx for idx in self.list_of_lists[self.theme] if self.letters[self.kazakh_letters.index(cyrToLat(idx[0]))] == 0] 
      self.word = random.choice(tmp)
      print("next selected word: " + self.word)
    #!
      for c in self.word:
        self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
      print("updated list of remaining letters to explore:")
      for idx in range(len(self.letters)):
    #!
            print(self.kazakh_letters[idx], end = " ")
      print("")
    
    if action == 2:
      if not self.errors:
        action = 3
        changed = True
        print("action was changed to " + self.actions_codes[action])
      else:
        # no change is done
        print("theme changed from " + str(self.theme), end = " ")
        self.theme = random.randint(0, 2)
        print("to " + str(self.theme))
        tmp = [idx for idx in self.list_of_lists[self.theme] if cyrToLat(idx[0].lower()) in self.errors] #############
        self.word = random.choice(tmp)
        print("next selected word: " + self.word + " resolves problematic letter " + cyrToLat(self.word[0]))
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.errors.remove(cyrToLat(self.word[0]))
        self.score = self.score - 1
        for c in self.word:
    #!
          self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
        print("updated list of remaining letters to explore:")
        for idx in range(len(self.letters)):
          if self.letters[idx] == 0:
    #!
            print(self.kazakh_letters[idx], end = " ")
        print("")
    
    if action == 3:
      #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      print("theme changed from " + str(self.theme), end = " ")
      self.theme = random.randint(0, 2)
      print("to " + str(self.theme))
      tmp = [idx for idx in self.list_of_lists[self.theme] if self.letters[self.kazakh_letters.index(cyrToLat(idx[0]))] == 0] ##########
      self.word = random.choice(tmp)
      print("next selected word: " + self.word)
      #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      for c in self.word:
    #!
          self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
      print("updated list of remaining letters to explore:")
      for idx in range(len(self.letters)):
        if self.letters[idx] == 0:
    #!
            print(self.kazakh_letters[idx], end = " ")
      print("")
    
    # ask advice
    if action == 4:
      bool_var = 0
      while bool_var == 0:
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        word = input("Please, help me! Which word should we try?")
        for t in range(len(self.list_of_lists) - 1):
          if word in self.list_of_lists[t]:
            self.word = word
            self.theme = t
            print("theme identified: " + str(self.theme))
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            for c in self.word:
          #!
              self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
            print("updated list of remaining letters to explore:")
            for idx in range(len(self.letters)):
              if self.letters[idx] == 0:
          #!
                print(self.kazakh_letters[idx], end = " ")
            print("")
            bool_var = 1

    print(">>>>>interaction with student begins")
    user_word, self.time_elapsed = self.interact()
    print(">>>>>interaction with student stops")
    self.time_total = self.time_total + self.time_elapsed

    #!
    helper = []
    if (len(wordCyrToLat(user_word)) == len(wordCyrToLat(self.word))):
      if (wordCyrToLat(user_word) != wordCyrToLat(self.word)):
        helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))
    else:
      helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))

    for i in range(len(helper)):
      if helper[i] not in self.errors:
        self.errors.append(helper[i])

    # for underlining and printing the letters
    #!

    for i in range(len(self.word)):
      checker = False
      for j in range(len(helper)):

        if (helper[j] == self.word[i]):
          checker = True
      if (checker == True):
        print(Format.underline + self.word[i] + Format.end, end = "")  
      else:
        print(self.word[i], end ="")

    print("")
    print("problematic letters:")
    for letter in self.errors:
      print(letter, end = " ")
      self.score = self.score + 1
    print("")
#!
    state = State(31 - np.count_nonzero(self.letters), self.time_total, self.time_elapsed, len(self.errors), self.theme, self.gender) 
    state.print_info()

    self.counter = self.counter + 1
    if self.counter == 10:
      done = True

    # reward implementations here
    total = 0
    for ele in range(0, len(self.letters)):
      total = total + self.letters[ele]
      #!
    if ((600*30)/(self.time_total*(31 - total +1) * self.time_elapsed))>0.8 or ((600*30)/(self.time_total*(31 - total +1) * self.time_elapsed))<0.3:
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
    if self.score > 5:
      reward = reward - 50
    else:
      reward = reward + 50
    reward = reward + np.count_nonzero(self.letters)*10
    print("additional reward: " + str(reward))
    return reward
