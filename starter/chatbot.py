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

class Chatbot:
    """Simple class to implement the chatbot for PA 6."""
    #############################################################################
    # `moviebot` is the default chatbot. Change it to your chatbot's name       #
    #############################################################################
    def __init__(self, is_turbo=False):
      self.name = 'Meera and Devangi\'s MovieBot'
      self.is_turbo = is_turbo
      self.read_data()

    #############################################################################
    # 1. WARM UP REPL
    #############################################################################

    def greeting(self):
      """chatbot greeting message"""
      #############################################################################
      # Write a short greeting message                                      #
      #############################################################################

      greeting_message = 'Hey there - it\'s nice to meet you! My name is Daniel, but you can call me Dan :) What is your name?'

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

        score = self.calcSentimentScore(input)
        #response = ' '.join(input.split())
        response = "this is score %d" % score
      return response

    def removePunct(self, input):
        #TODO: add stemming
        input = input.lower()
        punc = ['.', ',', ';', '!', '?', '/', '@', '#', '*', '&', '$', '-', '+', '\n', '(', ')']
        for p in punc:
          input = input.replace(p, '')
        return input

    def calcSentimentScore(self, input):
      #TODO: implement negations
      score = 0
      input = self.removePunct(input)
      for word in input.split():
        if word in self.sentiment:
          if self.sentiment[word] == 'neg':
              score -= 1
          elif self.sentiment[word] == 'pos':
              score += 1
      return score
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

    def binarize(self):
      """Modifies the ratings matrix to make all of the ratings binary"""
      # Idea: +1 if the rating is > 2.5, -1 if it is <= 2.5, and 0 if it is not rated - DV
      rows = self.ratings.shape[0]
      cols = self.ratings.shape[1]
      for i in range(rows):
          for j in range(cols):
              if self.ratings[i][j] >= 0.5 and self.ratings[i][j] <= 2.5:
                  self.ratings[i][j] = -1
              elif self.ratings[i][j] > 2.5:
                  self.ratings[i][j] = 1
      return self.ratings


    def distance(self, u, v):
      """Calculates a given distance function between vectors u and v"""
      # TODO: Implement the distance function between vectors u and v]
      # Note: you can also think of this as computing a similarity measure
      #Idea: cosine similarity? -DV
      pass


    def recommend(self, u):
      """Generates a list of movies based on the input vector u using
      collaborative filtering"""
      # TODO: Implement a recommendation function that takes a user vector u
      # and outputs a list of movies recommended by the chatbot

      pass


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
