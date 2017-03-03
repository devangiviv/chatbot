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
import PorterStemmer as pa

import warnings
warnings.filterwarnings("ignore")

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
      self.initEmotions()
      self.myTitles = collections.defaultdict(list)
      self.getTitles()
      self.arabic_to_roman = self.a_to_r()
      self.roman_to_arabic = self.r_to_a()
      self.user_movies = [] #eventually use this to refer back to movies mentioned
      self.response = ''
      self.already_disambiguated_inputs = []

      #BOOL VARIABLES FOR DFA
      self.asked_for_name = False
      self.movie_scheme = True #since we haven't recommended a movie yet
      self.just_recommended_1 = False
      self.just_recommended_2 = False
      self.explored_alternate_universe = False
      self.processing_movie_years = False
      self.processing_alternate_universe = False

      #EASTEREGG
      self.easterEgg = {}
      self.easterEgg['Intro'] = self.getEgg0()
      self.easterEgg['10'] = self.getEgg10()
      self.easterEgg['11'] = self.getEgg11()
      self.easterEgg['12'] = self.getEgg12()
      self.easterEgg['13'] = self.getEgg13()
      self.easterEgg['14'] = self.getEgg14()
      self.easterEgg['15'] = self.getEgg15()
      self.easterEgg['16'] = self.getEgg16()
      self.easterEgg['17'] = self.getEgg17()
      self.easterEgg['18'] = self.getEgg18()
      self.easterEgg['19'] = self.getEgg19()
      self.easterEgg['20'] = self.getEgg20()
      self.easterEgg['nah'] = self.getNah()


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
\nIn these troubling days of unconstitutional executive orders and laughable disregard for the
laws and ideals of this country...I want to help you. Yes, you, my fellow American.
It's important to march, to protest, to call your congresspeople, to vote,
and to run for office. But every once in a while, we all need a break.
And nothing beats a good ole movie night with family and friends.
\nSo, that's why I'm here. I've taken a break from my rigorous nap schedule to do this,
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
      goodbye_message = """I've always believed you can learn something from nearly everybody you meet, if you're open to it.
Even in this short conversation we've had, I can tell you will do great things. The nation depends on it.
It has been nice talking to you, and even though my memory will be wiped like my email servers the next time we meet, I'll leave you with this.
Do all the good you can, for all the people you can, in all the ways you can, as long as you can. (Whether you're marching for equality or grading a chatbot.)
\n\nGod bless you, and God bless the United States of America. """

      #############################################################################
      #                             END OF YOUR CODE                              #
      #############################################################################

      return goodbye_message

    #############################################################################
    # 2. Modules 2 and 3: extraction and transformation                         #
    #############################################################################

    def getEgg0(self):
    	response = """\n YESSSS...There is an alternate universe -- wait for it...I promise I'm not crazy
\n-- in which I am president. I can't talk about it in the media, because everyone already thinks everything is fake news.
\nBut since we've started getting to know each other, I'll tell you about it now. So what are you waiting for? Just enter any number from 10 to 20 and I'll tell you what I did in on that day in my administration.
#alternativefacts. \nIf you're too cool for this or get tired then just say "nah" and I'll take a hint."""
    	return response
    def getEgg10(self):
    	response = """\nDAY 10: Charged Trump w/ treason. Sent Chaffetz the "Why are you so obsessed with me?" GIF from Mean Girls. Ate a plate of nachos with RBG.
\nFilled all key positions in my administration. Re-read every Harry Potter book. Sent Bill to 7-Eleven for Sourpatch Kids """
    	return response
    def getEgg11(self):
    	response = """\nDAY 11: Had brunch with Fey & Poehler. Signed an EO that outlaws mansplaining. Tasked Bill with re-organizing my pantsuit closet. None of my Cabinet members have plagiarized. Told Ryan he seems smarter when he's not talking. Sent Bill to pick up Chipotle. """
    	return response
    def getEgg12(self):
    	response = """\nDAY 12: Wrote a speech that made sense. Sent a bunch of #NastyWomen to Trump Tower to prank Donald. Told Bill to fetch me an iced tea. I know who Frederick Douglass is. Gave a PowerPoint presentation to the GOP on hypocrisy. Sent Bill to H&M for statement necklaces."""
    	return response
    def getEgg13(self):
    	response = """\nDAY 13: Signed an EO making Pride a nat'l holiday. Glitter-bombed McConnell (not sry about it). Sent Bill to get me Beats by Dre headphones."""
    	return response
    def getEgg14(self):
    	response = """\nDAY 14: Haven't undone any Dodd-Frank reforms. Prank-called Trump Tower with Huma. Sent Bill to Papyrus for new stationary. Destroyed the last Horcrux (Trump's spray tan bottle). Subscribed Ryan to Teen Vogue Sent Bill to CVS for Lindt truffle chocolates."""
    	return response
    def getEgg15(self):
    	response = """\nDAY 15: Not using tax-payer $ toward my Chappaqua residence. Told Pence he's the worst. Sent Bill to Michael's for craft supplies. Still respect our checks & balances. Called Trump a "so-called citizen" (& then exiled him) Sent Bill to Drybar for hairspray."""
    	return response
    def getEgg16(self):
    	response = """\nDAY 16: Reviewed briefs on immigration reform. Told Pence that he's pathetic. Sent Bill to Safeway for a Super Bowl snack stadium.Co-hosted a #SB51 party with Beyoncé. Toasted to Lady Gaga & the matriarchy. Sent Bill to Buffalo Wild Wings for more grub."""
    	return response
    def getEgg17(self):
    	response = """\nDAY 17: Not making up fake terrorist attacks. Told Ryan/McConnell that they're hypocritical sellouts. Sent Bill out for empanadas. Was invited to address UK Parliament. Told Chaffetz he was a pathetic excuse for a human being. Tasked Bill with knitting me a scarf."""
    	return response
    def getEgg18(self):
    	response = """\nDAY 18: Met with teacher's union leaders. Told Pence to wipe that look off his face. Sent Bill to Peet's for a chai latte. And then sent Bill to Nordstrom's for sensible heels."""
    	return response
    def getEgg19(self):
    	response = """\nDAY 19: Haven't melted down over a clothing store. Told McConnell that he's worthless. Sent Bill to Smoothie King for a peach drink. Still not enriching myself via the presidency. Exiled Sessions to the island on Lost. Sent Bill to Room & Board for home decor."""
    	return response
    def getEgg20(self):
    	response = """\nDAY 20: Still haven't insulted Vets/POWs/Gold Star families. Told Trump that he's a disgrace. Sent Bill to ShopHouse for lunch. My WH isn't falling like a house of cards. Told the GOP that they're a trainwreck. Sent Bill to Au Bon Pain for a croissant."""
    	return response
    def getNah(self):
    	response = """\nAlright fine, I'll stop. But if you ever want more, check out my alternate reality on Twitter @IfHillaryHad. Or just check out the hashtag #BillErrands. :P\nJust let me know if you want to go back to movies - you know what to do! (Hint: type 'back to movies')"""
    	return response

    def sassy_name_response(self):
        return"""Wow, so you don\'t want to tell me your name...I\'ll just call you Donald. That's what you get HA! \n \n"""

    def intro_cont(self):
        return """Let me warn you - although I'm very focused, I can get chatty (and slightlyyy sassy) as well.
I'll talk to you about everything from Trump to an alternate reality in which I'm President
(just ask about the "alternate universe"). If you ever want to go back to talking about movie recommendations,
just let me know by typing 'back to movies.' And if you ever want to break my heartlike the Electoral College and
leave me, just type :quit. Here's how this works. Unlike many GOP congresspeople, I don't avoid town halls
and I want to hear what you have to say.
So, why don't you start by telling me about a movie you've seen and how you felt about it?\n"""

    def give_recommendation_string(self):
        return """\n\nHmm, give me a second to think of the perfect recommendation for you. \nIn the meantime, did you know I was actually in the movie "Love Actually"?
Check it out if you want a break: https://www.youtube.com/watch?v=IAhF8tPqafQ. (Come on, do it!!!)
\nOkay, you've told me about """ + str(len(self.user_movies)) + """ movies, so I'll give you about half as many recommendations.
Think that's too few? DEAL WITH IT LOL. Read my book "Hard Choices." 'Cause that's how we do it in Brooklyn, baby!
         """

    def ask_for_name(self, input):
        self.user_name = input.strip()
        if input.strip() == '' or input == '\n' or not input:
            self.response += self.sassy_name_response()
            self.user_name = 'Donald'
        self.response += 'Hi there, ' + self.user_name + '!\n\n'
        self.response += self.intro_cont()
        self.asked_for_name = True

    """ Still in movie scheme - haven't given a rec"""
    def did_not_understand(self, input):
        #if user is talking about a movie not in database
        if input.strip() == 'back to movies' and self.just_recommended_2:
            self.response += "\nGreat, let\'s get back into it! So, tell me about another movie you've seen and I'll update my recommendations!"
            self.reprompt_for_movie()
            return
        elif input.strip() == 'back to movies':
            self.response += "\nGreat, let\'s get back into it!"
            self.reprompt_for_movie()
            return
        regex = '"(.*?)"'
        unknown_mov = re.findall(regex, input)
        if len(unknown_mov) > 0:
            self.response += "Okay, I have to admit something. Besides politics, I don't get out much and I don't know what movie you're referring to by " + unknown_mov[0] + ". Please tell me about a different one or try again..."
        #if user does not talk about a movie
        else:
            self.response += "Hey, " + self.user_name + ", let's stay on topic here and remember why I'm taking time out of my nap schedule to be here with you...I'd love to chat, but only after we finish one round of movie recommendations."
        self.reprompt_for_movie()

    def reprompt_for_movie_strings(self):
        reprompt_strings = []
        reprompt_strings.append("""\nRemember, I can't recommend you movies unless you tell me about at least 5 you've already watched! Let's get this rolling...(Come on, don't be shy, """ + self.user_name + ")!!")
        reprompt_strings.append("""\nKeep 'em coming! Remember, I want to hear about 4 more movies before recommending one.""")
        reprompt_strings.append("""\nYay, just 3 more movies to go.""")
        reprompt_strings.append("""\nYay, just 2 more movies to go.""")
        reprompt_strings.append("""\nGreat - I just need one more opinion before I make a recommendation!""")
        #reprompt_strings.append("""\nOh, and I can see you like my my movie recommendations ;) Thanks for asking for more of my wit, unlike America </3! """)
        return reprompt_strings

    def reprompt_for_movie(self):
        reprompt_strings = self.reprompt_for_movie_strings()
        if len(self.user_movies) == 0:
            self.response += reprompt_strings[0]
        elif len(self.user_movies) == 1:
            self.response += reprompt_strings[1]
        elif len(self.user_movies) == 2:
            self.response += reprompt_strings[2]
        elif len(self.user_movies) == 3:
            self.response += reprompt_strings[3]
        elif len(self.user_movies) == 4:
            self.response += reprompt_strings[4]
        #elif len(self.user_movies) > 4:
        #    self.response += reprompt_strings[5]
        if len(self.user_movies) <= 4:
            self.response += self.movie_prompt()

    def movie_prompt(self):
        if len(self.user_movies) > 0:
            return """\n\nAlright, tell me about another movie you've seen and how you felt about it!\n"""
        else:
            return """\n\nAlright, tell me about a movie you've seen and how you felt about it!\n"""

    def sentiment_grounding(self, old_score):
        if old_score >= 1:
            return "liked it."
        elif old_score >= 2:
            return "really, really liked it."
        elif old_score <= -1:
            return "didn't like it."
        elif old_score <= -2:
            return "really, really didn't like it."

    def respond_to_movie(self, movie_title, score):
        repeat = False
        for i in range(len(self.user_movies)):
            movie = self.user_movies[i][0]
            old_score = self.user_movies[i][1]
            if movie == movie_title:
                repeat = True
                sent = self.sentiment_grounding(old_score)
                self.response += "Ah, \"" + str(movie_title) + "\" again! I remember you " + sent + " So let me see - do you still feel the same way?\n...\nHmm."
                self.user_movies[i] = (movie, score)

        if not repeat:
            self.user_movies.append((movie_title, score))
        ind = self.getIndex(movie_title)
        genre = self.titles[ind][1]
        genre = genre.replace("|", "/")
        if score >= 2 or score <= -2:
            self.response += " Ooh okay, I can tell you feel quite strongly about this one. "
        if score > 0:
            self.response += " Okay I totally agree - I like " + genre + " movies quite a bit, too!"
        if score < 0:
            self.response += " Oh, I hear ya, " + self.user_name + ", I don't like " + genre + " movies, either."
        rand = randint(0,3)
        if not rand:
            self.response += " (Then again, I'm a politician. Flip-flopping opinions is my job. :P)"

    def process_neutral_score(self, movie_title):
        retort_string = """Hmmm, I think you're being a bit unclear, so I'm having a hard time understanding you...
You're basically me trying to crack a joke on national television - no one gets it. Don't be so neutral...
put some more gusto into it so I can actually tell how you feel about """ + movie_title + "!!"
        self.response += retort_string

    def output_recommendation(self):
        rec = self.recommend(self.user_movies)
        self.response += self.give_recommendation_string()
        self.response += "\nHere are the movies I think you should watch:\n" + rec
        self.movie_scheme = False
        self.just_recommended_1 = True
        self.just_recommended_2 = True
        self.response += "\nSo, do you like this recommendation as much as I like statement pantsuits? #pantsuitnation :) Be honest with me - yes or no?"

    def generalInstructions(self):
        result = """\n \nNow, if you want to go back to movie recommendations, just type 'back to movies'. Otherwise, we can just chat :)"""
        if not self.explored_alternate_universe:
            result += "\nOh and you haven't asked me about the alternate universe where I'm president yet! Just type 'alternate universe' if you're curious..."
        return result

    def process_just_recommended_1(self, input):
        if "yes" in input or "yeah" in input or "ya" in input:
            self.response += "Thank you for trusting me to recommend movies to you. For all the women - especially the young women, who put your faith in me - I want you to know that nothing has made me prouder than to be your movie-recommending champion."
            self.just_recommended_1 = False
            self.response += self.generalInstructions()
        elif "no" in input or "nah" in input:
            self.response += """Well, when I'm knocked down, I get right back up and never listen to anyone who says I can't or shouldn't go on.
The worst thing that can happen in a democracy -- as well as in an individual's life -- is to become cynical about the future and lose hope: that is the end, and we cannot let that happen.
Although these recommendations might not have worked for you today, stay hopeful.
And remember...you can always go watch Kate McKinnon portraying me on Saturday Night Live :) if you're not into movies."""
            self.just_recommended_1 = False
            self.response += self.generalInstructions()
        else:
            self.response += "Hey :( Answer my question! Did you like the recommendation - yes or no?"

    def process_just_recommended_2(self, input):
        if input.strip() == 'back to movies':
            self.movie_scheme = True
        else:
            self.movie_scheme = False
        self.just_recommended_2 = False

    def process_back_to_movies(self):
        self.movie_scheme = True

    def process_movie_series(self, series_list):
        self.response += "Okay, there are a few possible movie titles you could be referring to: "
        for s in series_list:
            self.response += '\n' + s
        self.response += """\nPlease re-enter the specific movie title you're talking about and tell me how you felt about it!"""

    def process_movie_years(self, title, years_list):
        self.processing_movie_years = True
        self.response += "There are a few versions of that movie from the following years: "
        for year in years_list:
            self.response += '\n' + year
        self.response += """\nPlease re-enter the movie title followed by the (year) you're talking about!
Keep in mind, I've handled so many email servers my brain practically is one.
So enter the title in quotes just how I'd find it in a database and tell me how you felt about it! :P"""

    def create_stemmed_list(self, l):
        result = []
        p = pa.PorterStemmer()
        for w in l:
            result.append(p.returnStemmedWord(w))
        return result

    def initEmotions(self):
        self.angry = ['angry', 'rage', 'upset', 'furious', 'irate', 'seething', 'infuriated', 'angry', 'livid', 'murderous', 'steaming', 'abhor', 'abhorrent', 'agitate', 'agony', 'belligerent', 'catastrophe', 'carnage', 'anger', 'angered', 'demonic', 'cursed', 'bloody']
        self.angry_stemmed = self.create_stemmed_list(self.angry)
        self.happy = ['happiness', 'elated', 'overjoyed', 'joyous', 'thrilled', 'joyfully', 'happily', 'happy', 'joyful', 'joy', 'ecstatic', 'ebullient', 'smile', 'grin', 'laugh', 'smiling', 'grinning', 'laughing', 'laughter', 'giggle', 'giggling']
        self.happy_stemmed = self.create_stemmed_list(self.happy)

    def calcEmotionScore(self, input):
        result = ''
        score = 0
        intensifiers = ['realli', 'veri', 'truli', 'extrem', 'so', 'soo', 'lot', 'most']
        boost_tot = 1
        boost = 1
        if '!!' in input:
            boost_tot += boost

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
          if w not in self.angry or self.happy:
            p = pa.PorterStemmer()
            w = p.returnStemmedWord(w)

          sentence += w
          sentence += ' '
          #negation is implemented below
          if w in self.angry or w in self.happy or w in self.angry_stemmed or w in self.happy_stemmed:
            regex_result = []
            if w in self.angry or w in self.angry_stemmed:
                if prev in intensifiers:
                    boost_tot += boost
                if prev == 'not' or prev[-2:] == 'nt' or prev == 'never':
                    score += 1
                if prev == 'pretty': #pretty bad #counterbalances the addition from pretty
                    score -= 1
                #below regex is to turn things like didn't really hate into positive
                regex = '((?:.*?(?:nt|not|never)))(?:.*?)(?:' + w + ').*?'
                regex_result = re.findall(regex, sentence)
                if len(regex_result) > 0:
                    #print("found in regex-----------------------------------------------------")
                    result = 'not angry'
                    return result
                else:
                    score -= 1
            elif w in self.happy or w in self.happy_stemmed:
                if prev in intensifiers:
                    boost_tot += boost
                if prev == 'not' or prev[-2:] == 'nt' or prev == 'never':
                    score -= 1
                regex = '((?:.*?(?:nt|not|never)))(?:.*?)(?:' + w + ').*?'
                regex_result = re.findall(regex, sentence)
                if len(regex_result) > 0:
                    result = 'not happy'
                    return result
                else:
                    score += 1
        #calculate boosts
        score *= boost_tot
        if result is not '':
            return result
        elif score > 0:
            return 'happy'
        elif score < 0:
            return 'angry'
        else:
            return None

    def emotion_score_response(self, e):
        if not e:
            return ''
        if e == 'not happy':
            return """By the way, I realized you're not happy. I know it's sometimes hard to remain optimistic when
everything seems to be crumbling in the world. You don't always get what you want. Believe me, I've been there. But what's
important when you're feeling low, is to remember my best friend Michelle Obama's words "When they go low, we go high,"" and get up,
dust yourself off, and keep fighting."""
        elif e == 'angry':
            return """\n\nBy the way, you seem angry. Look, I get it. I can tell you're upset. BUT think of it this way...
would you rather go through whatever you're going through or stand next to Donald Trump for hours having him yell “WRONG”
at you every five seconds in front of the whole world? Come on, cheer up! The impeachment clock is ticking :P #pantsuitnation"""
        elif e == 'happy':
            return """\n\nBy the way, it's great to hear that you're happy! Just as happy as I should have been on Election Night </3. Sigh."""
        elif e == 'not angry':
            return """\n\nBy the way, it's good to hear that you're not angry.
You know who IS angry all the time? We both know who - good ole Donald. And don’t tell anyone I said this,
but I'm trying to find a way to get him to watch this bad lip reading of the inauguration to make him a tiny
bit more annoyed. Have you seen it? If not, WHAT ARE YOU DOING? Go watch this NOW :)
https://www.youtube.com/watch?v=gneBUA39mnI"""

    def process_emotion(self, input):
        e_score = self.calcEmotionScore(input)
        self.response += self.emotion_score_response(e_score)

    def process_alternate_universe(self):
        self.response += self.easterEgg['Intro']

    def process(self, input):
        """Takes the input string from the REPL and call delegated functions
        that 1) extract the relevant information and 2) transform the information into a response to the user"""
        self.response = ''
        #ASKING FOR NAME
        if not self.asked_for_name:
            self.ask_for_name(input)
            return self.response
        if self.just_recommended_1:
            #self.response += "\nHERE 1------------"
            self.process_just_recommended_1(input)
            return self.response
        if self.just_recommended_2:
            #self.response += "\nHERE 2-----------"
            self.process_just_recommended_2(input)
        if input.strip() == "back to movies":
            self.process_back_to_movies()
        #------------------------NOT MOVIE SCHEME----------------------------
        if not self.movie_scheme:
            self.process_emotion(input)
            #--------ALTERNATE UNIVERSE----------------
            if self.processing_alternate_universe:
                num = input.strip()
                if num == 'nah':
                    self.processing_alternate_universe = False
                if num in self.easterEgg:
                    self.response += self.easterEgg[num]
                else:
                    rand_num = randint(10, 20)
                    self.response += "\nHey, stick to the numbers given :) I have 10 quality accounts of my presidency for ya! For example..."
                    self.response += self.easterEgg[str(rand_num)]
                return self.response
            if input.strip() == 'alternate universe':
                self.explored_alternate_universe = True
                self.processing_alternate_universe = True
                self.process_alternate_universe()
                return self.response
        #--------------------MOVIE SCHEME----------------------------------------
        if self.movie_scheme:
            #self.response += "\nHERE in movie scheme------------"
            movie_series = self.disambiguate(input) #[title1, title2, ...]
            #print(movie_series)
            series_stem = self.processInputForPrefix(input)

            #print("THIS IS THE MOVIE SERIES")
            #print(movie_series)
            #USER ENTERED STAR WARS
            if len(movie_series) > 0 and (series_stem not in self.already_disambiguated_inputs):
                self.already_disambiguated_inputs.append(series_stem)
                self.process_movie_series(movie_series)
                return self.response
            movie_title, rest_of_sentence, mov_years = self.extractTitles(input) #returns a tuple #mov_years = ['(2001)', etc ]
            #NOT A VALID TITLE
            if movie_title == "No title found":
                #self.response += "here in movie title not found"
                self.did_not_understand(input)
                self.processing_movie_years = False
                return self.response
            elif self.processing_movie_years:
                #self.response += "here in pmy"
                regex = '"(.*?)"'
                matches = re.findall(regex, input)
                if len(matches) == 0:
                    self.did_not_understand(input)
                    return self.response
                index = self.getIndexExact(matches[0])
                if index == -1:
                    self.did_not_understand(input)
                    return self.response
                self.processing_movie_years = False
                movie_title = self.titles[index][0]
                score = self.calcSentimentScore(rest_of_sentence)
                #NEUTRAL SCORE
                if score == 0:
                    self.process_neutral_score(movie_title)
                    return self.response
                #NON-NEUTRAL SCORE
                else:
                    self.respond_to_movie(movie_title, score)
                self.reprompt_for_movie()
            elif len(mov_years) > 1:
                self.process_movie_years(movie_title, mov_years)
                return self.response
            #VALID TITLE, HAVE CHOSEN A MOVIE
            else:
                score = self.calcSentimentScore(rest_of_sentence)
                #NEUTRAL SCORE
                if score == 0:
                    self.process_neutral_score(movie_title)
                    return self.response
                #NON-NEUTRAL SCORE
                else:
                    self.respond_to_movie(movie_title, score)
                self.reprompt_for_movie()
            #TIME TO RECOMMEND!
            if len(self.user_movies) >= 5:
                self.output_recommendation()
        if self.response == '':
            self.response += "Well, I guess I'm not quite sure what to say to that."
            self.response += self.generalInstructions()
        return self.response

    ########EXTRACT CODE################
    def isMovie(self, input):
        for title in self.myTitles:
          if input.lower().strip() == title.lower().strip():
              #print("is a movie")
              return True
        return False

    def checkAmbiguitySeries(self, input):
      #self.getTitles()
      possibTit = []
      input = input.lower()
      for title in self.myTitles:
        lowTitle = title.lower().strip()
        if lowTitle.startswith(input.strip()):
          possibTit.append(title)
      return possibTit

    #Call this before extractTitles -- prompt user to re input, and then extract title from that re inputted input.
    def disambiguate(self, input):
      modStr = self.processInputForPrefix(input)
      #print(modStr)
      maxPossibTitSer = self.checkAmbiguitySeries(modStr)
      #print("max seri")
      #print(maxPossibTitSer)
      if len(maxPossibTitSer) == 1:
        return []
      return maxPossibTitSer

    def extractTitles(self, input):
        #self.debug == True
        self.disambiguate(input)
        prePrep = ['the', 'a', 'an']
        postPrep = [', the', ', a', ', an']
        lowerInput = input.lower()
        maxTitle = "No title found" #or set to no title found?
        maxLen = 0
        maxSent = ""
        maxPossibTitSer = []
        maxPossibTitYr = []
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

          #print("at no title found case")
          #modStr = self.processInputForPrefix(input)
          #print(modStr)
          #maxPossibTitSer = self.checkAmbiguitySeries(modStr)
          #maxPossibTitYr = self.myTitles[title]

          #print("max seri")
          #print(maxPossibTitSer)
          (truth1, title1, sent1, userInput1) = self.checkUserNoPostPrep(postTitlePrep, lowerInput, lowerTitle, title, input)
          #print(truth1, title1, sent)
          if truth1:
            #print("in truth 1")
            if len(title1) > maxLen:
              #print("len title1 greater than maxLen")
              maxTitle = title1
              maxLen = len(title1)
              maxSent = sent1
              #maxPossibTitSer = self.checkAmbiguitySeries(userInput1.strip())
              maxPossibTitYr = self.myTitles[maxTitle]
              #print("in truth 1")
              #print(sent1)
          (truth2, title2, sent2, userInput2) =  self.checkUserFullTitle(lowerInput, lowerTitle, title, input)
          if truth2:
            #print("in truth 2")
            #print("This is the max len")
            #print(maxLen)
            #print("This is the max title")
            #print(maxTitle)
            if len(title2) > maxLen:
              #print("This is title 2!")
              #print(title2)
              #print("len title2 greater than maxLen")
              maxTitle = title2
              #print("max Title, case 2 %s", maxTitle)
              maxLen = len(title2)
              maxSent = sent2
              #maxPossibTitSer = self.checkAmbiguitySeries(userInput2.strip())
              maxPossibTitYr = self.myTitles[maxTitle]
              #print("max title")
              #print(maxTitle)
              #print(sent2)
          (truth3, title3, sent3, userInput3) = self.checkUserNoPrePrep(preTitlePrep, lowerInput, lowerTitle, title, input)
          if truth3:
            #print("in truth 3")
            if len(title3) > maxLen:
              #print("len title3 greater than maxLen")
              maxTitle = title3
              maxLen = len(title3)
              #print(sent3)
              maxSent = sent3
              #maxPossibTitSer = self.checkAmbiguitySeries(userInput3.strip())
              maxPossibTitYr = self.myTitles[maxTitle]
          (truth4, title4, sent4, userInput4) = self.checkUserYesPrePrep(preTitlePrep, lowerInput, lowerTitle, title, input)
          if truth4:
            #print("in truth 4")
            if len(title4) > maxLen:
              #print("len title4 greater than maxLen")
              maxTitle = title4
              maxLen = len(title4)
              #print(sent4)
              maxSent = sent4
              #maxPossibTitSer = self.checkAmbiguitySeries(userInput4.strip())
              maxPossibTitYr = self.myTitles[maxTitle]
        #print(self.myTitles)

        return (maxTitle, maxSent, maxPossibTitYr)

    #takes first consecutive sequence of capitalized words as key words
    def processInputForPrefix(self, input):
        #can maybe add numbers?
        caps = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
        caps.append('S')
        caps.append('T')
        caps.append('U')
        caps.append('V')
        caps.append('W')
        caps.append('X')
        caps.append('Y')
        caps.append('Z')

        prefix = "NONE"
        input = self.remove_punct_with_case(input)
        #print("no punc")
        #print(input)
        if len(input.strip()) == 0:
          return prefix
        splitInput = input.split()

        if (len(splitInput[0].strip()) > 0) and (splitInput[0].strip() in ["i", "I"]):
          input = input[1:]
          input = input.strip()
        splitInput = input.split()
        prevInt = -1
        startIndex = 0
        for i in xrange(0, len(splitInput)):
          if (splitInput[i][0] in caps):
            prefix = ""
            prefix += splitInput[i] + " "
            startIndex = i+1
            break
        while startIndex < len(splitInput):
          if (splitInput[startIndex][0] in caps):
            prefix += splitInput[startIndex] + " "
          startIndex += 1
        #print("THIS IS TH PREFIX")
        #print(prefix)
        return prefix

    def checkUserNoPostPrep(self, postTitlePrep, lowerInput, lowerTitle, title, input):
        i4 = -1
        postPrep = [', the', ', a', ', an']
        num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if postTitlePrep in postPrep:
            i4 = lowerInput.find(lowerTitle[0: (len(lowerTitle) - len(postTitlePrep))].strip())
            iEnd = i4 + (len(lowerTitle) - len(postTitlePrep))
        if i4 >=0: #and input[i4].isupper():
            sentimentWords = lowerInput.replace(lowerInput[i4:iEnd], "")
            return (True, title, sentimentWords, lowerInput[i4:iEnd])
        elif i4 >= 0 and (input[i4] in num):
            sentimentWords = lowerInput.replace(lowerInput[i4:iEnd], "")
            return (True, title, sentimentWords, lowerInput[i4:iEnd])
        return (False, title, "", "")

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
          #print(sentimentWords)
          return (True, title, sentimentWords, title)
        elif i2 >= 0 and (input[i2] in num):
            sentimentWords = lowerInput.replace(lowerInput[i2:iEnd],"")
            return (True, title, sentimentWords, title)
        return (False, title, "", "")

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
           #print(sentimentWords)
           return (True, title, sentimentWords, lowerInput[i3:iEnd])
         elif i3 >= 0 and (input[i3] in num):
            sentimentWords = lowerInput.replace(lowerInput[i3:iEnd], "")
            return (True, title, sentimentWords, lowerInput[i3:iEnd])
        return (False, title, "", "")

    def checkUserFullTitle(self, lowerInput, lowerTitle, title, input):

      num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
      #print("lower input lower title")
      #print(lowerInput)
      #print(lowerTitle)
      i1 = lowerInput.find(lowerTitle)
      iEnd = i1 + len(lowerTitle)
      if i1 >=0 and input[i1].isupper():
        #print("Arguments to checkusefultitle")
        #print("in if statment----------------------------")
        #print(lowerInput)
        #print(lowerTitle)
        #print(title)
        #print(input)
        sentimentWords = lowerInput.replace(lowerInput[i1:iEnd], "")
        #print(sentimentWords)
        return (True, title, sentimentWords, lowerInput[i1:iEnd])
      elif i1 >= 0 and (input[i1] in num):
        sentimentWords = lowerInput.replace(lowerInput[i1:iEnd], "")
        return (True, title, sentimentWords, lowerInput[i1:iEnd])
      return (False, title, "", "")



    #modify to include list of lists
    #parse out titles in parentheses
    #for user input, will also have to parse out year and recognize.
    def getTitles(self):
        #self.debug = True
        prep = ['The', 'A', 'An']
        #[("Legend of 1900, The (a.k.a. The Legend of the Pianist on the Ocean) (Leggenda del pianista sull'oceano) ", '(1998)')]
        pattern = '(.*?)(\([1-3][0-9][0-9][0-9]\))$'
        moviePat = ''
        currStr = ''
        #print("HERE__________")
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
        prep = ['The', 'A', 'An']
        modInput = ""
        modInputs = []
        for word in prep:
          modInput = word + " " + input
          modInputs.append(modInput)
        for movie in modInputs:
          if movie in self.myTitles:
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


    def remove_punct_with_case(self, input):
        #input = input.lower()
        punc = ['.', ',', ';', '!', '?', '/', '@', '#', '*', '&', '$', '-', '+', '\n', '(', ')', '\'', "\"", '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for p in punc:
          input = input.replace(p, '')
        return input

    def remove_punct(self, input):
        input = input.lower()
        punc = ['.', ',', ';', ':', '!', '?', '/', '@', '#', '*', '&', '$', '-', '+', '\n', '(', ')', '\'', "\"", '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for p in punc:
          input = input.replace(p, '')
        return input

    """If returned score is >=2 or <= 2, it's probably a strong emotion.
       If returned score is >=3 or <= 3, it's definitely a strong emotion."""
    def calcSentimentScore(self, input):
      score = 0
      intensifiers = ['realli', 'veri', 'truli', 'extrem', 'so', 'soo', 'lot', 'most']
      strong_pos = ['love', 'favorite', 'best', 'amazing', 'perfect']
      strong_neg = ['hate', 'worst', 'disgust']
      boost_tot = 1
      boost = 1
      if '!!' in input:
          boost_tot += boost

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
                  if prev == 'pretty': #pretty bad #counterbalances the addition from pretty
                      score -= 1
                  #below regex is to turn things like didn't really hate into positive
                  regex = '((?:.*?(?:nt|not|never)))(?:.*?)(?:' + w + ').*?'
                  regex_result = re.findall(regex, input)
                  if len(regex_result) > 0:
                      #print("found in regex-----------------------------------------------------")
                      score += 1
                  else:
                      score -= 1
          elif self.sentiment[w] == 'pos':
              if prev == 'not' or prev[-2:] == 'nt' or prev == 'never':
                  score -= 1
              else:
                  regex = '((?:.*?(?:nt|not|never)))(?:.*?)(?:' + w + ').*?'
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
                  regex = '((?:.*?(?:nt|not|never)))(?:.*?)(?:' + w + ').*?'
                  regex_result = re.findall(regex, input)
                  if len(regex_result) > 0:
                      score += 1
                  else:
                      score -= 1
          elif self.sentiment_stemmed[w] == 'pos':
              if prev == 'not' or prev[-2:] == 'nt' or prev == 'never':
                  score -= 1
              else:
                  regex = '((?:.*?(?:nt|not|never)))(?:.*?)(?:' + w + ').*?'
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
      #binarize the matrix - we aren'd doing this
      #self.binarize()
      self.non_binarize()
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

    def non_binarize(self):
        for i in range(self.ratings.shape[0]):
            self.ratings[i][np.where(self.ratings[i]>0)] -= np.mean(self.ratings[i][np.where(self.ratings[i]>0)])

    def binarize(self):
      """Modifies the ratings matrix to make all of the ratings binary. This function is unused."""
      # Idea: +1 if the rating is > 2.5, -1 if it is <= 2.5, and 0 if it is not rated - DV
      #TODO: Can also try using each movie's average rating as its threshold
      #self.debug == True
      threshold = 2.5
      self.ratings[np.where(self.ratings >= threshold)] = -2
      self.ratings[np.where(self.ratings >= 0.5)] = -1
      self.ratings[np.where(self.ratings == -2)] = 1

    def distance(self, u, v):
      """Calculates a given distance function between vectors u and v"""
      # Implement the distance function between vectors u and v
      # Note: you can also think of this as computing a similarity measure
      #Idea: cosine similarity? -DV
      dot_product = np.dot(u, v) + 0.0
      norm_product = np.linalg.norm(u) * np.linalg.norm(v)
      return (dot_product / (norm_product + 1e-7))

    """Returns the index in the original 9125 dimensions for a given title extracted from the user's input"""
    def getIndex(self, title):
        for i in range(len(self.titles)):
            if title in self.titles[i][0]:
                return i

    def getIndexExact(self, title_exact):
        for i in range(len(self.titles)):
            if title_exact == self.titles[i][0]:
                return i
        return -1

    def recommend(self, t):
      #self.debug == True
      """Generates a list of movies based on the input vector u using
      collaborative filtering"""
      # Implement a recommendation function that takes a user vector u
      # and outputs a list of movies recommended by the chatbot
      # Assumes that t = [(movie as it appears in getTitles, rest of sentence), (movie as it appears in getTitles, rest of sentence), etc]

      index_of_j = [] #indices of the movies the user has commented on
      u = self.user_movies
      #i.e. u = [(movie1, rating1), (movie2, rating2) etc]
      for title, rating in u:
          index_of_j.append(self.getIndex(title))
      #print(index_of_j)

      ri_list = [] #list of user's calculated rating for movie i
      dont_include = False
      for i in range(len(self.titles)):
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
          result_string += self.titles[i][0]
          result_string += '\n'
      return result_string

    #############################################################################
    # 4. Debug info                                                             #
    #############################################################################

    def debug(self, input):
      """Returns debug information as a string for the input string from the REPL"""
      # Pass the debug information that you may think is important for your
      # evaluators
      #debug_info = self.user_movies
      #debug_info, stemmed_input = self.calcEmotionScore(input)
      #if not debug_info:
      #  debug_info = 'neither anger nor happiness'

      #return debug_info
      pass


    #############################################################################
    # 5. Write a description for your chatbot here!                             #
    #############################################################################
    def intro(self):
      return """
      *****Please check out the README to find out all the details about our implementation!*****
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
