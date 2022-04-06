import numpy as np
import time
import random
from collections import defaultdict
import json
import math

# UNCOMMENT WHEN FIX CSV
import csv

import codecs
from telebot import types
import os
import telebot

import sys

API = os.environ['API-KEY']

bot = telebot.TeleBot(API)


# Function 1. Reads the file, splits quotes and authors, returns a list of tuples that contain either (quote, author) or (quote)
def crt_tuples(i):
    lst_of_tuples = []
    if(i==1):
      with codecs.open('datasetpoems_easy.txt', encoding='utf-8-sig') as f:
          for line in f:
              lst = line.split('.')
              lst = [x.replace("\r\n", " ") for x in lst]
              lst.append(count_letters_weights(lst[0]))
              lst_of_tuples.append(tuple(lst))
    elif(i==2):
      with codecs.open('datasetlyrics_easy.txt', encoding='utf-8-sig') as f:
          for line in f:
              lst = line.split('.')
              lst = [x.replace("\r\n", " ") for x in lst]
              lst.append(count_letters_weights(lst[0]))
              lst_of_tuples.append(tuple(lst))
    elif(i==3):
      with codecs.open('datasetfamousquotes_easy.txt', encoding='utf-8-sig') as f:
          for line in f:
              lst = line.split('. ')
              lst = [x.replace("\r\n", " ") for x in lst]
              lst.append(count_letters_weights(lst[0]))
              lst_of_tuples.append(tuple(lst))
    elif(i==4):
      with codecs.open('datasetpoems_hard.txt', encoding='utf-8-sig') as f:
          for line in f:
              lst = line.split('.')
              lst = [x.replace("\r\n", " ") for x in lst]
              lst.append(count_letters_weights(lst[0]))
              lst_of_tuples.append(tuple(lst))
    elif(i==5):
      with codecs.open('datasetlyrics_hard.txt', encoding='utf-8-sig') as f:
          for line in f:
              lst = line.split('. ')
              lst = [x.replace("\r\n", " ") for x in lst]
              lst.append(count_letters_weights(lst[0]))
              lst_of_tuples.append(tuple(lst))
    else:
      with codecs.open('datasetfamousquotes_hard.txt', encoding='utf-8-sig') as f:
          for line in f:
              lst = line.split('. ')
              lst = [x.replace("\r\n", " ") for x in lst]
              lst.append(count_letters_weights(lst[0]))
              lst_of_tuples.append(tuple(lst))
    return lst_of_tuples

def letter_score(some_letter):
  #convertation = {'a':'0', 'ä':'1', 'b':'2', 'v':'3', 'g':'4', 'ğ':'5', 'd':'6', 'e':'7', 'j':'8', 
  #                'z':'9', 'i':'10', 'k':'11', 'q':'12', 'l':'13', 'm':'14', 'n':'15', 'ñ':'16', 'o':'17', 
  #                'ö':'18', 'p':'19', 'r':'20', 's':'21', 't':'22', 'u':'23', 'ū':'24', 
  #                'ü':'25', 'f':'26', 'h':'27', 'ş':'28', 'y':'29', 'ı':'30'}
  convertation = {'a':'1', 'ä':'3', 'b':'1', 'v':'1', 'g':'1', 'ğ':'3', 'd':'1', 'e':'1', 'j':'1',
                'z':'1', 'i':'1', 'k':'1', 'q':'3', 'l':'1', 'm':'1', 'n':'1', 'ñ':'3', 'o':'1', 
                'ö':'3', 'p':'3', 'r':'1', 's':'1', 't':'1', 'u':'1', 'ü':'3', 
                'ū':'3', 'f':'1', 'h':'1', 'ş':'3', 'y':'3', 'ı':'3'}
  for letter, index in convertation.items():
    some_letter = some_letter.replace(letter, index)
  return int(some_letter)


def convert_kazakh_to_english(author_name):
  dictionary = {'Ь': '', 'Ъ': '', 'ъ': '', 'А': 'A', 'а': 'a', 'Ә': 'Ä', 'ә': 'ä', 'Б': 'B', 'б': 'b', 'В': 'V',
          'в': 'v', 'Г': 'G', 'г': 'g', 'Ғ': 'Ğ', 'ғ': 'ğ', 'Д': 'D', 'д': 'd', 'Е': 'E', 'е': 'e', 'Ё': 'E',
          'ё': 'e', 'Ж': 'J', 'ж': 'j', 'З': 'Z', 'з': 'z', 'И': 'I', 'и': 'i', 'Й': 'i',
          'й': 'i', 'K': 'K', 'к': 'k', 'Қ': 'Q', 'қ': 'q', 'Л': 'L', 'л': 'l', 'М': 'M', 'м': 'm', 'Н': 'N',
          'н': 'n', 'Ң': 'Ñ', 'ң': 'ñ', 'О': 'O', 'о': 'o', 'Ө': 'Ö', 'ө': 'ö', 'П': 'P', 'п': 'p', 'Р': 'R', 'р': 'r', 'С': 'S',
          'с': 's', 'Т': 'T', 'т': 't', 'У': 'U', 'у': 'u', 'Ұ': 'Ū', 'ұ': 'ū', 'Ү': 'Ü','ү': 'ü', 'Ф': 'F', 'ф': 'f', 'Х': 'H',
          'х': 'h', 'Һ': 'H', 'һ': 'h', 'Ц': 'C', 'ц': 'c', 'Ч': 'Ş', 'ч': 'ş', 'Ш': 'Ş', 'ш': 'ş',
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
    return 'c'
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

def lowerKazakh(letter):
  l = letter
# switch letter to a new one
  if (l == 'A'):
    return 'a'
  elif (l == 'Ä'):
    return 'ä'
  elif (l == 'B'):
    return 'b'
  elif (l == 'V'):
    return 'v'
  elif (l == 'G'):
    return 'g'
  elif (l == 'Ğ'):
    return 'ğ'
  elif (l == 'D'):
    return 'd'
  elif (l == 'E'):
    return 'e'
  elif (l == 'J'):
    return 'j'
  elif (l == 'Z'):
    return 'z'
  elif (l == 'I'):
    return 'i'
  elif (l == 'K'):
    return 'k'
  elif (l == 'Q'):
    return 'q'
  elif (l == 'L'):
    return 'l'
  elif (l == 'M'):
    return 'm'
  elif (l == 'N'):
    return 'n'
  elif (l == 'Ñ'):
    return 'ñ'
  elif (l == 'O'):
    return 'o'
  elif (l == 'Ö'):
    return 'ö'
  elif (l == 'P'):
    return 'p'
  elif (l == 'R'):
    return 'r'
  elif (l == 'S'):
    return 's'
  elif (l == 'T'):
    return 't'
  elif (l == 'U'):
    return 'u' 
  elif (l == 'Ū'):
    return 'ū'
  elif (l == 'Ü'):
    return 'ü'
  elif (l == 'F'):
    return 'f'
  elif (l == 'H'):
    return 'h'
  elif (l == 'Ş'):
    return 'ş'
  elif (l == 'Y'):
    return 'y'
  elif (l == 'I'):
    return 'ı'
  # if any other case is met, return simply same 'letter'
  else:
    return l


def please_try_typing (n):
  #n = random.randint(0,4)
  if (n == 0):
    return "Please use the Kazakh-Latin alphabet to type the following:"
  elif (n == 1):
    return "Using the Kazakh-Latin alphabet, type the following:"
  elif (n == 2):
    return "Please try typing the following word using the Kazakh-Latin alphabet:"
  elif (n == 3):
    return "What is the Kazakh-Latin version of the following word?"
  elif (n == 4):
    return "How would you write the following word in the Kazakh-Latin alphabet?"

def no_mistakes ():
  n = random.randint(0,8)
  if (n == 0):
    return "Wow! You really are a genius! 🤩"
  elif (n == 1):
    return "Excellent! 🤩"
  elif (n == 2):
    return "Super! 🤩"
  elif (n == 3):
    return "You’re doing great! 🤩"
  elif (n == 4):
    return "Perfect! 🤩"
  elif (n == 5):
    return "Way to go! 🤩"
  elif (n == 6):
    return "Look at you, converting letters like a pro! 🤩"
  elif (n == 7):
    return "You sure have a way with words! 🤩"
  elif (n == 8):
    return "You’re a word converting machine! 🤩"


def one_mistake ():
  n = random.randint(0,5)
  if (n == 0):
    return "Almost there! You should try again. 🤓"
  elif (n == 1):
    return "Well, that was really close! Keep going! 🤓"
  elif (n == 2):
    return "Give it another shot! 🤓"
  elif (n == 3):
    return "99% accuracy, let’s get that lost one 🤓"
  elif (n == 4):
    return "You got the point! We are very close to perfection 🤓"
  elif (n == 5):
    return "So close! Go on! 🤓"


def more_than_one_mistake ():
  n = random.randint(0,3)
  if (n == 0):
    return "I’m sure you can do better than this! 😛"
  elif (n == 1):
    return "That wasn’t bad! Maybe you should try harder… 😛"
  elif (n == 2):
    return "I do not like to tell people that they are wrong, but I can’t be silent this time! 😛"
  elif (n == 3):
    return "One day I will tell everybody that I taught you, but today we have many things to work on together 😛"

  

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
              if (word_given[i] == ' '):
                listOfMistakes.append(word_entered[i])
              else:
                listOfMistakes.append(word_given[i])
              word_entered[i] = word_given[i]

  
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
              if (word_given[i] == ' '):
                listOfMistakes.append(word_entered[i])
              else:
                listOfMistakes.append(word_given[i])
              word_entered[i] = word_given[i]
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

def wrongLetters_phrase_word_split(phrase_user, phrase_actual):
  list_phrase_user = phrase_user.split()
  list_phrase_actual = phrase_actual.split()
  for i in range (0,len(list_phrase_actual)):
    list_phrase_user.append('')
  for i in range (0,len(list_phrase_user)):
    list_phrase_actual.append('')
  listOfMistakes = []
  for i in range(0,min(len(list_phrase_user), len(list_phrase_actual))):
    helper = wrongLetters(list_phrase_user[i], list_phrase_actual[i])
    for j in range(0, len(helper)):
      listOfMistakes.append(helper[j])
  
  return listOfMistakes


def wrongLetters_phrase(phrase_user, phrase_actual):
  list_phrase_user = phrase_user.split()
  list_phrase_actual = phrase_actual.split()
  #for i in range (0,max(len(list_phrase_user), len(list_phrase_actual))+1):
  for i in range (0,len(list_phrase_actual)):
    list_phrase_user.append('')
  for i in range (0,len(list_phrase_user)):
    list_phrase_actual.append('')

  list_of_listOfMistakes = []
  for i in range(0,min(len(list_phrase_user), len(list_phrase_actual))+1):
    listOfMistakes = []

    helper1 = wrongLetters(''.join(list_phrase_user[:i]), ''.join(list_phrase_actual[:i]))
    helper2 = wrongLetters_phrase_word_split(' '.join(list_phrase_user[i:]), ' '.join(list_phrase_actual[i:]))
    
    for j in range(0, len(helper1)):
      listOfMistakes.append(helper1[j])
    for j in range(0, len(helper2)):
      listOfMistakes.append(helper2[j])


    
    while ' ' in listOfMistakes:
      listOfMistakes.remove(' ')

    list_of_listOfMistakes.append(listOfMistakes)

    #print("HERE IS A LIST: ", helper1, helper2, listOfMistakes)
  
  return min(list_of_listOfMistakes, key=len)
    




  
def count_letters_weights(phrase):
  #      cyr_letters =    а, ә, б, в, г, ғ, д, е, ж, з, и, к, қ, л, м, н, ң, о, ө, п, р, с, т, у, ү, ұ, ф, х, ш, ы, і
  count_kazakh_letters = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  #latin_phrase = wordCyrToLat (phrase)
  latin_phrase = phrase
  total_num = 0
  for letter in latin_phrase:
    if (letter == 'а' or letter == 'А'):
      count_kazakh_letters[0] = count_kazakh_letters[0] + 1
    elif (letter == 'ә' or letter == 'Ә'):
      count_kazakh_letters[1] = count_kazakh_letters[1] + 1
    elif (letter == 'б' or letter == 'Б'):
      count_kazakh_letters[2] = count_kazakh_letters[2] + 1
    elif (letter == 'в' or letter == 'В'):
      count_kazakh_letters[3] = count_kazakh_letters[3] + 1
    elif (letter == 'г' or letter == 'Г'):
      count_kazakh_letters[4] = count_kazakh_letters[4] + 1
    elif (letter == 'ғ' or letter == 'Ғ'):
      count_kazakh_letters[5] = count_kazakh_letters[5] + 1
    elif (letter == 'д' or letter == 'Д'):
      count_kazakh_letters[6] = count_kazakh_letters[6] + 1
    elif (letter == 'е' or letter == 'Е'  or letter == 'ё' or letter == 'Ё' or letter == 'э' or letter == 'Э'):
      count_kazakh_letters[7] = count_kazakh_letters[7] + 1
    elif (letter == 'ж' or letter == 'Ж'):
      count_kazakh_letters[8] = count_kazakh_letters[8] + 1
    elif (letter == 'з' or letter == 'З'):
      count_kazakh_letters[9] = count_kazakh_letters[9] + 1
    elif (letter == 'и' or letter == 'И'):
      count_kazakh_letters[10] = count_kazakh_letters[10] + 1
    elif (letter == 'к' or letter == 'К'):
      count_kazakh_letters[11] = count_kazakh_letters[11] + 1
    elif (letter == 'қ' or letter == 'Қ'):
      count_kazakh_letters[12] = count_kazakh_letters[12] + 1
    elif (letter == 'л' or letter == 'Л'):
      count_kazakh_letters[13] = count_kazakh_letters[13] + 1
    elif (letter == 'м' or letter == 'М'):
      count_kazakh_letters[14] = count_kazakh_letters[14] + 1
    elif (letter == 'н' or letter == 'Н'):
      count_kazakh_letters[15] = count_kazakh_letters[15] + 1
    elif (letter == 'ң' or letter == 'Ң'):
      count_kazakh_letters[16] = count_kazakh_letters[16] + 1
    elif (letter == 'о' or letter == 'О'):
      count_kazakh_letters[17] = count_kazakh_letters[17] + 1
    elif (letter == 'ө' or letter == 'Ө'):
      count_kazakh_letters[18] = count_kazakh_letters[18] + 1
    elif (letter == 'п' or letter == 'П'):
      count_kazakh_letters[19] = count_kazakh_letters[19] + 1
    elif (letter == 'р' or letter == 'Р'):
      count_kazakh_letters[20] = count_kazakh_letters[20] + 1
    elif (letter == 'с' or letter == 'С' or letter == 'ц' or letter == 'Ц'):
      count_kazakh_letters[21] = count_kazakh_letters[21] + 1
    elif (letter == 'т' or letter == 'Т'):
      count_kazakh_letters[22] = count_kazakh_letters[22] + 1
    elif (letter == 'у' or letter == 'У'):
      count_kazakh_letters[23] = count_kazakh_letters[23] + 1
    elif (letter == 'ү' or letter == 'Ү'):
      count_kazakh_letters[24] = count_kazakh_letters[24] + 1
    elif (letter == 'ұ' or letter == 'Ұ'):
      count_kazakh_letters[25] = count_kazakh_letters[25] + 1
    elif (letter == 'ф' or letter == 'Ф'):
      count_kazakh_letters[26] = count_kazakh_letters[26] + 1
    elif (letter == 'х' or letter == 'Х' or letter == 'һ' or letter == 'Һ'):
      count_kazakh_letters[27] = count_kazakh_letters[27] + 1
    elif (letter == 'ш' or letter == 'Ш' or letter == 'ч' or letter == 'Ч' or letter == 'щ' or letter == 'Щ'):
      count_kazakh_letters[28] = count_kazakh_letters[28] + 1
    elif (letter == 'ы' or letter == 'Ы'):
      count_kazakh_letters[29] = count_kazakh_letters[29] + 1
    elif (letter == 'і' or letter == 'І'):
      count_kazakh_letters[30] = count_kazakh_letters[30] + 1
    else:
      total_num = total_num - 1
    total_num = total_num + 1
  for i in range(31):
    count_kazakh_letters[i] = count_kazakh_letters[i]/total_num
    
  return count_kazakh_letters

def convert_letter_to_index(some_letter):
  #convertation = {'a':'0', 'ä':'1', 'b':'2', 'v':'3', 'g':'4', 'ğ':'5', 'd':'6', 'e':'7', 'j':'8', 
  #                'z':'9', 'i':'10', 'k':'11', 'q':'12', 'l':'13', 'm':'14', 'n':'15', 'ñ':'16', 'o':'17', 
  #                'ö':'18', 'p':'19', 'r':'20', 's':'21', 't':'22', 'u':'23', 'ū':'24', 
  #                'ü':'25', 'f':'26', 'h':'27', 'ş':'28', 'y':'29', 'ı':'30'}
  convertation = {'а':'0', 'ә':'1', 'б':'2', 'в':'3', 'г':'4', 'ғ':'5', 'д':'6', 'е':'7', 'ж':'8', 
                  'з':'9', 'и':'10', 'к':'11', 'қ':'12', 'л':'13', 'м':'14', 'н':'15', 'ң':'16', 'о':'17', 
                  'ө':'18', 'п':'19', 'р':'20', 'с':'21', 'т':'22', 'у':'23', 'ү':'24', 
                  'ұ':'25', 'ф':'26', 'х':'27', 'ш':'28', 'ы':'29', 'і':'30'}
  for letter, index in convertation.items():
    some_letter = some_letter.replace(letter, index)
  return int(some_letter)

# suporting function to parse keys for loading Q values
def parseKey(key):
  state = key.split(' action ')[0]
  action = int(key[-1])
  return (state, action)

class OurEnvironment:
   #environment class goes here

  def loadQValues_lettersRL(self):
    #with open('qValues' + str(self.id) + '.json') as fp:
    with open('qValues_lettersRL_Quotes.json') as fp:
      toLoad = json.load(fp)
      self.qValues_lettersRL = {parseKey(key) : toLoad[key] for key in toLoad}


  def saveQValues_lettersRL(self):
    toSave = {key[0] + ' action ' + str(key[1]) : self.qValues_lettersRL[key] for key in self.qValues_lettersRL}
    with open(f'qValues_lettersRL_Quotes.json', 'w') as fp:
    #with open(f'qValues'+str(self.id) +'.json', 'w') as fp:
      json.dump(toSave, fp)
      
  def loadQValues_levelRL(self):
    #with open('qValues' + str(self.id) + '.json') as fp:
    with open('qValues_levelRL_Quotes.json') as fp:
      toLoad = json.load(fp)
      self.qValues_levelRL = {parseKey(key) : toLoad[key] for key in toLoad}


  def saveQValues_levelRL(self):
    toSave = {key[0] + ' action ' + str(key[1]) : self.qValues_levelRL[key] for key in self.qValues_levelRL}
    with open(f'qValues_levelRL_Quotes.json', 'w') as fp:
    #with open(f'qValues'+str(self.id) +'.json', 'w') as fp:
      json.dump(toSave, fp)

  def __init__(self, gender, id, adapt_to_gender = False):

    self.id = id

    if os.path.exists(str(id)+".txt"):
      self.logfile = open(str(self.id)+".txt", "a")
    else:
      self.logfile = open(str(self.id)+".txt", "w")
    self.likes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.oldPhrases = []
    if os.path.exists(str(id)+"UsedPhrases.txt"):
      with codecs.open(str(id)+"UsedPhrases.txt", encoding='utf-8-sig') as f:
        for line in f:
          line.replace("\n", "")
          self.oldPhrases.append(line)

    self.err_hst = []
    self.gender = gender
    self.adapt_to_gender = adapt_to_gender
    self.gameIter_lettersRL = []
    self.gameIter_levelRL = []
    self.actions_lettersRL = [0, 1, 2, 3]
    self.actions_levelRL = [0, 1, 2]
    # self.actions = [0, 1, 2, 3, 4]    # actions: 0 - keep the theme and keep learning the problematic letter
                                      # 1 - keep the theme and explore words with new letters
                                      # 2 - change the theme and keep learning the problematic letter
                                      # 3 - change the theme and explore words with new letters
                                      # 4 - ask advice from adult

    if os.path.exists("qValues_lettersRL_Quotes.json"):
      self.loadQValues_lettersRL()
    else:
      self.qValues_lettersRL = defaultdict(float)
    if os.path.exists("qValues_levelRL_Quotes.json"):
      self.loadQValues_levelRL()
    else:  
      self.qValues_levelRL = defaultdict(float)
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
    self.list1 = crt_tuples(1)
    self.list_of_lists.append(self.list1)
    self.list2 = crt_tuples(2)
    self.list_of_lists.append(self.list2)
    self.list3 = crt_tuples(3)
    self.list_of_lists.append(self.list3)
    self.list4 = crt_tuples(4)
    self.list_of_lists.append(self.list4)
    self.list5 = crt_tuples(5)
    self.list_of_lists.append(self.list5)
    self.list6 = crt_tuples(6)
    self.list_of_lists.append(self.list6)
    self.counter = 1                     # count words (if 10 -> new episode)
    self.actions_codes = ["work with problematic easy letters", "explore words with new easy letters", "work with problematic hard letters", "explore words with new hard letters", "ask advice from adult"]
    self.actions_codes2 = ["decrease difficulty level", "keep difficulty level", "increase difficulty level"]
    self.errors_easy = []
    self.errors_hard = []
    self.end_time = time.time()
    self.start_time = time.time()
    self.word = ""
    self.author = ""


    # TO FIX CSV
    csv_columns = ['id', 'total_time', 'interaction_date_and_time', 'num_of_iterations', 'explored_letters', 'problem_letters', 'avg_time_per_iteration', '(time 1-N)']
    if os.path.exists("users_data_quotesRL.csv"):
      self.csv_file = open("users_data_quotesRL.csv", "a")
      self.writer = csv.DictWriter(self.csv_file, fieldnames=csv_columns)
    else:
      self.csv_file = open("users_data_quotesRL.csv", "w")
      self.writer = csv.DictWriter(self.csv_file, fieldnames=csv_columns) #csv.writer(self.csv_file)
      self.writer.writeheader()
      
    self.state_lettersRL = []
    self.action_lettersRL = 0
    
    self.state_levelRL = []
    self.action_levelRL = 0
    
    self.info = [self.id, 0, time.ctime(time.time()), 0, 0, 0, 0, []]

 # this is a method for assessing a word to a student. Provide a word and wait him/her to rewrite it. Also count time for response
  # def interact(self, word):
  #   print(word)
  #   start_time = time.time()
  #   user_word = input("Please, write this word: ")
  #   end_time = time.time()
  #   time_lapsed = end_time - start_time
  #   return user_word, time_lapsed
 

  def start_episode(self):
    self.logfile.write("A new interaction (phrases) with user #" + str(self.id) + " begins: \n")
    # if self.adapt_to_gender:        # if True -> apply predefined advice (apply specific theme for gender)
    #   self.logfile.write("Predefined advice is on. \n")
    #   #print("predefined advice is on")
    #   if self.gender == 0:
    #     self.theme = 0
    #   elif self.gender == 1:
    #     self.theme = 1
    #   else:
    #     self.theme = 2
    # else:
    #   self.logfile.write("Predefined advice is off. \n")
    #   #print("predefined advice is off")
    #   self.theme = random.randint(0,len(self.list_of_lists)-1)
    if self.theme == 0:
      self.logfile.write("Theme: poems was selected. \n")
      #print("theme: GIRLS was selected")
    elif self.theme == 1:
      self.logfile.write("Theme: lyrics was selected. \n")
      #print("theme: BOYS was selected")
    else:
      self.logfile.write("Theme: quotes was selected. \n")
      #print("theme: ANIMALS was selected")


    # select a random word in the given theme
    old = True
    oldsCounter = 0
    while old:
      word_index = random.randint(0,len(self.list_of_lists[self.theme])-1)

      self.word = self.list_of_lists[self.theme][word_index][0]
      if self.word not in self.oldPhrases:
        old = False
        self.oldPhrases.append(self.word)
      if oldsCounter > 2: # adjust this value 
        old = False
      oldsCounter = oldsCounter + 1

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
    self.letters_copy = self.letters
    # indicate explored letters
    for c in self.word:
      if c != ' ' and c != '.' and c!='–' and c!= '—'  and c != '?'and c != '-'and c != ',' and c != '!'and c != ':'and c != ';' and c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь' and c != '…':
        self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1    
    self.logfile.write("Updated list of remaining letters to explore: ")
    for idx in range(len(self.letters)):
      if self.letters[idx] == 0:
        self.logfile.write(self.kazakh_letters[idx] + " ")
        #print(chr(idx + ord('a')), end = " ")
    #print("")
    self.logfile.write("\n")
    self.info[4] = np.count_nonzero(self.letters)


    # show the word to student, receive his/her response
    #time_total = 0
    #print(">>>>>interaction with student begins")
    if len(self.author) > 10:
      name = convert_kazakh_to_english(self.author)

      text1 = "Could you please rewrite " + name + "'s following quote using Kazakh-Latin alphabet: \n⌨️ " + self.word
      text2 = "How the following quote of " + name + " would be written using Kazakh-Latin alphabet: \n⌨️ "+ self.word
      text3 = "Please rewrite " + name + "'s quote using Kazakh-Latin alphabet: \n⌨️ " + self.word
    else:
      
      text1 = "Could you please write the following using Kazakh-Latin alphabet: \n⌨️ "+ self.word
      text2 = "How this phrase would look like using Kazakh-Latin alphabet: \n⌨️ "+ self.word
      text3 = "Please rewrite the following using Kazakh-Latin alphabet: \n⌨️ "+ self.word

    self.letters_copy = self.letters
    self.challenges_copy = self.challenges
    self.errors_easy_copy = self.errors_easy
    self.errors_hard_copy = self.errors_hard

    random_text = random.choices([text1, text2, text3])
    sent = bot.send_message(self.id, random_text)
    self.start_time = time.time()
    #self.logfile.close()
    self.info[3] = self.info[3] + 1
    bot.register_next_step_handler(sent, self.process)

  def getFeedback(self, id):

    markup = types.InlineKeyboardMarkup()
    buttonA = types.InlineKeyboardButton('Like', callback_data=str(self.id)+'l')
    buttonB = types.InlineKeyboardButton('Dislike', callback_data=str(self.id)+'d')
    

    markup.row(buttonA, buttonB)

    bot.send_message(self.id, '🙃 ---End of the section--- 🙂\n'+'Did you like this interaction?', reply_markup=markup)

  def greet(self, id):

    markup = types.InlineKeyboardMarkup()
    buttonA = types.InlineKeyboardButton('Kazakh poems', callback_data=str(self.id)+'a')
    buttonB = types.InlineKeyboardButton('Kazakh music lyrics', callback_data=str(self.id)+'b')
    buttonC = types.InlineKeyboardButton('Kazakh famous quotes', callback_data=str(self.id)+'c')

    markup.row(buttonA, buttonB)
    markup.row(buttonC)

    bot.send_message(self.id, 'We have three topics for you, please choose the one you are interested in:', reply_markup=markup)

      #bot.callback_query_handler(func=lambda call: True)
  #@bot.message_handler(commands=['buttons'])

  def getLike(self, id, counter):

    markup = types.InlineKeyboardMarkup()
    buttonA = types.InlineKeyboardButton('Like', callback_data=str(self.id)+'a' + str(counter%10))
    buttonB = types.InlineKeyboardButton('Dislike', callback_data=str(self.id)+'b'+ str(counter%10))
    

    markup.row(buttonA, buttonB)

    bot.send_message(self.id, 'Did you like this phrase?', reply_markup=markup) 

  def process(self, message):
    user_word_written = message.text
    #user_word_written0 = message.text
    #user_word_written = ""
    #for ch in user_word_written0:
    #  user_word_written = user_word_written + lowerKazakh(ch)
    self.end_time = time.time()
    self.logfile.write("User's trial: " + user_word_written + "\n")
    time_elapsed = self.end_time - self.start_time
    #self.logfile.write("Time of this interaction: " + str(time_elapsed) + "\n")
    self.time_total = self.time_total + time_elapsed
    self.info[1] = round(self.time_total, 2)
    self.info[6] = round(self.time_total, 2)
    self.info[7].append(round(time_elapsed, 2))


    user_word_list = []
    for i in range(len(user_word_written)):
      user_word_list.append(lowerKazakh(user_word_written[i]))
    user_word = listToString(user_word_list)
    # record errors of  the student 
    print_corr = []
    tmp = 0
    helper = []
    if (len(wordCyrToLat(user_word)) == len(wordCyrToLat(self.word))):
      if (wordCyrToLat(user_word) != wordCyrToLat(self.word)):
        helper = wrongLetters_phrase(user_word, wordCyrToLat(self.word))
        #helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))
        tmp = 1
    else:
      helper = wrongLetters_phrase(user_word, wordCyrToLat(self.word))
    #  helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))
      tmp = 1

    #if (len(user_word_list) < len(stringToList(wordCyrToLat(self.word)))/2 or len(helper) > len(user_word_list)*0.8 or len(user_word.split()) <= 1):
    if len(helper) > len(user_word_list)*0.55:
      print("bileberda")
      self.letters = self.letters_copy
      self.challenges = self.challenges_copy
      self.errors_easy = self.errors_easy_copy
      self.errors_hard = self.errors_hard_copy
      
    else:
      for i in range(len(helper)):
        if helper[i]!=' ' and helper[i] != '.' and helper[i]!='–' and helper[i]!= '—'  and helper[i] != '?'and helper[i] != '-'and helper[i] != ',' and helper[i] != '!'and helper[i] != ':'and helper[i] != ';' and helper[i] != '…':
          if letter_score(helper[i])==1:
            if helper[i] not in self.errors_easy:
              self.errors_easy.append(helper[i])
              self.challenges = self.challenges + 1
          else:
            if helper[i] not in self.errors_hard:
              self.errors_hard.append(helper[i])
              self.challenges = self.challenges + 3
              
    #hasError = 0
    self.err_hst.append(len(self.errors_easy) + 3*len(self.errors_hard))
    for i in range(len(self.word)):
      if (cyrToLat(self.word[i]) not in helper):
        if (i == 0):
          print_corr.append(upperKazakh(cyrToLat(self.word[i])))
        else:
          print_corr.append(cyrToLat(self.word[i]))
      else:
        if (i == 0):
          print_corr.append(upperKazakh(cyrToLat(self.word[i])))
        else:
          print_corr.append(cyrToLat(self.word[i]))
        #print_corr.append(upperKazakh(cyrToLat(self.word[i])))
        #hasError = 1
        

        
    self.info[5] = len(self.errors_easy) + len(self.errors_hard)
    #if hasError == 1:

    self.logfile.write("Current problematic easy letters: ")
    for letter in self.errors_easy:
      #print(letter, end = " ")
      self.logfile.write(letter + " ")
    #   self.score = self.score + 1
    self.logfile.write("\nCurrent problematic hard letters: ")
    for letter in self.errors_hard:
      #print(letter, end = " ")
      self.logfile.write(letter + " ")
    #print("")
    self.logfile.write("\n")
    print_corr2 = ''
    #list_of_praises = ['You are doing great!','Good job!','Keep going!','You should be proud!', 'Keep it up!',"That's coming along nicely!","You've got it!",'You rock!','Great you are!','Well done!','Nice going!','Keep on trying!']
    if tmp==1:
      if (len(helper) <= 3):
        bot.send_message(message.chat.id, one_mistake())
      else:
        bot.send_message(message.chat.id, more_than_one_mistake ())
        #the correct writing is:
      bot.send_message(message.chat.id, '✅ '+print_corr2.join(print_corr))
    else:
      bot.send_message(message.chat.id, no_mistakes())
    #self.logfile.close()

    # UNCOMMENT WHEN FIX CSV  
    temp_dict = {'id': self.info[0], 'total_time': self.info[1], 'interaction_date_and_time': self.info[2], 'num_of_iterations': self.counter, 'explored_letters': self.info[4], 'problem_letters': self.info[5], 'avg_time_per_iteration': self.info[6], '(time 1-N)': self.info[7]}
    
    
    # self.writer.writerow(temp_dict)
    print(self.info)
    
    # UNCOMMENT WHEN FIX CSV
    self.csv_file.close()

    self.getLike(self.id, self.counter)
    
    self.counter = self.counter + 1
    time_elapsed = time_elapsed//5
    if time_elapsed>24:
      time_elapsed = 24
    self.state_lettersRL = []
    self.state_levelRL = []
    specifics = 0
    commons = 0
    for i in range(len(self.letters)):
      if self.letters[i]==0 and letter_score(self.kazakh_letters[i])==1:
        specifics = specifics + 1
      elif self.letters[i]==0 and letter_score(self.kazakh_letters[i])==3:
        commons = commons + 1
    sp = 0
    if specifics <= 1:
      sp = 0
    elif specifics < 5:
      sp = 1
    elif specifics < 9:
      sp = 2
    else:
      sp = 3
    self.state_lettersRL.append('unexplored spec. lett-s score: ' + str(sp))


    cm = 0
    if commons == 0:
      cm = 0
    elif commons < 3:
      cm = 1
    elif commons < 6:
      cm = 2
    else:
      cm = 3
    self.state_lettersRL.append('unexplored com. lett-s score: ' + str(cm))
    
    sp = 0
    cm = 0
    errors_easy = len(self.errors_easy)
    if errors_easy == 0:
      cm = 0
    elif errors_easy < 3:
      cm = 1
    elif errors_easy < 6:
      cm = 2
    else:
      cm = 3
    self.state_lettersRL.append('num of com. errors: ' + str(cm))
        
    errors_hard = len(self.errors_hard)
    if errors_hard == 0:
      sp = 0
    elif errors_hard < 3:
      sp = 1
    elif errors_hard < 6:
      sp = 2
    else:
      sp = 3
    self.state_lettersRL.append('num of spec. errors: ' + str(sp))
    self.state_lettersRL = ' '.join(self.state_lettersRL)
    
    
    if self.theme == 0 or self.theme == 1 or self.theme == 2:
      self.state_levelRL.append('level: 0')
    else:
      self.state_levelRL.append('level: 1')

    if self.theme == 0 or self.theme == 3:
      self.state_levelRL.append('theme: 0')
    elif self.theme == 1 or self.theme == 4:
      self.state_levelRL.append('theme: 1')
    elif self.theme == 2 or self.theme == 5:
      self.state_levelRL.append('theme: 2')
      
    #self.state.append('gender: ' + str(self.gender))
    
    # proportion = 0
    # if time_elapsed/len(self.word) < 0.05:
    #   proportion = 0
    # elif time_elapsed/len(self.word) < 0.14 and time_elapsed/len(self.word)>=0.05: 
    #   proportion = 1
    # elif time_elapsed/len(self.word) < 0.23 and time_elapsed/len(self.word)>=0.14:
    #   proportion = 2
    # else:
    #   proportion = 3
    # self.state_levelRL.append('time proportion: ' + str(proportion))
    # self.state_levelRL = ' '.join(self.state_levelRL)
    slope = 0
    if len(self.err_hst)>1:
        slope,sh = np.polyfit(list(range(0, len(self.err_hst))), self.err_hst, 1)
    if slope < -0.25:
      slope = 0
    elif slope >= -0.25 and slope < 0:
      slope = 1
    elif slope >= 0 and slope < 0.25:
      slope = 2
    else:
      slope = 3

    self.state_levelRL.append('current slope ' + str(slope))
    self.state_levelRL = ' '.join(self.state_levelRL)
    
    self.action_lettersRL = self.act_lettersRL(self.state_lettersRL, self.epsilon)
    self.action_levelRL = self.act_levelRL(self.state_levelRL, self.epsilon)
    if self.action_levelRL == 0 and self.theme>2:
      self.theme = self.theme - 3
    elif self.action_levelRL == 2 and self.theme<3:
      self.theme = self.theme + 3

    # done = False
    changed = False
    self.logfile.write("Action selected by LEVEL agent: " + self.actions_codes2[self.action_levelRL] + "\n")
    #print("action selected: " + self.actions_codes[action])
    self.challenges_copy = self.challenges
    self.errors_easy_copy = self.errors_easy
    self.errors_hard_copy = self.errors_hard
    ###################### 1 Feb
    passed = False
    while not passed:
      try:
        self.action_lettersRL = self.act_lettersRL(self.state_lettersRL, self.epsilon)
        self.logfile.write("Action selected by LETTERS agent: " + self.actions_codes[self.action_lettersRL] + "\n")
        if self.action_lettersRL == 0:
          if not self.errors_easy:
            self.qValues_lettersRL[(self.state_lettersRL, self.action_lettersRL)] = -math.inf
            self.action_lettersRL = 1
            changed = True
            self.logfile.write("No errors in easy letters, action was changed to: " + self.actions_codes[self.action_lettersRL] + "\n")
          else:
            s = random.choice(self.errors_easy)
            tmp = []
            letter_weights = []
            for idx in self.list_of_lists[self.theme]:
              tmp.append(tuple(idx))
              letter_weights.append(idx[2][convert_letter_to_index(lowerKazakh(latToCyr(s)))])
            
            #tmp = [idx for idx in self.list_of_lists[self.theme] if latToCyr(s) in idx[0]] ###### HERE
            #print(s)
              
            # convert to power
            power_letter_weights = []
            
            for weight in letter_weights:
              power_letter_weights.append(pow(weight, 8))
            
            old = True
            oldsCounter = 0
            while old:
              length_of_list = len(self.list_of_lists[self.theme])
              pre_x = random.choices(list(range(0,length_of_list)), weights = power_letter_weights, k=1)
              #x = random.choices(tmp, weights = letter_weights, k=1)
              #x = random.choices(self.list_of_lists[self.theme], weights = power_letter_weights, k=1)
              #x = self.list_of_lists[self.theme][pre_x[0]]
              x = []
              x.append(self.list_of_lists[self.theme][pre_x[0]])
              #print(self.list_of_lists[self.theme][pre_x[0]])
              #print(x)

              # reduce weights of that phrase
              
              #index_x = self.list_of_lists[self.theme].index(x)
              for i in range(0, len(self.list_of_lists[self.theme][pre_x[0]][2])):
                self.list_of_lists[self.theme][pre_x[0]][2][i] = self.list_of_lists[self.theme][pre_x[0]][2][i]/10
              #self.list_of_lists[self.theme][pre_x[0]][2] = helper_letter_weights

              self.word = x[0][0]
              self.author = x[0][1]
              #self.word = x[0]
              #self.author = x[1]
              if self.word not in self.oldPhrases:
                old = False
                self.oldPhrases.append(self.word)
              if oldsCounter > 2: # adjust this value 
                old = False
              oldsCounter = oldsCounter + 1

            
            
            
            self.logfile.write("\n")
            self.logfile.write("Next selected word: " + self.word + " resolves problematic letter " + s + "\n")
            #self.errors_copy = self.errors
            self.errors_easy.remove(s)  # CORRECT THIS
            self.logfile.write("Remaining problematic easy letters: "+ str(self.errors_easy) + "\n")
            print(self.word)
            self.letters_copy = self.letters
            for c in self.word:
              if c != ' ' and c != '.' and c!='–' and c!= '—'  and c != '?'and c != '-'and c != ',' and c != '!'and c != ':'and c != ';' and c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
                self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1 
            self.logfile.write("Updated list of remaining letters to explore: ")
            for idx in range(len(self.letters)):
              if self.letters[idx] == 0:
                self.logfile.write(self.kazakh_letters[idx] + " ")
            self.logfile.write("\n")
    
        if self.action_lettersRL == 1:
          sublist = []
          for j in range(len(self.kazakh_letters)):
            if self.letters[j]==0 and letter_score(self.kazakh_letters[j])==1:
              sublist.append(self.kazakh_letters[j])
          if len(sublist)!=0:
            tmp = [idx for idx in self.list_of_lists[self.theme] if random.choice(sublist) in idx[0]]
            if len(tmp) != 0:

              old = True
              oldsCounter = 0
              while old:
                x = random.choice(tmp)
                self.word = x[0]
                self.author = x[1]
                if self.word not in self.oldPhrases:
                  old = False
                  self.oldPhrases.append(self.word)
                if oldsCounter > 2: # adjust this value 
                  old = False
                oldsCounter = oldsCounter + 1

              
            else:

              old = True
              oldsCounter = 0
              while old:
                x = random.choice( self.list_of_lists[self.theme])
                self.word = x[0]
                self.author = x[1]
                if self.word not in self.oldPhrases:
                  old = False
                  self.oldPhrases.append(self.word)
                if oldsCounter > 2: # adjust this value 
                  old = False
                oldsCounter = oldsCounter + 1

          else:

            old = True
            oldsCounter = 0
            while old:
              x = random.choice( self.list_of_lists[self.theme])
              self.word = x[0]
              self.author = x[1]
              if self.word not in self.oldPhrases:
                old = False
                self.oldPhrases.append(self.word)
              if oldsCounter > 2: # adjust this value 
                old = False
              oldsCounter = oldsCounter + 1

            
          self.logfile.write("\n")
          self.logfile.write("Next selected word: " + self.word + "\n")
          print(self.word)
          self.letters_copy = self.letters
          for c in self.word:
            if c != ' ' and c != '.' and c != '?'and c != '-' and c != ',' and c!='–'and c!='—' and c != '!'and c != ':'and c != ';' and c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
              self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
          self.logfile.write("Updated list of remaining letters to explore: ")
          for idx in range(len(self.letters)):
            if self.letters[idx] == 0:
              self.logfile.write(self.kazakh_letters[idx] + " ")
          self.logfile.write("\n")
        


        ################# AND HERE
        if self.action_lettersRL == 2:
          if not self.errors_hard:
            self.qValues_lettersRL[(self.state_lettersRL, self.action_lettersRL)] = -math.inf
            self.action_lettersRL = 1
            changed = True
            self.logfile.write("No errors in hard letters, action was changed to: " + self.actions_codes[self.action_lettersRL] + "\n")
          else:
            s = random.choice(self.errors_hard)
            tmp = []
            letter_weights = []
            for idx in self.list_of_lists[self.theme]:
              tmp.append(tuple(idx))
              letter_weights.append(idx[2][convert_letter_to_index(lowerKazakh(latToCyr(s)))])
            
            #tmp = [idx for idx in self.list_of_lists[self.theme] if latToCyr(s) in idx[0]] ###### HERE
            #print(s)

            # convert to power
            power_letter_weights = []
            
            for weight in letter_weights:
              power_letter_weights.append(pow(weight, 8))
              
            old = True
            oldsCounter = 0
            while old:
              length_of_list = len(self.list_of_lists[self.theme])
              pre_x = random.choices(list(range(0,length_of_list)), weights = power_letter_weights, k=1)
              #x = random.choices(tmp, weights = letter_weights, k=1)
              #x = random.choices(self.list_of_lists[self.theme], weights = power_letter_weights, k=1)
              #x = self.list_of_lists[self.theme][pre_x[0]]
              x = []
              x.append(self.list_of_lists[self.theme][pre_x[0]])
              #print(self.list_of_lists[self.theme][pre_x[0]])
              #print(x)

              # reduce weights of that phrase
              
              #index_x = self.list_of_lists[self.theme].index(x)
              for i in range(0, len(self.list_of_lists[self.theme][pre_x[0]][2])):
                self.list_of_lists[self.theme][pre_x[0]][2][i] = self.list_of_lists[self.theme][pre_x[0]][2][i]/10
              #self.list_of_lists[self.theme][pre_x[0]][2] = helper_letter_weights

              self.word = x[0][0]
              self.author = x[0][1]
              #self.word = x[0]
              #self.author = x[1]
              if self.word not in self.oldPhrases:
                old = False
                self.oldPhrases.append(self.word)
              if oldsCounter > 2: # adjust this value 
                old = False
              oldsCounter = oldsCounter + 1

            
            
            
            self.logfile.write("\n")
            self.logfile.write("Next selected word: " + self.word + " resolves problematic letter " + s + "\n")
            #self.errors_copy = self.errors
            self.errors_hard.remove(s)  # CORRECT THIS
            self.logfile.write("Remaining problematic easy letters: "+ str(self.errors_hard) + "\n")
            print(self.word)
            self.letters_copy = self.letters
            for c in self.word:
              if c != ' ' and c != '.' and c!='–' and c!= '—'  and c != '?'and c != '-'and c != ',' and c != '!'and c != ':'and c != ';' and c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
                self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1 
            self.logfile.write("Updated list of remaining letters to explore: ")
            for idx in range(len(self.letters)):
              if self.letters[idx] == 0:
                self.logfile.write(self.kazakh_letters[idx] + " ")
            self.logfile.write("\n")
    
        if self.action_lettersRL == 3:
          sublist = []
          for j in range(len(self.kazakh_letters)):
            if self.letters[j]==0 and letter_score(self.kazakh_letters[j])==3:
              sublist.append(self.kazakh_letters[j])
          if len(sublist)!=0:
            tmp = [idx for idx in self.list_of_lists[self.theme] if random.choice(sublist) in idx[0]]
            if len(tmp) != 0:

              old = True
              oldsCounter = 0
              while old:
                x = random.choice(tmp)
                self.word = x[0]
                self.author = x[1]
                if self.word not in self.oldPhrases:
                  old = False
                  self.oldPhrases.append(self.word)
                if oldsCounter > 2: # adjust this value 
                  old = False
                oldsCounter = oldsCounter + 1

              
            else:

              old = True
              oldsCounter = 0
              while old:
                x = random.choice( self.list_of_lists[self.theme])
                self.word = x[0]
                self.author = x[1]
                if self.word not in self.oldPhrases:
                  old = False
                  self.oldPhrases.append(self.word)
                if oldsCounter > 2: # adjust this value 
                  old = False
                oldsCounter = oldsCounter + 1

          else:

            old = True
            oldsCounter = 0
            while old:
              x = random.choice( self.list_of_lists[self.theme])
              self.word = x[0]
              self.author = x[1]
              if self.word not in self.oldPhrases:
                old = False
                self.oldPhrases.append(self.word)
              if oldsCounter > 2: # adjust this value 
                old = False
              oldsCounter = oldsCounter + 1

            
          self.logfile.write("\n")
          self.logfile.write("Next selected word: " + self.word + "\n")
          print(self.word)
          self.letters_copy = self.letters
          for c in self.word:
            if c != ' ' and c != '.' and c != '?'and c != '-' and c != ',' and c!='–'and c!='—' and c != '!'and c != ':'and c != ';' and c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
              self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
          self.logfile.write("Updated list of remaining letters to explore: ")
          for idx in range(len(self.letters)):
            if self.letters[idx] == 0:
              self.logfile.write(self.kazakh_letters[idx] + " ")
          self.logfile.write("\n")
        passed = True
      except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        
        self.logfile.write("\nException met: "+ str(exc_type) + " in " + str(fname) + " line " + str(exc_tb.tb_lineno))
        pass
    
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
    self.info[4] = np.count_nonzero(self.letters)
    #print(">>>>>interaction with student begins")
    if len(self.author) > 10:
      name = convert_kazakh_to_english(self.author)

      text1 = "Could you please rewrite " + name + "'s following quote using Kazakh-Latin alphabet: \n⌨️ " + self.word
      text2 = "How the following quote of " + name + " would be written using Kazakh-Latin alphabet: \n⌨️ "+ self.word
      text3 = "Please rewrite " + name + "'s quote using Kazakh-Latin alphabet: \n⌨️ " + self.word
    else:
      
      text1 = "Could you please write the following using Kazakh-Latin alphabet: \n⌨️ "+ self.word
      text2 = "How this phrase would look like using Kazakh-Latin alphabet: \n⌨️ "+ self.word
      text3 = "Please rewrite the following using Kazakh-Latin alphabet: \n⌨️ "+ self.word


      if (self.action_lettersRL == 0 or self.action_lettersRL == 2):
        bot.send_message(message.chat.id, "Let's work on letter: " + latToCyr(s))
      elif (random.randint(0,2) == 0):
        bot.send_message(message.chat.id, "Let's work on some new letters")
        
    random_text = random.choices([text1, text2, text3])
    sent2 = bot.send_message(message.chat.id, random_text)
    self.start_time = time.time()
    self.logfile.close()
    self.info[3] = self.info[3] + 1
    bot.register_next_step_handler(sent2, self.process2)

  def praise(self, message):
    list_of_praises = ['You are doing great!','You are improving!','Good job!','Keep going!','You should be proud!', 'Keep it up!',"That's coming along nicely!","You've got it!",'You rock!',"You've made a lot of progress!",'Great you are!','Well done!','Getting better with time!','Nice going!','Keep on trying!']
    bot.send_message(message.chat.id, list_of_praises[0])
    
  def process2(self, message):
    self.logfile = open(str(self.id)+".txt", "a")
    user_word_written = message.text
    self.logfile.write("User's trial: " + user_word_written + "\n")
    self.end_time = time.time()
    self.time_elapsed = self.end_time - self.start_time
    
    self.logfile.write("Time of this interaction: " + str(self.time_elapsed) + "\n")
    self.time_total = self.time_total + self.time_elapsed
    
    self.info[1] = round(self.info[1] + self.time_total, 2)
    self.info[6] = round((self.info[6]*(self.counter - 1) + self.time_elapsed)/self.counter, 2)
    self.info[7].append(round(self.time_elapsed, 2))
    self.time_elapsed = self.time_elapsed//5
    if self.time_elapsed>24:
      self.time_elapsed = 24
    user_word_list = []
    for i in range(len(user_word_written)):
      user_word_list.append(lowerKazakh(user_word_written[i]))
    user_word = listToString(user_word_list)
    print_corr = []
    tmp = 0
    helper = []
    if (len(wordCyrToLat(user_word)) == len(wordCyrToLat(self.word))):
      if (wordCyrToLat(user_word) != wordCyrToLat(self.word)):
        helper = wrongLetters_phrase(user_word, wordCyrToLat(self.word))
        #helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))
        tmp = 1
    else:
      helper = wrongLetters_phrase(user_word, wordCyrToLat(self.word))
      #helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))
      tmp = 1

    #if (len(user_word_list) < len(stringToList(wordCyrToLat(self.word)))/2 or len(helper) > len(user_word_list)*0.8 or len(user_word.split()) <= 1):
    if len(helper) > len(user_word_list)*0.55:
      print("bileberda")
      self.letters = self.letters_copy
      self.challenges = self.challenges_copy
      self.errors_easy = self.errors_easy_copy
      self.errors_hard = self.errors_hard_copy
      
    else:
      for i in range(len(helper)):
        if helper[i]!=' ' and helper[i] != '.' and helper[i]!='–' and helper[i]!= '—'  and helper[i] != '?'and helper[i] != '-'and helper[i] != ',' and helper[i] != '!'and helper[i] != ':'and helper[i] != ';':
          if letter_score(helper[i])==1:
            if helper[i] not in self.errors_easy:
              self.errors_easy.append(helper[i])
              self.challenges = self.challenges + 1
          else:
            if helper[i] not in self.errors_hard:
              self.errors_hard.append(helper[i])
              self.challenges = self.challenges + 3


    
    self.err_hst.append(len(self.errors_easy) + 3*len(self.errors_hard))

    for i in range(len(self.word)):
      if (cyrToLat(self.word[i]) not in helper):
        if (i == 0):
          print_corr.append(upperKazakh(cyrToLat(self.word[i])))
        else:
          print_corr.append(cyrToLat(self.word[i]))
      else:
        if (i == 0):
          print_corr.append(upperKazakh(cyrToLat(self.word[i])))
        else:
          print_corr.append(cyrToLat(self.word[i]))
        #print_corr.append(upperKazakh(cyrToLat(self.word[i])))
    self.info[5] = len(self.errors_easy)+len(self.errors_hard)
    self.logfile.write("Current problematic letters: ")
    for letter in self.errors_easy:
      self.logfile.write(letter + " ")
    #   self.score = self.score + 1
    for letter in self.errors_hard:
      self.logfile.write(letter + " ")
    self.logfile.write("\n")
    print_corr2 = ''
    #list_of_praises = ['You are doing great!','Good job!','Keep going!','You should be proud!', 'Keep it up!',"That's coming along nicely!","You've got it!",'You rock!','Great you are!','Well done!','Nice going!','Keep on trying!']
    if tmp==1:
      if (len(helper) <= 3):
        bot.send_message(message.chat.id, one_mistake())
      else:
        bot.send_message(message.chat.id, more_than_one_mistake ())
      #bot.send_message(message.chat.id, random.choice(list_of_praises))
        #the correct writing is:
      bot.send_message(message.chat.id, '✅ '+print_corr2.join(print_corr))
    else:
      bot.send_message(message.chat.id, no_mistakes())

    # UNCOMMENT WHEN FIX CSV  
    self.csv_file = open("users_data_quotesRL.csv", "r")
    csv_columns = ['id', 'total_time', 'interaction_date_and_time', 'num_of_iterations', 'explored_letters', 'problem_letters', 'avg_time_per_iteration', '(time 1-N)']
    lines=csv.DictReader(self.csv_file,fieldnames=csv_columns,delimiter='\n')

    tmp = []
    for line in lines:
      tmp.append(line)
    tmp.pop()
    self.csv_file.close()
    self.csv_file = open("users_data_quotesRL.csv", "w+")
    
    self.writer = csv.DictWriter(self.csv_file, fieldnames=csv_columns) #csv.writer(self.csv_file)
    for t in tmp:
      self.writer.writerow(t)
    temp_dict = {'id': self.info[0], 'total_time': self.info[1], 'interaction_date_and_time': self.info[2], 'num_of_iterations': self.counter, 'explored_letters': self.info[4], 'problem_letters': self.info[5], 'avg_time_per_iteration': self.info[6], '(time 1-N)': self.info[7]}
    self.writer.writerow(temp_dict)
    self.csv_file.close()

    self.getLike(self.id, self.counter)


    next_state_lettersRL = []
    next_state_levelRL = []
    specifics = 0
    commons = 0
    for i in range(len(self.letters)):
      if self.letters[i]==0 and letter_score(self.kazakh_letters[i])==1:
        specifics = specifics + 1
      elif self.letters[i]==0 and letter_score(self.kazakh_letters[i])==3:
        commons = commons + 1
    sp = 0
    if specifics <= 1:
      sp = 0
    elif specifics < 5:
      sp = 1
    elif specifics < 9:
      sp = 2
    else:
      sp = 3
    next_state_lettersRL.append('unexplored spec. lett-s score: ' + str(sp))


    cm = 0
    if commons == 0:
      cm = 0
    elif commons < 3:
      cm = 1
    elif commons < 6:
      cm = 2
    else:
      cm = 3
    next_state_lettersRL.append('unexplored com. lett-s score: ' + str(cm))
    
    sp = 0
    cm = 0
    errors_easy = len(self.errors_easy)
    if errors_easy == 0:
      cm = 0
    elif errors_easy < 3:
      cm = 1
    elif errors_easy < 6:
      cm = 2
    else:
      cm = 3
    next_state_lettersRL.append('num of com. errors: ' + str(cm))
        
    errors_hard = len(self.errors_hard)
    if errors_hard == 0:
      sp = 0
    elif errors_hard < 3:
      sp = 1
    elif errors_hard < 6:
      sp = 2
    else:
      sp = 3
    next_state_lettersRL.append('num of spec. errors: ' + str(sp))
    next_state_lettersRL = ' '.join(next_state_lettersRL)
    
    
    if self.theme == 0 or self.theme == 1 or self.theme == 2:
      next_state_levelRL.append('level: 0')
    else:
      next_state_levelRL.append('level: 1')

    if self.theme == 0 or self.theme == 3:
      next_state_levelRL.append('theme: 0')
    elif self.theme == 1 or self.theme == 4:
      next_state_levelRL.append('theme: 1')
    elif self.theme == 2 or self.theme == 5:
      next_state_levelRL.append('theme: 2')
      
    #self.state.append('gender: ' + str(self.gender))
    
   # proportion = 0
  #  if self.time_elapsed/len(self.word) < 0.05:
  #    proportion = 0
  #  elif self.time_elapsed/len(self.word) < 0.14 and self.time_elapsed/len(self.word)>=0.05: 
   #   proportion = 1
   # elif self.time_elapsed/len(self.word) < 0.23 and self.time_elapsed/len(self.word)>=0.14:
  #    proportion = 2
   # else:
   #   proportion = 3
    #next_state_levelRL.append('time proportion: ' + str(proportion))
 #   next_state_levelRL = ' '.join(next_state_levelRL)
    slope = 0
    if len(self.err_hst)>1:
        slope,sh = np.polyfit(list(range(0, len(self.err_hst))), self.err_hst, 1)
    if slope < -0.25:
      slope = 0
    elif slope >= -0.25 and slope < 0:
      slope = 1
    elif slope >= 0 and slope < 0.25:
      slope = 2
    else:
      slope = 3

    next_state_levelRL.append('current slope ' + str(slope))
    next_state_levelRL = ' '.join(self.state_levelRL)  
    
    

    self.counter = self.counter + 1
    # if self.counter == 10:
    #   done = True

    # reward implementations here
  #  total = 0
  #  for ele in range(0, len(self.letters)):
   #   total = total + self.letters[ele]

    reward = 0
    # if len(helper) < len(user_word_list)/2: 
    #   if self.time_elapsed <60 and self.time_elapsed> 5:
    #     reward = 10
    #   else:
    #     reward = -50

    #   self.logfile.write("reward: " + str(reward) +"\n")

    #   nextQValues = [self.qValues.get((next_state_lettersRL, nextAction), 0) for nextAction in self.actions_lettersRL]
    #   nextValue = max(nextQValues)
    #   self.qValues_lettersRL[(self.state_lettersRL, self.action_lettersRL)] = (1 - self.alpha) * self.qValues.get((self.state_lettersRL, self.action_lettersRL), 0) \
    #                                       + self.alpha * (reward + self.discount * nextValue)
    
    # reward = 0
    # if len(helper) < len(user_word_list)/2: 
    #   if self.time_elapsed <60 and self.time_elapsed> 5:
    #     reward = 10
    #   else:
    #     reward = -50

    #   self.logfile.write("reward: " + str(reward) +"\n")

    #   nextQValues = [self.qValues.get((next_state_levelRL, nextAction), 0) for nextAction in self.actions_levelRL]
    #   nextValue = max(nextQValues)
    #   self.qValues_levelRL[(self.state_levelRL, self.action_levelRL)] = (1 - self.alpha) * self.qValues.get((self.state_levelRL, self.action_levelRL), 0) \
    #                                       + self.alpha * (reward + self.discount * nextValue)
    # if done:
    #   self.time_total = 0
    # if changed:
    #   self.qValues[(state, action)] = -math.inf
    #   action = changed_action
    self.gameIter_levelRL.append((self.state_levelRL, self.action_levelRL, reward, next_state_levelRL))
    self.gameIter_lettersRL.append((self.state_lettersRL, self.action_lettersRL, reward, next_state_lettersRL))
    self.state_levelRL = next_state_levelRL
    self.state_lettersRL = next_state_lettersRL
    
    self.action_levelRL = self.act_levelRL(self.state_levelRL, self.epsilon)
    if self.action_levelRL == 0 and self.theme>2:
      self.theme = self.theme - 3
    elif self.action_levelRL == 2 and self.theme<3:
      self.theme = self.theme + 3
    # action = self.act(state, self.epsilon)
    self.logfile.write("Action selected by LEVEL agent: " + self.actions_codes2[self.action_levelRL] + "\n")
    passed = False
    while not passed:
      try:
        self.action_lettersRL = self.act_lettersRL(self.state_lettersRL, self.epsilon)
        self.logfile.write("Action selected by LETTERS agent: " + self.actions_codes[self.action_lettersRL] + "\n")
        if self.action_lettersRL == 0:
          if not self.errors_easy:
            self.qValues_lettersRL[(self.state_lettersRL, self.action_lettersRL)] = -math.inf
            self.action_lettersRL = 1
            changed = True
            self.logfile.write("No errors in easy letters, action was changed to: " + self.actions_codes[self.action_lettersRL] + "\n")
          else:
            #tmp = [idx for idx in self.list_of_lists[self.theme] if cyrToLat(idx[0][0].lower()) in self.errors]
            s = random.choice(self.errors_easy)
            self.logfile.write("Resolves problematic letter: " + s + "\n")
            tmp = []
            letter_weights = []
            for idx in self.list_of_lists[self.theme]:
            #  tmp.append(tuple(idx))
              tmp.append(idx)
              letter_weights.append(idx[2][convert_letter_to_index(lowerKazakh(latToCyr(s)))])  

            power_letter_weights = []
            
            for weight in letter_weights:
              power_letter_weights.append(pow(weight, 8))
              
            old = True
            oldsCounter = 0
            while old:
              length_of_list = len(self.list_of_lists[self.theme])
              pre_x = random.choices(list(range(0,length_of_list)), weights = power_letter_weights, k=1)
              #x = random.choices(tmp, weights = letter_weights, k=1)
              #x = random.choices(self.list_of_lists[self.theme], weights = power_letter_weights, k=1)
              #x = self.list_of_lists[self.theme][pre_x[0]]
              x = []
              x.append(self.list_of_lists[self.theme][pre_x[0]])
              #print(self.list_of_lists[self.theme][pre_x[0]])
              #print(x)

              # reduce weights of that phrase
              
              #index_x = self.list_of_lists[self.theme].index(x)
              for i in range(0, len(self.list_of_lists[self.theme][pre_x[0]][2])):
                self.list_of_lists[self.theme][pre_x[0]][2][i] = self.list_of_lists[self.theme][pre_x[0]][2][i]/10
              #self.list_of_lists[self.theme][pre_x[0]][2] = helper_letter_weights

              
              self.word = x[0][0]
              self.author = x[0][1]
              if self.word not in self.oldPhrases:
                old = False
                self.oldPhrases.append(self.word)
              if oldsCounter > 2: # adjust this value 
                old = False
              oldsCounter = oldsCounter + 1
            self.logfile.write("\n")
            self.logfile.write("Next selected word: " + self.word + " resolves problematic letter " + s + "\n")
            self.errors_easy_copy = self.errors_easy
            self.challenges_copy = self.challenges
            self.errors_easy.remove(s)
            self.logfile.write("Remaining problematic easy letters: "+ str(self.errors_easy) + "\n")
            print(self.word)
            self.letters_copy = self.letters
      #      self.score = self.score - 1
            for c in self.word:
              if c != ' ' and c!='–' and c!='—' and c != '?'and c != '.'and c != '-' and c != ',' and c != '!'and c != ':'and c != ';'  and c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь' and c != '…':
                self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1 
            self.logfile.write("Updated list of remaining letters to explore: ")
            for idx in range(len(self.letters)):
              if self.letters[idx] == 0:
                self.logfile.write(self.kazakh_letters[idx] + " ")
            self.logfile.write("\n")
    
        if self.action_lettersRL == 1:
          sublist = []
          for j in range(len(self.kazakh_letters)):
            if self.letters[j]==0 and letter_score(self.kazakh_letters[j])==1:
              sublist.append(self.kazakh_letters[j])
          if len(sublist)!=0:
            tmp = [idx for idx in self.list_of_lists[self.theme] if random.choice(sublist) in idx[0]]
            if len(tmp) != 0:
              old = True
              oldsCounter = 0
              while old:
                x = random.choice(tmp)
                self.word = x[0]
                self.author = x[1]
                if self.word not in self.oldPhrases:
                  old = False
                  self.oldPhrases.append(self.word)
                if oldsCounter > 2: # adjust this value 
                  old = False
                oldsCounter = oldsCounter + 1
            else:
              old = True
              oldsCounter = 0
              while old:
                x = random.choice( self.list_of_lists[self.theme])
                self.word = x[0]
                self.author = x[1]
                if self.word not in self.oldPhrases:
                  old = False
                  self.oldPhrases.append(self.word)
                if oldsCounter > 2: # adjust this value 
                  old = False
                oldsCounter = oldsCounter + 1
          else:
            x = random.choice( self.list_of_lists[self.theme])
            self.word = x[0]
            self.author = x[1]
          self.logfile.write("\n")
          self.logfile.write("Next selected word: " + self.word + "\n")
          print(self.word)
          self.letters_copy = self.letters
          for c in self.word:
            if c != ' 'and c!='—' and c!='–' and c != '?' and c != '.' and c != '-'and c != ',' and c != '!'and c != ':'and c != ';' and c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
              self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
          self.logfile.write("Updated list of remaining letters to explore: ")
          for idx in range(len(self.letters)):
            if self.letters[idx] == 0:
              self.logfile.write(self.kazakh_letters[idx] + " ")
          self.logfile.write("\n")
        
        if self.action_lettersRL == 2:
          if not self.errors_hard:
            self.qValues_lettersRL[(self.state_lettersRL, self.action_lettersRL)] = -math.inf
            self.action_lettersRL = 1
            changed = True
            self.logfile.write("No errors in hard letters, action was changed to: " + self.actions_codes[self.action_lettersRL] + "\n")
          else:
            #tmp = [idx for idx in self.list_of_lists[self.theme] if cyrToLat(idx[0][0].lower()) in self.errors]
            s = random.choice(self.errors_hard)
            self.logfile.write("Resolves problematic letter: " + s + "\n")
            tmp = []
            letter_weights = []
            for idx in self.list_of_lists[self.theme]:
            #  tmp.append(tuple(idx))
              tmp.append(idx)
              letter_weights.append(idx[2][convert_letter_to_index(lowerKazakh(latToCyr(s)))])  

            power_letter_weights = []
            
            for weight in letter_weights:
              power_letter_weights.append(pow(weight, 8))
            old = True
            oldsCounter = 0
            while old:
              length_of_list = len(self.list_of_lists[self.theme])
              pre_x = random.choices(list(range(0,length_of_list)), weights = power_letter_weights, k=1)
              #x = random.choices(tmp, weights = letter_weights, k=1)
              #x = random.choices(self.list_of_lists[self.theme], weights = power_letter_weights, k=1)
              #x = self.list_of_lists[self.theme][pre_x[0]]
              x = []
              x.append(self.list_of_lists[self.theme][pre_x[0]])
              #print(self.list_of_lists[self.theme][pre_x[0]])
              #print(x)

              # reduce weights of that phrase
              
              #index_x = self.list_of_lists[self.theme].index(x)
              for i in range(0, len(self.list_of_lists[self.theme][pre_x[0]][2])):
                self.list_of_lists[self.theme][pre_x[0]][2][i] = self.list_of_lists[self.theme][pre_x[0]][2][i]/10
              #self.list_of_lists[self.theme][pre_x[0]][2] = helper_letter_weights

              
              self.word = x[0][0]
              self.author = x[0][1]
              if self.word not in self.oldPhrases:
                old = False
                self.oldPhrases.append(self.word)
              if oldsCounter > 2: # adjust this value 
                old = False
              oldsCounter = oldsCounter + 1
            self.logfile.write("\n")
            self.logfile.write("Next selected word: " + self.word + " resolves problematic letter " + s + "\n")
            self.errors_hard_copy = self.errors_hard
            self.errors_hard.remove(s)
            self.logfile.write("Remaining problematic easy letters: "+ str(self.errors_hard) + "\n")
            print(self.word)
            self.letters_copy = self.letters
      #      self.score = self.score - 1
            for c in self.word:
              if c != ' ' and c!='–' and c!='—' and c != '?'and c != '.'and c != '-' and c != ',' and c != '!'and c != ':'and c != ';'  and c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
                self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1 
            self.logfile.write("Updated list of remaining letters to explore: ")
            for idx in range(len(self.letters)):
              if self.letters[idx] == 0:
                self.logfile.write(self.kazakh_letters[idx] + " ")
            self.logfile.write("\n")
    
        if self.action_lettersRL == 3:
          sublist = []
          for j in range(len(self.kazakh_letters)):
            if self.letters[j]==0  and letter_score(self.kazakh_letters[j])==3:
              sublist.append(self.kazakh_letters[j])
          if len(sublist)!=0:
            tmp = [idx for idx in self.list_of_lists[self.theme] if random.choice(sublist) in idx[0]]
            if len(tmp) != 0:
              old = True
              oldsCounter = 0
              while old:
                x = random.choice(tmp)
                self.word = x[0]
                self.author = x[1]
                if self.word not in self.oldPhrases:
                  old = False
                  self.oldPhrases.append(self.word)
                if oldsCounter > 2: # adjust this value 
                  old = False
                oldsCounter = oldsCounter + 1
            else:
              old = True
              oldsCounter = 0
              while old:
                x = random.choice( self.list_of_lists[self.theme])
                self.word = x[0]
                self.author = x[1]
                if self.word not in self.oldPhrases:
                  old = False
                  self.oldPhrases.append(self.word)
                if oldsCounter > 2: # adjust this value 
                  old = False
                oldsCounter = oldsCounter + 1
          else:
            x = random.choice( self.list_of_lists[self.theme])
            self.word = x[0]
            self.author = x[1]
          self.logfile.write("\n")
          self.logfile.write("Next selected word: " + self.word + "\n")
          print(self.word)
          self.letters_copy = self.letters
          for c in self.word:
            if c != ' 'and c!='—' and c!='–' and c != '?' and c != '.' and c != '-'and c != ',' and c != '!'and c != ':'and c != ';' and c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
              self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
          self.logfile.write("Updated list of remaining letters to explore: ")
          for idx in range(len(self.letters)):
            if self.letters[idx] == 0:
              self.logfile.write(self.kazakh_letters[idx] + " ")
          self.logfile.write("\n")
        passed = True
      except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        
        self.logfile.write("\nException met: "+ str(exc_type) + " in " + str(fname) + " line " + str(exc_tb.tb_lineno))
        pass
        
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
    
    self.info[4] = np.count_nonzero(self.letters)
    self.logfile.close()
    if self.counter < 10:
      if len(self.author) > 10:
        name = convert_kazakh_to_english(self.author)
        text1 = "Could you please rewrite " + name + "'s following quote using Kazakh-Latin alphabet: \n⌨️ " + self.word
        text2 = "How the following quote of " + name + " would be written using Kazakh-Latin alphabet: \n⌨️ "+ self.word
        text3 = "Please rewrite " + name + "'s quote using Kazakh-Latin alphabet: \n⌨️ " + self.word

      else:
      
        text1 = "Could you please write the following using Kazakh-Latin alphabet: \n⌨️ "+ self.word
        text2 = "How this phrase would look like using Kazakh-Latin alphabet: \n⌨️ "+ self.word
        text3 = "Please rewrite the following using Kazakh-Latin alphabet: \n⌨️ "+ self.word

      
      if (self.action_lettersRL == 0 or self.action_lettersRL == 2):
        bot.send_message(message.chat.id, "Let's work on letter: " + latToCyr(s))
      elif (random.randint(0,2) == 0):
        bot.send_message(message.chat.id, "Let's work on some new letters")

      random_text = random.choices([text1, text2, text3])
      sent2 = bot.send_message(self.id, random_text)
      self.start_time = time.time()
      self.info[3] = self.info[3] + 1
      bot.register_next_step_handler(sent2, self.process2)
    else:
      self.getFeedback(self.id)

  def processFeedback(self, liked): 
    print(self.likes)
    phrasesLog = open(str(self.id)+"UsedPhrases.txt", "w")
    for line in self.oldPhrases:
      phrasesLog.write(line + "\n")
    phrasesLog.close()
    add_reward = 0
    if liked:
      add_reward = add_reward + 100
    else:
      add_reward = add_reward - 100
    
    slope,sh = np.polyfit(list(range(0, len(self.err_hst))), self.err_hst, 1)
    if slope < -0.25:
      add_reward = add_reward + 1000
    elif slope >= -0.25 and slope < 0:
      add_reward = add_reward + 500
      

    i = 0
    for (state, action, reward, nextState) in self.gameIter_levelRL[::-1]:  
      reward = reward + add_reward
      if self.likes[i] == 1:
        reward = reward + 100
      elif self.likes[i] == -1:
        reward = reward - 100
    
        
      nextQValues = [self.qValues_levelRL.get((nextState, nextAction), 0) for nextAction in self.actions_levelRL]
      nextValue = max(nextQValues)
      self.qValues_levelRL[(state, action)] = (1 - self.alpha) * self.qValues_levelRL.get((state, action), 0) \
                                      + self.alpha * (reward + self.discount * nextValue)
    self.saveQValues_levelRL()
    
    add_reward = 0

    if liked:
      add_reward = add_reward + 100
    else:
      add_reward = add_reward - 100

    add_reward = add_reward - (3*len(self.errors_hard) + len(self.errors_easy) - self.challenges )*10
    add_reward = add_reward + np.count_nonzero(self.letters)*10
    i = 0
    for (state, action, reward, nextState) in self.gameIter_lettersRL[::-1]:  
      reward = reward + add_reward
      if self.likes[i] == 1:
        reward = reward + 100
      elif self.likes[i] == -1:
        reward = reward - 100
    
        
      nextQValues = [self.qValues_lettersRL.get((nextState, nextAction), 0) for nextAction in self.actions_lettersRL]
      nextValue = max(nextQValues)
      self.qValues_lettersRL[(state, action)] = (1 - self.alpha) * self.qValues_lettersRL.get((state, action), 0) \
                                      + self.alpha * (reward + self.discount * nextValue)
    self.saveQValues_lettersRL()
    self.likes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    bot.send_message(self.id, "Thank you for your time! 😎")
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

  def act_lettersRL(self, state, epsilon):
      # this is an implementation of epsilon-greedy policy
      if random.random() < epsilon:
        #return random.randint(0, 4)
        return random.randint(0, 3)
  
      qValues = [self.qValues_lettersRL.get((state, action), 0) for action in self.actions_lettersRL]
  
      if np.all((qValues == 0)):
        #return random.randint(0, 4)
        return random.randint(0, 3)
      else:
        return np.argmax(qValues)

        
  def act_levelRL(self, state, epsilon):
      # this is an implementation of epsilon-greedy policy
      if random.random() < epsilon:
        #return random.randint(0, 4)
        return random.randint(0, 2)
  
      qValues = [self.qValues_levelRL.get((state, action), 0) for action in self.actions_levelRL]
  
      if np.all((qValues == 0)):
        #return random.randint(0, 4)
        return random.randint(0, 2)
      else:
        return np.argmax(qValues)

# import threading
# import time

# exitFlag = 0
# envs = defaultdict(OurEnvironment)
# class myThread (threading.Thread):
#    def __init__(self, id, name):
#       threading.Thread.__init__(self)
#       self.id = id
#       self.name = name
   
#    def run(self):
#       print ("Starting " + self.name)
#       env = OurEnvironment(0, self.id)
#       env.greet(self.id)
#       print ("Exiting " + self.name)

# threads = defaultdict(myThread)
# @bot.message_handler(commands = ['start'])
# def episode_start(message):
#   threads[message.chat.id] = myThread(message.chat.id, "Thread" +str(message.chat.id))
#   threads[message.chat.id].start()
#   for key in threads:
#     threads[key].join()
#   print ("complete")

class OurEnvironment1:
   #environment class goes here

  def loadQValues_lettersRL(self):
    #with open('qValues' + str(self.id) + '.json') as fp:
    with open('qValues_lettersRL_Quotes.json') as fp:
      toLoad = json.load(fp)
      self.qValues_lettersRL = {parseKey(key) : toLoad[key] for key in toLoad}


  def saveQValues_lettersRL(self):
    toSave = {key[0] + ' action ' + str(key[1]) : self.qValues_lettersRL[key] for key in self.qValues_lettersRL}
    with open(f'qValues_lettersRL_Quotes.json', 'w') as fp:
    #with open(f'qValues'+str(self.id) +'.json', 'w') as fp:
      json.dump(toSave, fp)
      
  def loadQValues_levelRL(self):
    #with open('qValues' + str(self.id) + '.json') as fp:
    with open('qValues_levelRL_Quotes.json') as fp:
      toLoad = json.load(fp)
      self.qValues_levelRL = {parseKey(key) : toLoad[key] for key in toLoad}


  def saveQValues_levelRL(self):
    toSave = {key[0] + ' action ' + str(key[1]) : self.qValues_levelRL[key] for key in self.qValues_levelRL}
    with open(f'qValues_levelRL_Quotes.json', 'w') as fp:
    #with open(f'qValues'+str(self.id) +'.json', 'w') as fp:
      json.dump(toSave, fp)

  def __init__(self, gender, id, adapt_to_gender = False):
    self.id = id
    if os.path.exists(str(id)+".txt"):
      self.logfile = open(str(self.id)+".txt", "a")
    else:
      self.logfile = open(str(self.id)+".txt", "w")
    self.gender = gender
    self.adapt_to_gender = adapt_to_gender
    self.gameIter_lettersRL = []
    self.gameIter_levelRL = []
    self.actions_lettersRL = [0, 1, 2, 3]
    self.actions_levelRL = [0, 1, 2]
    self.likes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # actions: 0 - keep the theme and keep learning the problematic letter
                                      # 1 - keep the theme and explore words with new letters
                                      # 2 - change the theme and keep learning the problematic letter
                                      # 3 - change the theme and explore words with new letters
                                      # 4 - ask advice from adult

    if os.path.exists("qValues_lettersRL_Quotes.json"):
      self.loadQValues_lettersRL()
    else:
      self.qValues_lettersRL = defaultdict(float)
    if os.path.exists("qValues_levelRL_Quotes.json"):
      self.loadQValues_levelRL()
    else:  
      self.qValues_levelRL = defaultdict(float)
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
    self.list_of_lists_weights = []
    self.weight_list1 = []
    self.weight_list2 = []
    self.weight_list3 = []
    self.weight_list4 = []
    self.weight_list5 = []
    self.list1 = ['апа', 'әже', 'бал', 'ваза', 'гүл', 'ғажап', 'дана', 'ерік', 'жауап', 'заман', 'ине', 'іс', 'көмек', 'қасық', 'лас', 'мамыр', 'неке', 'маңызды', 'осал', 'өрт', 'патша', 'рақым', 'сәуле', 'таза', 'ушу', 'ұя', 'үй', 'фарш', 'хат', 'шаш', 'ыдыс', 'ірімшік']
    self.list_of_lists.append(self.list1)
    for word in self.list1:
      self.weight_list1.append(count_letters_weights(word))
    self.list_of_lists_weights.append(self.weight_list1)
    self.list2 = ['аға', 'әке', 'бала','вагон', 'гу', 'ғарыш', 'дау', 'ереже', 'жігіт', 'заң', 'ит', 'шері', 'кеңес', 'қылыш', 'лай', 'мақсат', 'намыс', 'қараңғылық', 'от', 'өкім', 'піл', 'ру', 'сергек', 'тас', 'уәде', 'ұл', 'үй', 'факт', 'хабар', 'шарт', 'шәкір', 'ырыс', 'із']
    self.list_of_lists.append(self.list2)
    for word in self.list2:
      self.weight_list2.append(count_letters_weights(word))
    self.list_of_lists_weights.append(self.weight_list2)
    self.list3 = ['ауф', 'әйи', 'буу', 'вах', 'гыа', 'ғаф', 'дей', 'ефу', 'жае', 'зим', 'исе', 'кук', 'қаң', 'лаф', 'мах', 'нао', 'ңа', 'фао', 'өйи', 'паф', 'рут', 'саю', 'тац', 'уей', 'ұп', 'үф', 'фаш', 'хас', 'һа', 'шуй', 'ымм', 'іди']
    self.list_of_lists.append(self.list3)
    for word in self.list3:
      self.weight_list3.append(count_letters_weights(word))
    self.list_of_lists_weights.append(self.weight_list3)
    self.list4 = ['аргумент', 'барби', 'вальс', 'генерал', 'қарағанды', 'джем', 'евро', 'жираф', 'зомби', 'интернет', 'тапішке', 'конвертер', 'ақын', 'лимон', 'мама', 'нота', 'шаң', 'окей', 'өскемен', 'папа', 'робот', 'снайпер', 'танк', 'университет', 'ұлт', 'үй', 'фото', 'фильм', 'хакер', 'шоппинг'] 
    self.list_of_lists.append(self.list4)
    for word in self.list4:
      self.weight_list4.append(count_letters_weights(word))
    self.list_of_lists_weights.append(self.weight_list4)
    self.list5 = ['асқабақ', 'әлеуметтік', 'білезік', 'валенттілік', 'гуманитарлық', 'ғаламтор', 'денсаулық', 'егемендік', 'жүгері', 'заңдылық', 'ілтипат', 'игілік', 'кәсіптік', 'қанағаттандыру', 'лүпілдек', 'мүмкіндік', 'нәсихаттау', 'одақтастыру', 'өзімшілдік', 'пікірлес', 'рәміздер', 'сәулетті', 'тітіркендіру', 'уылдырық', 'ұсақтау', 'үлпілдек', 'фракцияшылдық', 'хәзірет', 'шаруашылық', 'ынтымақ', 'ізгілік']
    self.list_of_lists.append(self.list5)
    for word in self.list5:
      self.weight_list5.append(count_letters_weights(word))
    self.list_of_lists_weights.append(self.weight_list5)
    self.counter = 1                     # count words (if 10 -> new episode)
    self.actions_codes = ["work with problematic easy letters", "explore words with new easy letters", "work with problematic hard letters", "explore words with new hard letters", "ask advice from adult"]
    self.actions_codes2 = ["decrease difficulty level", "keep difficulty level", "increase difficulty level"]
    self.errors_easy = []
    self.errors_hard = []
    self.end_time = time.time()
    self.start_time = time.time()
    self.word = ""
    self.change_try_typing = 0
    self.err_hst = []
    
    # UNCOMMENT WHEN FIX CSV
    csv_columns = ['id', 'total_time', 'interaction_date_and_time', 'num_of_iterations', 'explored_letters', 'problem_letters', 'avg_time_per_iteration', '(time 1-N)']
    if os.path.exists("users_data_wordsRL.csv"):
      self.csv_file = open("users_data_wordsRL.csv", "a")
      self.writer = csv.DictWriter(self.csv_file, fieldnames=csv_columns)
    else:
      self.csv_file = open("users_data_wordsRL.csv", "w")
      self.writer = csv.DictWriter(self.csv_file, fieldnames=csv_columns) #csv.writer(self.csv_file)
      self.writer.writeheader()


    self.info = [self.id, 0, time.ctime(time.time()), 0, 0, 0, 0, []]
    self.state_lettersRL = []
    self.action_lettersRL = 0
    
    self.state_levelRL = []
    self.action_levelRL = 0
 # this is a method for assessing a word to a student. Provide a word and wait him/her to rewrite it. Also count time for response
  # def interact(self, word):
  #   print(word)
  #   start_time = time.time()
  #   user_word = input("Please, write this word: ")
  #   end_time = time.time()
  #   time_lapsed = end_time - start_time
  #   return user_word, time_lapsed
 

  def start_episode(self, message):
    bot.send_message(self.id, "Hello! Welcome to K-Qbot! This chatbot is dedicated to help you effectively learn Kazakh-Latin alphabet! Your id is: "+str(self.id)+'. Please, copy and paste the id into the survey.')
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
      self.logfile.write("Theme: GIRLS was selected. \n")
      #print("theme: GIRLS was selected")
    elif self.theme == 1:
      self.logfile.write("Theme: BOYS was selected. \n")
      #print("theme: BOYS was selected")
    else:
      self.logfile.write("Theme: Others was selected. \n")
      #print("theme: ANIMALS was selected")

  
    # select a random word in the given theme
    word_index = random.randint(0,len(self.list_of_lists[self.theme])-1)
    self.word = self.list_of_lists[self.theme][word_index]
    self.logfile.write("\n")
    self.logfile.write("The word assigned by database: " + self.word + "\n")
    #print("selected word: " + self.word)
    
    self.letters_copy = self.letters
    # indicate explored letters
    for c in self.word:
      if c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
        self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1     
    self.logfile.write("Updated list of remaining letters to explore: ")
    for idx in range(len(self.letters)):
      if self.letters[idx] == 0:
        self.logfile.write(self.kazakh_letters[idx] + " ")
        #print(chr(idx + ord('a')), end = " ")
    #print("")
    self.logfile.write("\n")
    
    self.info[4] = np.count_nonzero(self.letters)

    # show the word to student
    sent = bot.send_message(message.chat.id, please_try_typing(self.change_try_typing) + "\n" + "⌨️ " + self.word)
    if (self.change_try_typing != 4):
      self.change_try_typing = self.change_try_typing + 1
    else:
      self.change_try_typing = 0
    self.start_time = time.time()
    #self.logfile.close()
    self.letters_copy = self.letters
    self.challenges_copy = self.challenges
    self.errors_easy_copy = self.errors_easy
    self.errors_hard_copy = self.errors_hard
############# FROM HERE ###########################
    # the following commands the agent to wait a message from a user (when received methid process() starts)
    self.info[3] = self.info[3] + 1
    bot.register_next_step_handler(sent, self.process)

  def getFeedback(self, id):

    markup = types.InlineKeyboardMarkup()
    buttonA = types.InlineKeyboardButton('Like', callback_data=str(self.id)+'y')
    buttonB = types.InlineKeyboardButton('Dislike', callback_data=str(self.id)+'n')
    

    markup.row(buttonA, buttonB)

    bot.send_message(self.id, '🙃 ---End of the section--- 🙂\n'+'Did you like this interaction?', reply_markup=markup)


  def getLike(self, id, counter):

    markup = types.InlineKeyboardMarkup()
    buttonA = types.InlineKeyboardButton('Like', callback_data=str(self.id)+'x' + str(counter%10))
    buttonB = types.InlineKeyboardButton('Dislike', callback_data=str(self.id)+'y'+ str(counter%10))
    

    markup.row(buttonA, buttonB)

    bot.send_message(self.id, 'Did you like this phrase?', reply_markup=markup)

  def process(self, message):
    # the message of the user is obtained
    user_word0 = message.text
    user_word_written = ''
    for ch in user_word0:
      user_word_written = user_word_written + lowerKazakh(ch)
############# UNTIL HERE ##########################
    self.end_time = time.time()
    self.logfile.write("User's trial: " + user_word_written + "\n")
    time_elapsed = self.end_time - self.start_time
    self.logfile.write("Time of this interaction: " + str(time_elapsed) + "\n")
    self.time_total = self.time_total + time_elapsed
    self.info[1] = round(self.time_total, 2)
    self.info[6] = round(self.time_total, 2)
    self.info[7].append(round(time_elapsed, 2))
    user_word_list = []
    for i in range(len(user_word_written)):
      user_word_list.append(lowerKazakh(user_word_written[i]))
    user_word = listToString(user_word_list)
    # record errors of  the student 
    print_corr = []
    tmp = 0
    helper = []
    if (len(wordCyrToLat(user_word)) == len(wordCyrToLat(self.word))):
      if (wordCyrToLat(user_word) != wordCyrToLat(self.word)):
        helper = wrongLetters(user_word, wordCyrToLat(self.word))
        tmp = 1
    else:
      helper = wrongLetters(user_word, wordCyrToLat(self.word))
      tmp = 1

    if (len(helper) > len(user_word_list)*0.6 and len(helper) >= 3):
      print("bileberda")
      self.letters = self.letters_copy
      self.challenges = self.challenges_copy
      self.errors_easy = self.errors_easy_copy
      self.errors_hard = self.errors_hard_copy
      
    else:
      for i in range(len(helper)):
        if letter_score(helper[i])==1:
          if helper[i] not in self.errors_easy:
            self.errors_easy.append(helper[i])
            self.challenges = self.challenges + 1
        else:
          if helper[i] not in self.errors_hard:
            self.errors_hard.append(helper[i])
            self.challenges = self.challenges + 3
      
    self.err_hst.append(len(self.errors_easy) + 3*len(self.errors_hard))
    for i in range(len(self.word)):
      if (cyrToLat(self.word[i]) not in helper):
        print_corr.append(cyrToLat(self.word[i]))
      else:
        print_corr.append(cyrToLat(self.word[i]))
    self.info[5] = len(self.errors_easy)+len(self.errors_hard)

    self.logfile.write("Current problematic letters: ")
    for letter in self.errors_easy:
      #print(letter, end = " ")
      self.logfile.write(letter + " ")
    #   self.score = self.score + 1
    for letter in self.errors_hard:
      #print(letter, end = " ")
      self.logfile.write(letter + " ")
    #   self.score = self.score + 1
    #print("")
    self.logfile.write("\n")
    #list_of_praises = ['You are doing great!','Good job!','Keep going!','You should be proud!', 'Keep it up!',"That's coming along nicely!","You've got it!",'You rock!','Great you are!','Well done!','Nice going!','Keep on trying!']
    print_corr2 = ''
    if tmp==1:
      if (len(helper) == 1):
        bot.send_message(message.chat.id, one_mistake())
      else:
        bot.send_message(message.chat.id, more_than_one_mistake ())
      #bot.send_message(message.chat.id, random.choice(list_of_praises))
        #the correct writing is:
      bot.send_message(message.chat.id, '✅ '+print_corr2.join(print_corr))
    else:
      bot.send_message(message.chat.id, no_mistakes())
    #self.logfile.close()

     # UNCOMMENT WHEN FIX CSV 
    temp_dict = {'id': self.info[0], 'total_time': self.info[1], 'interaction_date_and_time': self.info[2], 'num_of_iterations': self.counter, 'explored_letters': self.info[4], 'problem_letters': self.info[5], 'avg_time_per_iteration': self.info[6], '(time 1-N)': self.info[7]}
    self.writer.writerow(temp_dict)
    print(self.info)

    # UNCOMMENT WHEN FIX CSV
    self.csv_file.close()

    self.getLike(self.id, self.counter)

    self.counter = self.counter + 1
    time_elapsed = time_elapsed//5
    if time_elapsed>10:
      time_elapsed = 10
    self.state_lettersRL = []
    self.state_levelRL = []
    specifics = 0
    commons = 0
    for i in range(len(self.letters)):
      if self.letters[i]==0 and letter_score(self.kazakh_letters[i])==1:
        specifics = specifics + 1
      elif self.letters[i]==0 and letter_score(self.kazakh_letters[i])==3:
        commons = commons + 1
    sp = 0
    if specifics <= 1:
      sp = 0
    elif specifics < 5:
      sp = 1
    elif specifics < 9:
      sp = 2
    else:
      sp = 3
    self.state_lettersRL.append('unexplored spec. lett-s score: ' + str(sp))


    cm = 0
    if commons == 0:
      cm = 0
    elif commons < 3:
      cm = 1
    elif commons < 6:
      cm = 2
    else:
      cm = 3
    self.state_lettersRL.append('unexplored com. lett-s score: ' + str(cm))
    
    sp = 0
    cm = 0
    errors_easy = len(self.errors_easy)
    if errors_easy == 0:
      cm = 0
    elif errors_easy < 3:
      cm = 1
    elif errors_easy < 6:
      cm = 2
    else:
      cm = 3
    self.state_lettersRL.append('num of com. errors: ' + str(cm))
        
    errors_hard = len(self.errors_hard)
    if errors_hard == 0:
      sp = 0
    elif errors_hard < 3:
      sp = 1
    elif errors_hard < 6:
      sp = 2
    else:
      sp = 3
    self.state_lettersRL.append('num of spec. errors: ' + str(sp))
    self.state_lettersRL = ' '.join(self.state_lettersRL)
    
    
    if self.theme == 0 or self.theme == 1 or self.theme == 2:
      self.state_levelRL.append('level: 0')
    else:
      self.state_levelRL.append('level: 1')

    if self.theme == 0 or self.theme == 3:
      self.state_levelRL.append('theme: 0')
    elif self.theme == 1 or self.theme == 4:
      self.state_levelRL.append('theme: 1')
    elif self.theme == 2 or self.theme == 5:
      self.state_levelRL.append('theme: 2')
      
    #self.state.append('gender: ' + str(self.gender))
    
    # proportion = 0
    # if time_elapsed/len(self.word) < 0.05:
    #   proportion = 0
    # elif time_elapsed/len(self.word) < 0.14 and time_elapsed/len(self.word)>=0.05: 
    #   proportion = 1
    # elif time_elapsed/len(self.word) < 0.23 and time_elapsed/len(self.word)>=0.14:
    #   proportion = 2
    # else:
    #   proportion = 3
    # self.state_levelRL.append('time proportion: ' + str(proportion))
    # self.state_levelRL = ' '.join(self.state_levelRL)
    slope = 0
    if len(self.err_hst)>1:
        slope,sh = np.polyfit(list(range(0, len(self.err_hst))), self.err_hst, 1)
    if slope < -0.25:
      slope = 0
    elif slope >= -0.25 and slope < 0:
      slope = 1
    elif slope >= 0 and slope < 0.25:
      slope = 2
    else:
      slope = 3

    self.state_levelRL.append('current slope ' + str(slope))
    self.state_levelRL = ' '.join(self.state_levelRL)
    
    self.action_lettersRL = self.act_lettersRL(self.state_lettersRL, self.epsilon)
    self.action_levelRL = self.act_levelRL(self.state_levelRL, self.epsilon)
    if self.action_levelRL == 0 and self.theme>2:
      self.theme = random.randint(0, 2)
    elif self.action_levelRL == 2 and self.theme<3:
      self.theme = random.randint(3, 4)

    # done = False
    changed = False
    self.logfile.write("Action selected by LEVEL agent: " + self.actions_codes2[self.action_levelRL] + "\n")
    self.logfile.write("Action selected by LETTERS agent: " + self.actions_codes[self.action_lettersRL] + "\n")
    #print("action selected: " + self.actions_codes[action])
    self.challenges_copy = self.challenges
    self.errors_easy_copy = self.errors_easy
    self.errors_hard_copy = self.errors_hard
    passed = False
    while not passed:
      try:
        if self.action_lettersRL == 0:
          if not self.errors_easy:
            self.qValues_lettersRL[(self.state_lettersRL, self.action_lettersRL)] = -math.inf
            self.action_lettersRL = 1
            changed = True
            self.logfile.write("No errors in easy letters, action was changed to: " + self.actions_codes[self.action_lettersRL] + "\n")
          else:
            #s = random.choice(self.errors_easy)
            #tmp = [idx for idx in self.list_of_lists[self.theme] if latToCyr(s) in idx]
            s = random.choice(self.errors_easy)
            tmp = []
            letter_weights = []
            for i in range (0, len(self.list_of_lists[self.theme])):
              tmp.append(tuple(self.list_of_lists[self.theme][i]))
              letter_weights.append(self.list_of_lists_weights[self.theme][i][convert_letter_to_index(lowerKazakh(latToCyr(s)))])
            power_letter_weights = []
            for weight in letter_weights:
              power_letter_weights.append(pow(weight, 4))
            #length_of_list = len(self.list_of_lists[self.theme])
            #pre_x = random.choices(list(range(0,length_of_list)), weights = power_letter_weights, k=1)
            #x = random.choices(tmp, weights = power_letter_weights, k=1)
            x = random.choices(self.list_of_lists[self.theme], weights = power_letter_weights, k=1)
            #x = self.list_of_lists[self.theme][pre_x[0]]
            #x = []
            #x.append(self.list_of_lists[self.theme][pre_x])
            #tmp = [idx for idx in self.list_of_lists[self.theme] if cyrToLat(idx[0].lower()) in self.errors]
            word_index = self.list_of_lists[self.theme].index(x[0])
            for i in range(0,len(self.list_of_lists_weights[self.theme][word_index])):
              self.list_of_lists_weights[self.theme][word_index][i] = self.list_of_lists_weights[self.theme][word_index][i]/10
            self.word = x[0]
            #self.word = random.choice(tmp)
            self.logfile.write("\n")
            self.logfile.write("Next selected word: " + self.word + " resolves problematic letter " + cyrToLat(self.word[0]) + "\n")
            # self.errors.remove(cyrToLat(self.word[0]))
            self.errors_easy_copy = self.errors_easy
            self.challenges_copy = self.challenges
            self.errors_easy.remove(s)
            self.logfile.write("Remaining problematic letters: "+ str(self.errors_easy) + "\n")
            self.letters_copy = self.letters
      #      self.score = self.score - 1
            for c in self.word:
              if c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
                self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1 
            self.logfile.write("Updated list of remaining letters to explore: ")
            for idx in range(len(self.letters)):
              if self.letters[idx] == 0:
                self.logfile.write(self.kazakh_letters[idx] + " ")
            self.logfile.write("\n")
    
        if self.action_lettersRL == 1:
          tmp = [idx for idx in self.list_of_lists[self.theme] if self.letters[self.kazakh_letters.index(cyrToLat(idx[0]))] == 0 and letter_score(self.kazakh_letters[self.kazakh_letters.index(cyrToLat(idx[0]))])==1]
          self.word = random.choice(tmp)
          self.logfile.write("\n")
          self.logfile.write("Next selected word: " + self.word + "\n")
          for c in self.word:
            if c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
              self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
          self.logfile.write("Updated list of remaining letters to explore: ")
          for idx in range(len(self.letters)):
            if self.letters[idx] == 0:
              self.logfile.write(self.kazakh_letters[idx] + " ")
          self.logfile.write("\n")
        
        if self.action_lettersRL == 2:
          if not self.errors_hard:
            self.qValues_lettersRL[(self.state_lettersRL, self.action_lettersRL)] = -math.inf
            transfer = random.choice([0,1,2,3])
            if transfer > 0:
              self.action_lettersRL = 0
            else:
              self.action_lettersRL = 3
            changed = True
            self.logfile.write("No errors in hard letters. Action was changed to " + self.actions_codes[self.action_lettersRL] + "\n")
          else:
            #s = random.choice(self.errors_hard)
            #tmp = [idx for idx in self.list_of_lists[self.theme] if latToCyr(s) in idx]
            s = random.choice(self.errors_hard)
            tmp = []
            letter_weights = []
            for i in range (0, len(self.list_of_lists[self.theme])):
              tmp.append(tuple(self.list_of_lists[self.theme][i]))
              letter_weights.append(self.list_of_lists_weights[self.theme][i][convert_letter_to_index(lowerKazakh(latToCyr(s)))])
            power_letter_weights = []
            for weight in letter_weights:
              power_letter_weights.append(pow(weight, 4))
            #length_of_list = len(self.list_of_lists[self.theme])
            #pre_x = random.choices(list(range(0,length_of_list)), weights = power_letter_weights, k=1)
            #x = random.choices(tmp, weights = power_letter_weights, k=1)
            x = random.choices(self.list_of_lists[self.theme], weights = power_letter_weights, k=1)
            #x = self.list_of_lists[self.theme][pre_x[0]]
            #x = []
            #x.append(self.list_of_lists[self.theme][pre_x])
            #tmp = [idx for idx in self.list_of_lists[self.theme] if cyrToLat(idx[0].lower()) in self.errors]
            word_index = self.list_of_lists[self.theme].index(x[0])
            for i in range(0,len(self.list_of_lists_weights[self.theme][word_index])):
              self.list_of_lists_weights[self.theme][word_index][i] = self.list_of_lists_weights[self.theme][word_index][i]/10
            self.word = x[0]
            #tmp = [idx for idx in self.list_of_lists[self.theme] if cyrToLat(idx[0].lower()) in self.errors]
            #self.word = random.choice(tmp)
            self.logfile.write("\n")
            self.logfile.write("Next selected word: " + self.word + " resolves problematic letter " + cyrToLat(self.word[0]) + "\n")
            # self.errors.remove(cyrToLat(self.word[0]))
            self.errors_hard_copy = self.errors_hard
            self.challenges_copy = self.challenges
            self.errors_hard.remove(s)
            self.logfile.write("Remaining problematic letters: "+ str(self.errors_hard) + "\n")
            self.letters_copy = self.letters
      #      self.score = self.score - 1
            for c in self.word:
              if c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
                self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1 
            self.logfile.write("Updated list of remaining letters to explore: ")
            for idx in range(len(self.letters)):
              if self.letters[idx] == 0:
                self.logfile.write(self.kazakh_letters[idx] + " ")
            self.logfile.write("\n")
        
        if self.action_lettersRL == 3:
          self.logfile.write("Theme changed from " + str(self.theme))
          self.theme = random.randint(0, 2)
          self.logfile.write(" to " + str(self.theme) + "\n")
          tmp = [idx for idx in self.list_of_lists[self.theme] if self.letters[self.kazakh_letters.index(cyrToLat(idx[0]))] == 0 and letter_score(self.kazakh_letters[self.kazakh_letters.index(cyrToLat(idx[0]))])==3]
          self.word = random.choice(tmp)
          self.logfile.write("\n")
          self.logfile.write("Next selected word: " + self.word + "\n")
          self.letters_copy = self.letters
          for c in self.word:
            if c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
              self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
          self.logfile.write("Updated list of remaining letters to explore:")
          for idx in range(len(self.letters)):
            if self.letters[idx] == 0:
              self.logfile.write(self.kazakh_letters[idx] + " ")
          self.logfile.write("\n")
        passed = True
      except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        
        self.logfile.write("\nException met: "+ str(exc_type) + " in " + str(fname) + " line " + str(exc_tb.tb_lineno))
        pass
    
    # # ask advice
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
    self.info[4] = np.count_nonzero(self.letters)
    if (self.action_lettersRL == 0 or self.action_lettersRL == 2):
      bot.send_message(message.chat.id, "Let's work on letter: " + latToCyr(s))
    elif (random.randint(0,2) == 0):
      bot.send_message(message.chat.id, "Let's work on some new letters")
    sent2 = bot.send_message(message.chat.id, please_try_typing(self.change_try_typing) + "\n" + "⌨️ " + self.word)
    if (self.change_try_typing != 4):
      self.change_try_typing = self.change_try_typing + 1
    else:
      self.change_try_typing = 0
    self.start_time = time.time()
    self.logfile.close()

############# FROM HERE ###########################
    self.info[3] = self.info[3] + 1
    bot.register_next_step_handler(sent2, self.process2)

  def process2(self, message):
    user_word0 = message.text
    user_word_written = ''
    for ch in user_word0:
      user_word_written = user_word_written + lowerKazakh(ch)

############# UNTIL HERE ##########################

    self.logfile = open(str(self.id)+".txt", "a")
    self.logfile.write("User's trial: " + user_word_written + "\n")
    self.end_time = time.time()
    time_elapsed = self.end_time - self.start_time
    self.logfile.write("Time of this interaction: " + str(time_elapsed) + "\n")
    self.time_total = self.time_total + time_elapsed
    self.info[1] = round(self.info[1] + self.time_total, 2)
    self.info[6] = round((self.info[6]*(self.counter - 1) + time_elapsed)/self.counter, 2)
    self.info[7].append(round(time_elapsed, 2))
    time_elapsed = time_elapsed//5
    if time_elapsed>10:
      time_elapsed = 10

    user_word_list = []
    for i in range(len(user_word_written)):
      user_word_list.append(lowerKazakh(user_word_written[i]))
    user_word = listToString(user_word_list)
    print_corr = []
    tmp = 0
    helper = []
    if (len(wordCyrToLat(user_word)) == len(wordCyrToLat(self.word))):
      if (wordCyrToLat(user_word) != wordCyrToLat(self.word)):
        helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))
        tmp = 1
    else:
      helper = wrongLetters(wordCyrToLat(user_word), wordCyrToLat(self.word))
      tmp = 1

    if (len(helper) > len(user_word_list)*0.6 and len(helper) >= 3):
      print("bileberda")
      self.letters = self.letters_copy
      self.challenges = self.challenges_copy
      self.errors_easy = self.errors_easy_copy
      self.errors_hard = self.errors_hard_copy
      
    else:
      for i in range(len(helper)):
        if letter_score(helper[i])==1:
          if helper[i] not in self.errors_easy:
            self.errors_easy.append(helper[i])
            self.challenges = self.challenges + 1
        else:
          if helper[i] not in self.errors_hard:
            self.errors_hard.append(helper[i])
            self.challenges = self.challenges + 3
      
    self.err_hst.append(len(self.errors_easy) + 3*len(self.errors_hard))
    for i in range(len(self.word)):
      if (cyrToLat(self.word[i]) not in helper):
        print_corr.append(cyrToLat(self.word[i]))
      else:
        print_corr.append(cyrToLat(self.word[i]))

    
    self.logfile.write("Current problematic letters: ")
    for letter in self.errors_easy:
      self.logfile.write(letter + " ")
    for letter in self.errors_hard:
      self.logfile.write(letter + " ")
    #   self.score = self.score + 1
    self.logfile.write("\n")
    print_corr2 = ''
    #list_of_praises = ['You are doing great!','Good job!','Keep going!','You should be proud!', 'Keep it up!',"That's coming along nicely!","You've got it!",'You rock!','Great you are!','Well done!','Nice going!','Keep on trying!']
    if tmp==1:
      if (len(helper) == 1):
        bot.send_message(message.chat.id, one_mistake())
      else:
        bot.send_message(message.chat.id, more_than_one_mistake ())
      #bot.send_message(message.chat.id, random.choice(list_of_praises))
        #the correct writing is:
      bot.send_message(message.chat.id,'✅ '+ print_corr2.join(print_corr))
    else:
      bot.send_message(message.chat.id, no_mistakes())

      # UNCOMMENT WHEN FIX CSV
    self.csv_file = open("users_data_wordsRL.csv", "r")
    csv_columns = ['id', 'total_time', 'interaction_date_and_time', 'num_of_iterations', 'explored_letters', 'problem_letters', 'avg_time_per_iteration', '(time 1-N)']
    lines=csv.DictReader(self.csv_file,fieldnames=csv_columns,delimiter='\n')

    tmp = []
    for line in lines:
      tmp.append(line)
    tmp.pop()
    self.csv_file.close()
    self.csv_file = open("users_data_wordsRL.csv", "w+")

    self.writer = csv.DictWriter(self.csv_file, fieldnames=csv_columns) #csv.writer(self.csv_file)

    for t in tmp:
      self.writer.writerow(t)
    temp_dict = {'id': self.info[0], 'total_time': self.info[1], 'interaction_date_and_time': self.info[2], 'num_of_iterations': self.counter, 'explored_letters': self.info[4], 'problem_letters': self.info[5], 'avg_time_per_iteration': self.info[6], '(time 1-N)': self.info[7]}
    self.writer.writerow(temp_dict)
    self.csv_file.close()
    
    self.getLike(self.id, self.counter)

    next_state_lettersRL = []
    next_state_levelRL = []
    specifics = 0
    commons = 0
    for i in range(len(self.letters)):
      if self.letters[i]==0 and letter_score(self.kazakh_letters[i])==1:
        specifics = specifics + 1
      elif self.letters[i]==0 and letter_score(self.kazakh_letters[i])==3:
        commons = commons + 1
    sp = 0
    if specifics <= 1:
      sp = 0
    elif specifics < 5:
      sp = 1
    elif specifics < 9:
      sp = 2
    else:
      sp = 3
    next_state_lettersRL.append('unexplored spec. lett-s score: ' + str(sp))


    cm = 0
    if commons == 0:
      cm = 0
    elif commons < 3:
      cm = 1
    elif commons < 6:
      cm = 2
    else:
      cm = 3
    next_state_lettersRL.append('unexplored com. lett-s score: ' + str(cm))
    
    sp = 0
    cm = 0
    errors_easy = len(self.errors_easy)
    if errors_easy == 0:
      cm = 0
    elif errors_easy < 3:
      cm = 1
    elif errors_easy < 6:
      cm = 2
    else:
      cm = 3
    next_state_lettersRL.append('num of com. errors: ' + str(cm))
        
    errors_hard = len(self.errors_hard)
    if errors_hard == 0:
      sp = 0
    elif errors_hard < 3:
      sp = 1
    elif errors_hard < 6:
      sp = 2
    else:
      sp = 3
    next_state_lettersRL.append('num of spec. errors: ' + str(sp))
    next_state_lettersRL = ' '.join(next_state_lettersRL)
    
    
    if self.theme >= 0 and self.theme < 3:
      next_state_levelRL.append('level: 0')
    else:
      next_state_levelRL.append('level: 1')

    
    next_state_levelRL.append('theme: ' + str(self.theme))
      
    #self.state.append('gender: ' + str(self.gender))
    
 #   proportion = 0
  #  if self.time_elapsed/len(self.word) < 0.05:
  #    proportion = 0
  #  elif self.time_elapsed/len(self.word) < 0.14 and self.time_elapsed/len(self.word)>=0.05: 
  #    proportion = 1
 #   elif self.time_elapsed/len(self.word) < 0.23 and self.time_elapsed/len(self.word)>=0.14:
  #    proportion = 2
  #  else:
  #    proportion = 3
    # next_state_levelRL.append('time proportion: ' + str(proportion))
  #  next_state_levelRL = ' '.join(next_state_levelRL)
    
    slope = 0
    if len(self.err_hst)>1:
        slope, sh= np.polyfit(list(range(0, len(self.err_hst))), self.err_hst, 1)
    if slope < -0.25:
      slope = 0
    elif slope >= -0.25 and slope < 0:
      slope = 1
    elif slope >= 0 and slope < 0.25:
      slope = 2
    else:
      slope = 3

    next_state_levelRL.append('current slope ' + str(slope))
    next_state_levelRL = ' '.join(self.state_levelRL)

    self.counter = self.counter + 1
    # if self.counter == 10:
    #   done = True

    # reward implementations here
  #  total = 0
  #  for ele in range(0, len(self.letters)):
   #   total = total + self.letters[ele]
    # if time_elapsed <60 and time_elapsed> 5:
    #   reward = 10
    # else:
    #   reward = -50
    # self.logfile.write("reward: " + str(reward) +"\n")
    reward = 0
    # nextQValues = [self.qValues.get((next_state, nextAction), 0) for nextAction in self.actions]
    # nextValue = max(nextQValues)
    # self.qValues[(self.state, self.action)] = (1 - self.alpha) * self.qValues.get((self.state, self.action), 0) \
    #                                     + self.alpha * (reward + self.discount * nextValue)
    # if done:
    #   self.time_total = 0
    # if changed:
    #   self.qValues[(state, action)] = -math.inf
    #   action = changed_action
    self.gameIter_levelRL.append((self.state_levelRL, self.action_levelRL, reward, next_state_levelRL))
    self.gameIter_lettersRL.append((self.state_lettersRL, self.action_lettersRL, reward, next_state_lettersRL))
    self.state_levelRL = next_state_levelRL
    self.state_lettersRL = next_state_lettersRL
    
    self.action_levelRL = self.act_levelRL(self.state_levelRL, self.epsilon)
    if self.action_levelRL == 0 and self.theme>2:
      self.theme = random.randint(0, 2)
    elif self.action_levelRL == 2 and self.theme<3:
      self.theme = random.randint(3, 4)
    self.logfile.write("Action selected by LEVEL agent: " + self.actions_codes2[self.action_levelRL] + "\n")
    passed = False
    while not passed:
      try:
        self.action_lettersRL = self.act_lettersRL(self.state_lettersRL, self.epsilon)
        self.logfile.write("Action selected LETTERS by agent: " + self.actions_codes[self.action_lettersRL] + "\n")
        if self.action_lettersRL == 0:
          if not self.errors_easy:
            self.qValues_lettersRL[(self.state_lettersRL, self.action_lettersRL)] = -math.inf
            self.action_lettersRL = 1
            # transfer = random.choice([0,1,2,3])
            # if transfer > 0:
            #   self.action_lettersRL = 2
            # else:
            #   self.action_lettersRL = 1
            changed = True
            self.logfile.write("No errors in easy letters, action was changed to: " + self.actions_codes[self.action_lettersRL] + "\n")
          else:
            #s = random.choice(self.errors_easy)
            #tmp = [idx for idx in self.list_of_lists[self.theme] if latToCyr(s) in idx]
            s = random.choice(self.errors_easy)
            tmp = []
            letter_weights = []
            for i in range (0, len(self.list_of_lists[self.theme])):
              tmp.append(tuple(self.list_of_lists[self.theme][i]))
              letter_weights.append(self.list_of_lists_weights[self.theme][i][convert_letter_to_index(lowerKazakh(latToCyr(s)))])
            power_letter_weights = []
            for weight in letter_weights:
              power_letter_weights.append(pow(weight, 4))
            #length_of_list = len(self.list_of_lists[self.theme])
            #pre_x = random.choices(list(range(0,length_of_list)), weights = power_letter_weights, k=1)
            #x = random.choices(tmp, weights = power_letter_weights, k=1)
            x = random.choices(self.list_of_lists[self.theme], weights = power_letter_weights, k=1)
            #x = self.list_of_lists[self.theme][pre_x[0]]
            #x = []
            #x.append(self.list_of_lists[self.theme][pre_x])
            #tmp = [idx for idx in self.list_of_lists[self.theme] if cyrToLat(idx[0].lower()) in self.errors]
            word_index = self.list_of_lists[self.theme].index(x[0])
            for i in range(0,len(self.list_of_lists_weights[self.theme][word_index])):
              self.list_of_lists_weights[self.theme][word_index][i] = self.list_of_lists_weights[self.theme][word_index][i]/10
            self.word = x[0]
            #self.word = random.choice(tmp)
            self.logfile.write("\n")
            self.logfile.write("Next selected word: " + self.word + " resolves problematic letter " + cyrToLat(self.word[0]) + "\n")
            self.errors_easy.remove(s)
            self.logfile.write("Remaining problematic letters: "+ str(self.errors_easy) + "\n")
            self.letters_copy = self.letters
      #      self.score = self.score - 1
            for c in self.word:
              if c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
                self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1 
            self.logfile.write("Updated list of remaining letters to explore: ")
            for idx in range(len(self.letters)):
              if self.letters[idx] == 0:
                self.logfile.write(self.kazakh_letters[idx] + " ")
            self.logfile.write("\n")
    
        if self.action_lettersRL == 1:
          tmp = [idx for idx in self.list_of_lists[self.theme] if self.letters[self.kazakh_letters.index(cyrToLat(idx[0]))] == 0 and letter_score(self.kazakh_letters[self.kazakh_letters.index(cyrToLat(idx[0]))])==1]
          self.word = random.choice(tmp)
          self.logfile.write("\n")
          self.logfile.write("Next selected word: " + self.word + "\n")
          self.letters_copy = self.letters
          for c in self.word:
            if c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
              self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
          self.logfile.write("Updated list of remaining letters to explore: ")
          for idx in range(len(self.letters)):
            if self.letters[idx] == 0:
              self.logfile.write(self.kazakh_letters[idx] + " ")
          self.logfile.write("\n")
        
        if self.action_lettersRL == 2:
          if not self.errors_hard:
            self.qValues_lettersRL[(self.state_lettersRL, self.action_lettersRL)] = -math.inf
            # transfer = random.choice([0,1,2,3])
            # if transfer > 0:
            #   self.action_lettersRL = 0
            # else:
            #   self.action_lettersRL = 3
            self.action_lettersRL = 3
            changed = True
            self.logfile.write("No errors in hard letters, action was changed to " + self.actions_codes[self.action_lettersRL] + "\n")
          else:
            # self.logfile.write("Theme changed from " + str(self.theme))
            # self.theme = random.randint(0, 2)
            # self.logfile.write(" to " + str(self.theme) + "\n")
            #s = random.choice(self.errors_hard)
            #tmp = [idx for idx in self.list_of_lists[self.theme] if latToCyr(s) in idx]
            s = random.choice(self.errors_hard)
            tmp = []
            letter_weights = []
            for i in range (0, len(self.list_of_lists[self.theme])):
              tmp.append(tuple(self.list_of_lists[self.theme][i]))
              letter_weights.append(self.list_of_lists_weights[self.theme][i][convert_letter_to_index(lowerKazakh(latToCyr(s)))])
            power_letter_weights = []
            for weight in letter_weights:
              power_letter_weights.append(pow(weight, 4))
            #length_of_list = len(self.list_of_lists[self.theme])
            #pre_x = random.choices(list(range(0,length_of_list)), weights = power_letter_weights, k=1)
            #x = random.choices(tmp, weights = power_letter_weights, k=1)
            x = random.choices(self.list_of_lists[self.theme], weights = power_letter_weights, k=1)
            #x = self.list_of_lists[self.theme][pre_x[0]]
            #x = []
            #x.append(self.list_of_lists[self.theme][pre_x])
            #tmp = [idx for idx in self.list_of_lists[self.theme] if cyrToLat(idx[0].lower()) in self.errors]
            word_index = self.list_of_lists[self.theme].index(x[0])
            for i in range(0,len(self.list_of_lists_weights[self.theme][word_index])):
              self.list_of_lists_weights[self.theme][word_index][i] = self.list_of_lists_weights[self.theme][word_index][i]/10
            self.word = x[0]
            #self.word = random.choice(tmp)
            self.logfile.write("\n")
            self.logfile.write("Next selected word: " + self.word + " resolves problematic letter " + cyrToLat(self.word[0]) + "\n")
            #self.errors.remove(cyrToLat(self.word[0]))
            self.errors_hard.remove(s)
            self.logfile.write("Remaining problematic easy letters: "+ str(self.errors_hard) + "\n")
      #      self.score = self.score - 1
            self.letters_copy = self.letters
            for c in self.word:
              if c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
                self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
            self.logfile.write("Updated list of remaining letters to explore:")
            for idx in range(len(self.letters)):
              if self.letters[idx] == 0:
                self.logfile.write(self.kazakh_letters[idx] + " ")
            self.logfile.write("\n")
        
        if self.action_lettersRL == 3:
          self.logfile.write("Theme changed from " + str(self.theme))
          self.theme = random.randint(0, 2)
          self.logfile.write(" to " + str(self.theme) + "\n")
          tmp = [idx for idx in self.list_of_lists[self.theme] if self.letters[self.kazakh_letters.index(cyrToLat(idx[0]))] == 0  and letter_score(self.kazakh_letters[self.kazakh_letters.index(cyrToLat(idx[0]))])==3]
          self.word = random.choice(tmp)
          self.logfile.write("\n")
          self.logfile.write("Next selected word: " + self.word + "\n")
          self.letters_copy = self.letters
          for c in self.word:
            if c != 'ъ' and c != 'Ъ' and c != 'ь' and c != 'Ь':
              self.letters[stringToList(self.kazakh_letters).index(cyrToLat(c))] = 1
          self.logfile.write("Updated list of remaining letters to explore:")
          for idx in range(len(self.letters)):
            if self.letters[idx] == 0:
              self.logfile.write(self.kazakh_letters[idx] + " ")
          self.logfile.write("\n")
        passed = True
      except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        
        self.logfile.write("\nException met: "+ str(exc_type) + " in " + str(fname) + " line " + str(exc_tb.tb_lineno))
        pass
    
    # # ask advice
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
    self.info[4] = np.count_nonzero(self.letters)
    self.logfile.close()
      
    if self.counter < 10:
      if (self.action_lettersRL == 0 or self.action_lettersRL == 2):
        bot.send_message(message.chat.id, "Let's work on letter: " + latToCyr(s))
      elif (random.randint(0,2) == 0):
        bot.send_message(message.chat.id, "Let's work on some new letters")
        
      sent2 = bot.send_message(message.chat.id, please_try_typing(self.change_try_typing) + "\n" + "⌨️ " + self.word)
      if (self.change_try_typing != 4):
        self.change_try_typing = self.change_try_typing + 1
      else:
        self.change_try_typing = 0

        

      self.start_time = time.time()
############# FROM HERE ###########################
      bot.register_next_step_handler(sent2, self.process2)
############# UNTIL HERE ##########################
    else:
      self.getFeedback(self.id)

  def processFeedback(self, liked): 
    #print(self.likes)
    add_reward = 0
    if liked:
      add_reward = add_reward + 50
    else:
      add_reward = add_reward - 100
    
    slope,sh  = np.polyfit(list(range(0, len(self.err_hst))), self.err_hst, 1)
    if slope < -0.25:
      add_reward = add_reward + 1000
    elif slope >= -0.25 and slope < 0:
      add_reward = add_reward + 500

    
    i = 0
    for (state, action, reward, nextState) in self.gameIter_levelRL[::-1]:  
      reward = reward + add_reward
      if self.likes[i] == 1:
        reward = reward + 100
      elif self.likes[i] == -1:
        reward = reward - 100
      nextQValues = [self.qValues_levelRL.get((nextState, nextAction), 0) for nextAction in self.actions_levelRL]
      nextValue = max(nextQValues)
      self.qValues_levelRL[(state, action)] = (1 - self.alpha) * self.qValues_levelRL.get((state, action), 0) \
                                      + self.alpha * (reward + self.discount * nextValue)
    self.saveQValues_levelRL()
    
    add_reward = 0
    
    if liked:
      add_reward = add_reward + 50
    else:
      add_reward = add_reward - 100
    
    
    add_reward = add_reward - (3*len(self.errors_hard) + len(self.errors_easy) - self.challenges )*10
    add_reward = add_reward + np.count_nonzero(self.letters)*10  
    i = 0
    for (state, action, reward, nextState) in self.gameIter_lettersRL[::-1]:  
      reward = reward + add_reward
      if self.likes[i] == 1:
        reward = reward + 100
      elif self.likes[i] == -1:
        reward = reward - 100
    
        
      nextQValues = [self.qValues_lettersRL.get((nextState, nextAction), 0) for nextAction in self.actions_lettersRL]
      nextValue = max(nextQValues)
      self.qValues_lettersRL[(state, action)] = (1 - self.alpha) * self.qValues_lettersRL.get((state, action), 0) \
                                      + self.alpha * (reward + self.discount * nextValue)
    self.saveQValues_lettersRL()
    
    self.likes =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    bot.send_message(self.id, "Good job! Now let's try something difficult. Command '/continue'")
  #return state, changed, action, reward, done





  def act_lettersRL(self, state, epsilon):
      # this is an implementation of epsilon-greedy policy
      if random.random() < epsilon:
        #return random.randint(0, 4)
        return random.randint(0, 3)
  
      qValues = [self.qValues_lettersRL.get((state, action), 0) for action in self.actions_lettersRL]
  
      if np.all((qValues == 0)):
        #return random.randint(0, 4)
        return random.randint(0, 3)
      else:
        return np.argmax(qValues)

        
  def act_levelRL(self, state, epsilon):
      # this is an implementation of epsilon-greedy policy
      if random.random() < epsilon:
        #return random.randint(0, 4)
        return random.randint(0, 2)
  
      qValues = [self.qValues_levelRL.get((state, action), 0) for action in self.actions_levelRL]
  
      if np.all((qValues == 0)):
        #return random.randint(0, 4)
        return random.randint(0, 2)
      else:
        return np.argmax(qValues)



envs1 = defaultdict(OurEnvironment1)
envs = defaultdict(OurEnvironment)
@bot.message_handler(commands = ['start'])
def episode_start(message):
  envs1[message.chat.id] = OurEnvironment1(0, message.chat.id)
  envs1[message.chat.id].start_episode(message)
@bot.message_handler(commands = ['continue'])
def episode_continue(message):
  envs[message.chat.id] = OurEnvironment(0, message.chat.id)
  envs[message.chat.id].greet(message)
  
  

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
  if (call.data[-1] == 'a'):
    bot.send_message(int(call.data[:-1]), "Great choice! You have chosen Kazakh poems!")
    #print(self.id)
  #       threads[message.chat.id] = myThread(message.chat.id, "Thread" +str(message.chat.id))
  #     threads[message.chat.id].start()
  # for key in threads:
  #   threads[key].join()
  # print ("complete")
    envs[int(call.data[:-1])].theme = 0
    envs[int(call.data[:-1])].start_episode()

  elif (call.data[-1] == 'b'):
    bot.send_message(int(call.data[:-1]), "Nice choice! You have chosen Kazakh music lyrics!")
    #print(self.id)
    envs[int(call.data[:-1])].theme = 1
    envs[int(call.data[:-1])].start_episode()
    
  elif (call.data[-1] == 'c'):
    bot.send_message(int(call.data[:-1]), "Interesting! You have chosen Kazakh famous quotes!")
    #print(self.id)
    envs[int(call.data[:-1])].theme = 2
    envs[int(call.data[:-1])].start_episode()
  elif (call.data[-1] == 'l'):
    bot.send_message(int(call.data[:-1]), "Thank you! 😁")
    #print(self.id)
    envs[int(call.data[:-1])].processFeedback(True)
  elif (call.data[-1] == 'd'):
    bot.send_message(int(call.data[:-1]), "Ok")
    #print(self.id)
    envs[int(call.data[:-1])].processFeedback(False)
  elif (call.data[-1] == 'y'):
    bot.send_message(int(call.data[:-1]), "Thank you! 🌝")
    #print(self.id)
    envs1[int(call.data[:-1])].processFeedback(True)
  elif (call.data[-1] == 'n'):
    bot.send_message(int(call.data[:-1]), "Ok")
    #print(self.id)
    envs1[int(call.data[:-1])].processFeedback(False)
  elif (call.data[-2] == 'x'):
    #bot.send_message(int(call.data[:-2]), "Thank you!")
    #print(self.id)
    envs1[int(call.data[:-2])].likes[int(call.data[-1])] = 1
  elif (call.data[-2] == 'y'):
    #bot.send_message(int(call.data[:-2]), "Ok")
    #print(self.id)
    envs1[int(call.data[:-2])].likes[int(call.data[-1])] = -1
  elif (call.data[-2] == 'a'):
    #bot.send_message(int(call.data[:-2]), "Thank you!")
    #print(self.id)
    envs[int(call.data[:-2])].likes[int(call.data[-1])] = 1
  elif (call.data[-2] == 'b'):
    #bot.send_message(int(call.data[:-2]), "Ok")
    #print(self.id)
    envs[int(call.data[:-2])].likes[int(call.data[-1])] = -1


def handle_queryLike(call):
  envs[int(call.data[:-1])].processFeedback(call.data[-1])


if __name__ == '__main__':
  bot.polling()
  # while True:
  #     try:
  #         bot.polling(none_stop=True)
  #     except Exception as e:
  #         time.sleep(3)
  #         exc_type, exc_obj, exc_tb = sys.exc_info()
  #         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
  #         print(exc_type, fname, exc_tb.tb_lineno)


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

  

  
