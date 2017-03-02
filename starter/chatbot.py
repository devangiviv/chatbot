#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PA6, CS124, Stanford, Winter 2016
# v.1.0.2
# Original Python code by Ignacio Cases (@cases)
# Ported to Java by Raghav Gupta (@rgupta93) and Jennifer Lu (@jenylu)
######################################################################
import csv
import math
import re
import numpy as np
import collections

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
      self.is_turbo = True
      self.user_name = ''
      self.sentiment_stemmed = {}
      self.read_data()
      self.num_to_recommend = 5
      self.myTitles = collections.defaultdict(list)
      self.arabic_to_roman = self.a_to_r()
      self.roman_to_arabic = self.r_to_a()
      self.asked_for_name = False
      self.sassy_name_response = """Wow, so you don\'t want to tell me your name...I\'ll just call you Donald. That's what you get HA! \n \n"""
      self.intro_cont = """Let me warn you - although I'm very focused, I can get chatty as well.
      I'll talk to you about everything from Trump to an alternate reality in which I’m President
      (just ask about the "alternate universe"). If you ever want to go back to talking about movie recommendations,
      just let me know by typing "back to movies." And if you ever want to break my heartlike the Electoral College and
      leave me, just type :quit. Here's how this works. Unlike many GOP congresspeople, I don't avoid town halls
      and I want to hear what you have to say.
      So, why don't you start by telling me about a movie you’ve seen and how you felt about it?\n"""
      self.user_movies = [] #eventually use this to refer back to movies mentioned

    #############################################################################
    # 1. WARM UP REPL
    #############################################################################

    def greeting(self):
      """chatbot greeting message"""
      #############################################################################
      # Write a short greeting message                                      #
      #############################################################################

      #greeting_message = 'Hey there - it\'s nice to meet you! My name is Daniel, but you can call me Dan :) What is your name?'
      greeting_message = """Hello, my fellow American. My name is Hillary Rodham Clinton.
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
        # Implement the extraction and transformation in this method, possibly#
        # calling other functions. Although modular code is not graded, it is       #
        # highly recommended                                                        #
        #############################################################################
        response = ''
        """if not self.asked_for_name:
            self.user_name = input.strip()
            if self.user_name == '':
                response += self.sassy_name_response
                self.user_name = 'Donald'
            response += 'Hi there, ' + self.user_name + '!\n\n'
            response += self.intro_cont
            self.asked_for_name = True"""
        movie_prompt = "Tell me about a movie\n"
        movie_title, rest_of_sentence = self.extractTitles(input) #returns a tuple
        self.user_movies.append((movie_title, rest_of_sentence))
        if len(self.user_movies) == 5:
            rec = self.recommend(self.user_movies)
            response += "I recommend you the following movies: \n " + rec + "\n" + movie_prompt


        """
        score, stemmed_input = self.calcSentimentScore(input)
        #response = ' '.join(input.split())
        response = "The score is %d, The stemmed input is %s, The extracted title is %s" % (score, stemmed_input, response1)
        """
        return response

    ########EXTRACT CODE################
    ###TODO: edge cases - Motorcycle diaries, Man with one red shoe, string II, Cutting edge: the mahic of mvie editing
    ###TODO: Handle cases with years in movie title
    ###TODO: extract sentiment words and return string

    #check first element of list because dictionary contains titles as title, genre
    #return a tuple -- first element is list, second element is words without movie for sentiment score
    #THINK ABOUT KEEPING TITLES AS LIST OF LISTS
    #DO DISAMBIGUATION before cycling thru titles
    #return tuple with one index with title and ext with string of sentiments w no title
    #etractTitles should return moviename as it appears in getTitles
    def extractTitles(self, input):
        self.debug == True
        prePrep = ['the', 'a', 'an']
        postPrep = [', the', ', a', ', an']
        lowerInput = input.lower()
        self.getTitles()
        maxTitle = "No title found" #or set to no title found?
        maxLen = 0
        maxSent = ""
        for title in self.myTitles:
          #print("title extract titles")
          #print(title)
          lowerTitle = title.lower()
          #print(title)
          preTitlePrep = []
          postTitlePrep = []
          if len(lowerTitle) > 0:
            preTitlePrep = lowerTitle.split()[0].strip()
            postTitlePrep = (', ' + lowerTitle.split()[-1]).strip()

          (truth1, title1, sent1) = self.checkUserNoPostPrep(postTitlePrep, lowerInput, lowerTitle, title, input)
          #print(truth1, title1, sent)
          if truth1:
            print("in truth 1")
            if len(title1) > maxLen:
              print("len title1 greater than maxLen")
              maxTitle = title1
              maxLen = len(title1)
              maxSent = sent1
              print("in truth 1")
              print(sent1)
          (truth2, title2, sent2) =  self.checkUserFullTitle(lowerInput, lowerTitle, title, input)
          if truth2:
            print("in truth 2")
            if len(title2) > maxLen:
              print("len title2 greater than maxLen")
              maxTitle = title2
              print("max Title, case 2 %s", maxTitle)
              maxLen = len(title2)
              maxSent = sent2
              print("max title")
              print(maxTitle)
              print(sent2)
          (truth3, title3, sent3) = self.checkUserNoPrePrep(preTitlePrep, lowerInput, lowerTitle, title, input)
          if truth3:
            print("in truth 3")
            if len(title3) > maxLen:
              print("len title3 greater than maxLen")
              maxTitle = title3
              maxLen = len(title3)
              print(sent3)
              maxSent = sent3
          (truth4, title4, sent4) = self.checkUserYesPrePrep(preTitlePrep, lowerInput, lowerTitle, title, input)
          if truth4:
            print("in truth 4")
            if len(title4) > maxLen:
              print("len title4 greater than maxLen")
              maxTitle = title4
              maxLen = len(title4)
              print(sent4)
              maxSent = sent4
        return (maxTitle, maxSent)


    def checkUserNoPostPrep(self, postTitlePrep, lowerInput, lowerTitle, title, input):
        i4 = -1
        postPrep = [', the', ', a', ', an']
        num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if postTitlePrep in postPrep:
            i4 = lowerInput.find(lowerTitle[0: (len(lowerTitle) - len(postTitlePrep))].strip())
            iEnd = i4 + (len(lowerTitle) - len(postTitlePrep))
        if i4 >=0 and input[i4].isupper():
            sentimentWords = lowerInput.replace(lowerInput[i4:iEnd], "")
            return (True, title, sentimentWords)
        elif i4 >= 0 and (input[i4] in num):
            sentimentWords = lowerInput.replace(lowerInput[i4:iEnd], "")
            return (True, title, sentimentWords)
        return (False, title, "")

    def checkUserNoPrePrep(self, preTitlePrep, lowerInput, lowerTitle, title, input):
        prePrep = ['the', 'a', 'an']
        i2 = -1
        num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if preTitlePrep in prePrep:
          i2 = lowerInput.find(lowerTitle[len(preTitlePrep):].strip())
          iEnd = i2 + len(lowerTitle[len(preTitlePrep):].strip())
          #for situations where movie title begins with article, but user doesn't provide article
        if i2 >=0 and input[i2].isupper():
          sentimentWords = lowerInput.replace(lowerInput[i2:iEnd],"")
          print(sentimentWords)
          return (True, title, sentimentWords)
        elif i2 >= 0 and (input[i2] in num):
            sentimentWords = lowerInput.replace(lowerInput[i2:iEnd],"")
            return (True, title, sentimentWords)
        return (False, title, "")

    def checkUserYesPrePrep(self, preTitlePrep, lowerInput, lowerTitle, title, input):
    #here need to check for if A beautiful mind, we return beautiful mind, a
        i3 = -1
        prePrep = ['the', 'a', 'an']
        num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        #for situations where user provides article (capitalized) but movie title does not begin with article
        for word in prePrep:
         newTitle = word + " " + lowerTitle
         i3  = lowerInput.find(newTitle)
         iEnd = i3 + len(newTitle)
         if i3 >= 0 and input[i3].isupper():
           sentimentWords = lowerInput.replace(lowerInput[i3:iEnd], "")
           print(sentimentWords)
           return (True, title, sentimentWords)
         elif i3 >= 0 and (input[i3] in num):
            sentimentWords = lowerInput.replace(lowerInput[i3:iEnd], "")
            return (True, title, sentimentWords)
        return (False, title, "")

    def checkUserFullTitle(self, lowerInput, lowerTitle, title, input):

      num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
      i1 = lowerInput.find(lowerTitle)
      iEnd = i1 + len(lowerTitle)
      if i1 >=0 and input[i1].isupper():
        sentimentWords = lowerInput.replace(lowerInput[i1:iEnd], "")
        print(sentimentWords)
        return (True, title, sentimentWords)
      elif i1 >= 0 and (input[i1] in num):
        sentimentWords = lowerInput.replace(lowerInput[i1:iEnd], "")
        return (True, title, sentimentWords)
      return (False, title, "")



    #modify to include list of lists
    #parse out titles in parentheses
    #for user input, will also have to parse out year and recognize.
    def getTitles(self):
        self.debug == True
        prep = ['The', 'A', 'An']
        #[("Legend of 1900, The (a.k.a. The Legend of the Pianist on the Ocean) (Leggenda del pianista sull'oceano) ", '(1998)')]
        pattern = '(.*?)(\([1-3][0-9][0-9][0-9]\))$'
        for title in self.titles:
          moviePat = re.findall(pattern, title[0])
          if len(moviePat) > 0:
            currStr = moviePat[0][0]
          if len(moviePat) >= 1:
            titles = self.parseTitles(moviePat[0][0])
            myYear = moviePat[0][1]
            #for title in titles:
            #  self.myTitles[title] = []
            for title in titles:
              self.myTitles[title.strip()].append(myYear)
          else:
            self.myTitles[currStr.strip()] = []
        #print(self.myTitles[5570])
        #print("TITLE DICT")
        #print(self.myTitles)

    def parseTitles(self, titleList):
        #print("parsing")
        titles = []
        ind = titleList.find('(')
        title = titleList[:ind]
        title.replace("a.k.a.", "")
        titles.append(title)
        #print("titles list")
        #print(titleList)
        titleList = titleList[ind:]
        #print(titleList)

        while titleList.strip() != "" and self.hasParen(titleList):
          #print(titleList)
          #print("inside loop")
          ind1 = titleList.find('(')
          ind2 = titleList.find(')')
          title = titleList[ind1:ind2+1]
          title = title[1:]
          title = title[:-1]
          title = title.strip()
          title = title.replace("a.k.a.", "")
          titles.append(title)
          titleList = titleList[ind2+1:]
        return titles

    def hasParen(self, strin):
        i = strin.find('(')
        i2 = strin.find(')')
        if i == -1 or i2 == -1:
          return False
        return True


    def addPrep(self, input):
        myTitles = self.getTitles()
        prep = ['The', 'A', 'An']
        modInput = ""
        modInputs = []
        for word in prep:
          modInput = word + " " + input
          modInputs.append(modInput)
        for movie in modInputs:
          if movie in myTitles:
            return (True, movie)
        return (False, "Invalid input")


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
        punc = ['.', ',', ';', '!', '?', '/', '@', '#', '*', '&', '$', '-', '+', '\n', '(', ')', '\'', "\""]
        for p in punc:
          input = input.replace(p, '')
        return input

    """If returned score is >=2 or <= 2, it's probably a strong emotion.
       If returned score is >=3 or <= 3, it's definitely a strong emotion."""
    def calcSentimentScore(self, input):
      #TODO: better metrics - emphasis if line contains many !!! or reaaallyyy (more generally)
      score = 0
      intensifiers = ['realli', 'veri', 'truli', 'extrem', 'so', 'soo', 'quite']
      strong_pos = ['love', 'favorite', 'best', 'amazing', 'perfect']
      strong_neg = ['hate', 'worst', 'disgust']
      boost_tot = 1
      boost = 1

      #normalize input
      input = self.remove_punct(input)
      sentence = ''
      split_input = input.split()

      #LOOP through each word
      for i in range(len(split_input)):
        w = split_input[i]
        prev = ''
        if i is not 0:
            prev = split_input[i-1]
        w = w.strip()
        prev = prev.strip()

        #calculate internsifiers and boosts - pre-stemming cases
        if w == 'reeeeeally':
            boost_tot += boost

        #if the word is not in our sentiment dictionary, try using the stemmed version of the word
        if w not in self.sentiment:
          p = pa.PorterStemmer()
          w = p.returnStemmedWord(w)

        sentence += w
        sentence += ' '
        #negation is implemented below
        if w in self.sentiment:
          regex_result = []
          if self.sentiment[w] == 'neg':
              if prev == 'not' or prev[-2:] == 'nt' or prev == 'never':
                  score += 1
              else:
                  if prev == 'pretty': #pretty bad
                      score -= 1
                  #below regex is to turn things like didn't really hate into positive
                  regex = '((?:i.*?(?:nt|not|never)))(?:.*?)(?:' + w + ').*?'
                  regex_result = re.findall(regex, input)
                  if len(regex_result) > 0:
                      score += 1
                  else:
                      score -= 1
          elif self.sentiment[w] == 'pos':
              if prev == 'not' or prev[-2:] == 'nt' or prev == 'never':
                  score -= 1
              else:
                  regex = '((?:i.*?(?:nt|not|never)))(?:.*?)(?:' + w + ').*?'
                  regex_result = re.findall(regex, input)
                  if len(regex_result) > 0:
                       score -= 1
                  else:
                      score += 1
        #w might be in the stemmed lexicon rather than the regular sentiment lexicon
        elif w in self.sentiment_stemmed:
          regex_result = []
          if self.sentiment_stemmed[w] == 'neg':
              if prev == 'not' or prev[-2:] == 'nt' or prev == 'never':
                  score += 1
              else:
                  if prev == 'pretty': #pretty bad
                      score -= 1
                  #below regex is to turn things like didn't really hate into positive
                  regex = '((?:i.*?(?:nt|not|never)))(?:.*?)(?:' + w + ').*?'
                  regex_result = re.findall(regex, input)
                  if len(regex_result) > 0:
                      score += 1
                  else:
                      score -= 1
          elif self.sentiment_stemmed[w] == 'pos':
              if prev == 'not' or prev[-2:] == 'nt' or prev == 'never':
                  score -= 1
              else:
                  regex = '((?:i.*?(?:nt|not|never)))(?:.*?)(?:' + w + ').*?'
                  regex_result = re.findall(regex, input)
                  if len(regex_result) > 0:
                      score -= 1
                  else:
                      score += 1
        #calculate boosts - adds extra weight to intensifiers and strong pos/neg words
        if w in intensifiers:
            boost_tot += boost
        if w in strong_pos:
            boost_tot += boost
        if w in strong_neg:
            boost_tot += boost
      score *= boost_tot
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
      #binarize the matrix
      self.binarize()
      reader = csv.reader(open('data/sentiment.txt', 'rb'))

      self.sentiment = dict(reader)
      #add some missing words to the sentiment lexicon
      self.sentiment['beautiful'] = 'pos'
      self.sentiment['fun'] = 'pos'
      self.sentiment['cool'] = 'pos'
      self.sentiment['enjoi'] = 'pos'

      #create the stemmed sentiment dictionary
      p = pa.PorterStemmer()
      for w in self.sentiment:
          stemmed_w = p.returnStemmedWord(w)
          self.sentiment_stemmed[stemmed_w] = self.sentiment[w]

    def binarize(self):
      """Modifies the ratings matrix to make all of the ratings binary"""
      # Idea: +1 if the rating is > 2.5, -1 if it is <= 2.5, and 0 if it is not rated - DV
      #TODO: Can also try using each movie's average rating as its threshold
      self.debug == True
      threshold = 2.5
      self.ratings[np.where(self.ratings >= threshold)] = -2
      self.ratings[np.where(self.ratings >= 0.5)] = -1
      self.ratings[np.where(self.ratings == -2)] = 1
      #below is old, slower version of binarizing
      """rows = self.ratings.shape[0]
      cols = self.ratings.shape[1]
      for i in range(rows):
          for j in range(cols):
              if self.ratings[i][j] >= 0.5 and self.ratings[i][j] <= threshold:
                  self.ratings[i][j] = -1
              elif self.ratings[i][j] > threshold:
                  self.ratings[i][j] = 1"""

    def distance(self, u, v):
      """Calculates a given distance function between vectors u and v"""
      # Implement the distance function between vectors u and v
      # Note: you can also think of this as computing a similarity measure
      #Idea: cosine similarity? -DV
      dot_product = np.dot(u, v) + 0.0
      norm_product = np.linalg.norm(u) * np.linalg.norm(v)
      return (dot_product / (norm_product + 1e-7))
      """u_norm = 0
      v_norm = 0
      for x in u:
          u_norm += x**2
      for y in v:
          v_norm += y**2
      u_norm = math.sqrt(u_norm)
      v_norm = math.sqrt(v_norm)
      return dot_product / (u_norm * v_norm)
      #if floating point, warnings, replace the above li
      #return dot_product / (u_norm * v_norm + 1e-7)"""

    """Given a list of (valid movie title w/o year, input with movie title removed) tuples,
       returns a list of (valid movie titles w/o year, sentiment ratings)"""
    def get_sentiment_for_movies(self, t):
        result = []
        for movie, rest in t:
            score, stemmed_sentence = self.calcSentimentScore(rest)
            result.append((movie, score))
        return result

    def recommend(self, t):
      self.debug == True
      """Generates a list of movies based on the input vector u using
      collaborative filtering"""
      # Implement a recommendation function that takes a user vector u
      # and outputs a list of movies recommended by the chatbot
      # Assumes that t = [(movie as it appears in getTitles, rest of sentence), (movie as it appears in getTitles, rest of sentence), etc]

      index_of_j = [] #indices of the movies the user has commented on
      titles = self.getTitles()

      u = self.get_sentiment_for_movies(t)
      #i.e. u = [(movie1, rating1), (movie2, rating2) etc]
      for title, rating in u:
          index_of_j.append(titles.index(title))
      #print(u)
      #print(index_of_j)

      ri_list = [] #list of user's calculated rating for movie i
      dont_include = False
      for i in range(len(titles)):
          ri = 0 #user's calculated rating for movie i
          movie_i = self.ratings[i] #get the row in the ratings matrix for movie i
          for j in range(len(index_of_j)):
              if i == j:
                  dont_include = True
              index_of_movie_j = index_of_j[j]
              movie_j = self.ratings[index_of_movie_j]
              s_ij = self.distance(movie_i, movie_j)
              ri += s_ij * u[j][1] #s_ij * r_xj
          if not dont_include:
              ri_list.append(ri)
          dont_include = False

      #returns a string of the movie titles of the k max ranked movies
      k = -1*len(self.user_movies)/2
      ri_list_np = np.array(ri_list)
      ind = np.argpartition(ri_list_np, k)[k:] #indexes of the k max ri values, though not necessarily in order of max ri
      result_string = ''
      for i in ind:
          result_string += titles[i]
          result_string += '\n'
      return result_string

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
