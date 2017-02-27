#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PA6, CS124, Stanford, Winter 2016
# v.1.0.2
# Original Python code by Ignacio Cases (@cases)
# Ported to Java by Raghav Gupta (@rgupta93) and Jennifer Lu (@jenylu)
######################################################################
import csv
import math

import numpy as np

from movielens import ratings
from random import randint
import portersalg as pa

class Chatbot:
    """Simple class to implement the chatbot for PA 6."""
    #############################################################################
    # `moviebot` is the default chatbot. Change it to your chatbot's name       #
    #############################################################################
    def __init__(self, is_turbo=False):
      self.name = 'Hillary Rodham Clinton'
      self.is_turbo = is_turbo
      self.user_name = ''
      self.read_data()
      self.num_to_recommend = 5
      self.arabic_to_roman = self.a_to_r()
      self.roman_to_arabic = self.r_to_a()
      #self.user_movies = [] #eventually use this to refer back to movies mentioned

    #############################################################################
    # 1. WARM UP REPL
    #############################################################################

    def greeting(self):
      """chatbot greeting message"""
      #############################################################################
      # Write a short greeting message                                      #
      #############################################################################

      #greeting_message = 'Hey there - it\'s nice to meet you! My name is Daniel, but you can call me Dan :) What is your name?'
      greeting_message = """My fellow American. My name is Hillary Rodham Clinton.
      As you know, America is going through difficult times. I’m tired of hiking in the woods,
      so I'm putting myself back out there and trying something new.
      \n In these troubling days of unconstitutional executive orders and laughable disregard for the
      laws and ideals of this country...I want to help you. Yes, you, my fellow American.
      It's important to march, to protest, to call your congresspeople, to vote,
      and to run for office. But every once in a while, we all need a break.
      And nothing beats a good ole movie night with family and friends.
      \n So, that's why I'm here. I've taken a break from my rigorous nap schedule to do this,
      and I'm glad you chose me to give you some movie advice.
      \nLet's get to know each other - what is your name?"""
      #############################################################################
      #                             END OF YOUR CODE                              #
      #############################################################################
      return greeting_message

    def goodbye(self):
      """chatbot goodbye message"""
      #############################################################################
      # Write a short farewell message                                      #
      #############################################################################

      goodbye_message = 'Great chatting with you - enjoy your movie!'

      #############################################################################
      #                             END OF YOUR CODE                              #
      #############################################################################

      return goodbye_message


    #############################################################################
    # 2. Modules 2 and 3: extraction and transformation                         #
    #############################################################################

    def process(self, input):
      """Takes the input string from the REPL and call delegated functions
      that
        1) extract the relevant information and
        2) transform the information into a response to the user
      """
      #############################################################################
      # TODO: Implement the extraction and transformation in this method, possibly#
      # calling other functions. Although modular code is not graded, it is       #
      # highly recommended                                                        #
      #############################################################################
      response = ''
      if self.is_turbo == True:
        response = 'processed %s in creative mode!!' % input
      else:
        #response = 'processed %s in starter mode' % input
        #response = ''

        score, stemmed_input = self.calcSentimentScore(input)
        #response = ' '.join(input.split())
        response = "The score is %d, The stemmed input is %s" % (score, stemmed_input)
      return response

    def a_to_r(self):
        d = {}
        d['1'] = 'I'
        d['2'] = 'II'
        d['3'] = 'III'
        d['4'] = 'IV'
        d['5'] = 'V'
        d['6'] = 'VI'
        d['7'] = 'VII'
        d['8'] = 'VIII'
        d['9'] = 'IX'
        d['10'] = 'X'
        d['15'] = 'XV'
        return d

    def r_to_a(self):
        d = {}
        d['I'] = '1'
        d['II'] = '2'
        d['III'] = '3'
        d['IV'] = '4'
        d['V'] = '5'
        d['VI'] = '6'
        d['VII'] = '7'
        d['VIII'] = '8'
        d['IX'] = '9'
        d['X'] = '10'
        d['XV'] = '11'
        d['XII'] = '12'
        d['XIII'] = '13'
        d['XIV'] = '14'
        d['XX'] = '20'
        d['XXI'] = '21'
        d['XXIV'] = '24'
        d['XXX'] = '30'
        d['XXXIII'] = '33'
        d['XLV'] = '45'
        d['LXIX'] = '69'
        d['XCIX'] = '99'
        d['CC'] = '200'
        d['M'] = '1000'
        d['MM'] = '2000'
        d['MMXLVI'] = '2046'
        return d


    def remove_punct(self, input):
        input = input.lower()
        punc = ['.', ',', ';', '!', '?', '/', '@', '#', '*', '&', '$', '-', '+', '\n', '(', ')', '\'']
        for p in punc:
          input = input.replace(p, ' ')
        return input

    def calcSentimentScore(self, input):
      #TODO: better metrics - emphasis if line contains many !!! or reaaallyyy
      score = 0
      input = self.remove_punct(input)
      sentence = ''
      split_input = input.split()
      for i in range(len(split_input)):
        w = split_input[i]
        prev = ''
        if i is not 0:
            prev = split_input[i-1]
        w = w.strip()
        prev = prev.strip()
        #if the word is not in our sentiment dictionary, try using the stemmed version
        if w not in self.sentiment:
          p = pa.PorterStemmer()
          w = p.returnStemmedWord(w)
        sentence += w
        sentence += ' '
        if w in self.sentiment:
          if self.sentiment[w] == 'neg':
              if prev == 'not':
                  score += 1
              else:
                  score -= 1
          elif self.sentiment[w] == 'pos':
              if prev == 'not':
                  score -= 1
              else:
                  score += 1
      return score, sentence
    #############################################################################
    # 3. Movie Recommendation helper functions                                  #
    #############################################################################

    def read_data(self):
      """Reads the ratings matrix from file"""
      # This matrix has the following shape: num_movies x num_users
      # The values stored in each row i and column j is the rating for
      # movie i by user j
      self.titles, self.ratings = ratings()
      reader = csv.reader(open('data/sentiment.txt', 'rb'))
      self.sentiment = dict(reader)
      self.sentiment['beautiful'] = 'pos'
      self.sentiment['fun'] = 'pos'
      self.sentiment['cool'] = 'pos'
      self.sentiment['beautiful'] = 'pos'

    def binarize(self):
      """Modifies the ratings matrix to make all of the ratings binary"""
      # Idea: +1 if the rating is > 2.5, -1 if it is <= 2.5, and 0 if it is not rated - DV
      #TODO: Can also try using each movie's average rating as its threshold
      threshhold = 2.5
      rows = self.ratings.shape[0]
      cols = self.ratings.shape[1]
      for i in range(rows):
          for j in range(cols):
              if self.ratings[i][j] >= 0.5 and self.ratings[i][j] <= threshold:
                  self.ratings[i][j] = -1
              elif self.ratings[i][j] > threshold:
                  self.ratings[i][j] = 1
      return self.ratings


    def distance(self, u, v):
      """Calculates a given distance function between vectors u and v"""
      # Implement the distance function between vectors u and v
      # Note: you can also think of this as computing a similarity measure
      #Idea: cosine similarity? -DV
      dot_product = np.dot(u, v) + 0.0
      u_norm = 0
      v_norm = 0
      for x in u:
          u_norm += x**2
      for y in v:
          v_norm += y**2
      u_norm = math.sqrt(u_norm)
      v_norm = math.sqrt(v_norm)
      return dot_product / (u_norm * v_norm)
      #if floating point, warnings, replace the above li
      #return dot_product / (u_norm * v_norm + 1e-7)

    """Given a list of (valid movie title w/o year, input with movie title removed) tuples,
       returns a list of (valid movie titles w/o year, sentiment ratings)"""
    def get_sentiment_for_movies(self, t):
        result = []
        for movie, rest in t:
            sentiment = calcSentimentScore(rest)
            result.append(movie, sentiment)

    def recommend(self, t):
      """Generates a list of movies based on the input vector u using
      collaborative filtering"""
      # Implement a recommendation function that takes a user vector u
      # and outputs a list of movies recommended by the chatbot
      # Assumes that t = [(movie w/o year, rest of sentence), (movie w/o year, rest of sentence), etc]

      index_of_j = [] #indices of the movies the user has commented on
      titles = self.getTitles()

      u = get_sentiment_for_movies(t)
      #i.e. u = [(movie1, rating1), (movie2, rating2) etc]
      for title, rating in u:
          index_of_j.append(titles.index(title))

      ri_list = [] #list of user's calculated rating for movie i
      for i in range(len(titles)):
          ri = 0 #user's calculated rating for movie i
          movie_i = self.ratings[i] #get the row in the ratings matrix for movie i
          for j in range(len(index_of_j)):
              index_of_movie_j = index_of_j[j]
              movie_j = self.ratings[index_of_movie_j]
              s_ij = distance(movie_i, movie_j)
              ri += s_ij * u[j][1] # s_ij * r_xj
              ri_list.append(ri)
      #index of first movie that has max predicted rating
      index_of_max_rating = ri_list.index(max(ri_list))
      return self.titles[index_of_max_rating]

    #############################################################################
    # 4. Debug info                                                             #
    #############################################################################

    def debug(self, input):
      """Returns debug information as a string for the input string from the REPL"""
      # Pass the debug information that you may think is important for your
      # evaluators
      debug_info = self.binarize()
      return debug_info


    #############################################################################
    # 5. Write a description for your chatbot here!                             #
    #############################################################################
    def intro(self):
      return """
      Your task is to implement the chatbot as detailed in the PA6 instructions.
      Remember: in the starter mode, movie names will come in quotation marks and
      expressions of sentiment will be simple!
      Write here the description for your own chatbot!
      """

    #############################################################################
    # Auxiliary methods for the chatbot.                                        #
    #                                                                           #
    # DO NOT CHANGE THE CODE BELOW!                                             #
    #                                                                           #
    #############################################################################

    def bot_name(self):
      return self.name


if __name__ == '__main__':
    Chatbot()
