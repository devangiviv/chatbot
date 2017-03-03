# chatbot
Chatbot project for CS 124!
Welcome to our Hillary Clinton-themed chatbot!

Our chatbot implements a variety of features specified in both the creative and starter bot modes. We have listed salient features of our chatbot below. Important notes: The chatbot requires users to go through one cycle of movie recommendations (i.e. user describes at least 5 movie opinions to the bot.) Afterwards, the user can choose to simply chat with the bot or say ‘back to movies’ at any point to return back to the movie recommendation task. For additional movies above the requirement of 5 movies, the bot will update its recommendations with every additional movie. After going through a cycle of the movie recommendation, users might also unlock a special Easter Egg feature! 

Here are some important details about our implementations - many of the details go beyond the minimum requirements so we’ve spent some time describing them in depth. :) Thanks for grading our chatbot!

1. Our chatbot is always run in Creative mode.

2. We implement the Creative feature: “Identifying movies without quotation marks or perfect capitalization”:
 We do rely on the first word of the title being capitalized (allowed by the rubric). Thus we can identify cases such as “Harry potter and the sorcerer’s stone.”
We can also handle when the user drops an article that is actually in the title or if the user adds an extra article.
 Moreover, we can also identify years when entered alongside the title.
Sentiment words in the movie title do not trip up the bot as they are spliced out and regarded as separate from words being used to actually extract sentiment.
We gracefully handle the case when multiple titles are inputting in an input by selecting the one of maximum length.
3. We implement the Creative feature: “Disambiguating movie titles for series and year ambiguities.”
ON DISAMBIGUATING SERIES:
For this feature, we expect that the “key words” for a desired title (e.g. in the case of Harry Potter and the Sorcerer’s Stone this would be “Harry Potter”) have their first letters capitalized. We would accept the sentence “Harry Potter is cool” but not “Harry potter is cool.”
Additionally, only the key words may have their first letters capitalized. So, “Honestly, God know how bad Harry Potter is” would capture “Honestly God” as the movie title instead of Harry Potter since words other than the desired key words are capitalized.
 We also allow an optional “I” at the beginning of the sentence. We would accept the sentence “I love Harry Potter” or “i love Harry Potter”
These constraints are necessary  in order to parse user input in a meaningful fashion. They are established with the understanding that multiple features need not be integrated (e.g. no quotes/capitalization in addition to disambiguation) as mentioned in the rubric.
This feature will effectively allow the user to type in a couple key words, e.g. “Star Trek,” and the chatbot will list a set of possible series suggestions. The user can then input a suggestion in whatever format he/she wishes (that is, without regard for quotes/capitalization -- just the first letter of the title would need to be in caps), and get a recommendation.
ON DISAMBIGUATING YEARS:
We disambiguate years as well, e.g. Titanic (1997) and Titanic (1953). We offer the user a list of possible year suggestions for a given title if a title has more than one possible year it was made in.
The user must then enter the title again, along with the year, in quotes (i.e. in Starter Bot format) for the title to be recognized and for the user ratings matrix to be appropriately updated. This was again, done with the understanding that multiple features need not be integrated as mentioned in the rubric.
Failures are again handled gracefully

4. We implement the Creative feature: “Fine-grained sentiment extraction:
- The bot knows strong sentiment words like ‘favorite,’ ‘best,’ and ‘hate,’ and also accurately magnifies their sentiments when used alongside common intensifiers. For example, “very very bad” would be sensed as a strong negative sentiment while “really good!!!” would be sensed as a positive sentiment.  In particular, we rely on known sets of strong positive words, strong negative words, and intensifiers to calculate “score boosts,” and also handle negation. Take a look at our calcSentimentScore function to find out more!

5. We implement the Creative feature: “Identifying and responding to emotions”
We are able to identify two sentiments -- “anger” and “joy” -- and respond to these. Multiple common words to express these emotions as well negations and appropriate responses were handled in our implementation.   
After going through one round of movie recommendations, the bot displays an ability to respond to all four of the following: anger, lack of anger, joy, and lack of joy - in true Hillary Clinton fashion.
6. We implement the Creative feature: “Speaking very fluently”
	- Our chatbot uses grounding and a variety of dialogues to maintain an engaging conversation with the user.
	- Dialogue selection is partially randomized to bring greater variety to the conversation.
-  We ensure that the flow of the conversation is not broken and that the same lines are not excessively repeated.
- The bot employs a use of slang, common expressions, and emoticons to make it personable


7. We implement the Creative feature: “Using a non-binarized dataset”
	- Our chatbot transforms the user ratings in a non-binarized fashion by applying mean-centering and using the cosine similarity calculation. We chose not to normalize or use the Pearson metric to get the best results.
	- Our runtime for the recommend function along with use of a non-binarized dataset is significantly under 5 seconds.

8. We implement half of the Creative feature: “Alternate/foreign titles”
	- We extract titles that are in parentheses, that is, additional titles and add them to our title list.  We handle articles for English language titles but not for foreign language titles (which is acceptable for half credit as stated in the rubric). We do not handle accented characters.
	- For example, we would accept the user input “Se7en” and “Harry Potter and the Philosopher’s Stone” and “Badkonake sefid.”

9. We implement our own Creative feature: “Endowing bot with a personality”
	- Our chatbot embodies Hilary Clinton. We include witty remarks that are in line with Clinton’s personality, for instance, “Hmm, give me a second to think of the perfect recommendation for you. In the meantime, did you know I was actually in the movie "Love Actually"? Check it out if you want a break: https://www.youtube.com/watch?v=IAhF8tPqafQ. (Come on, do it!!!)” when recommending movies and “Hmmm, I think you're being a bit unclear, so I'm having a hard time understanding you...You're basically me trying to crack a joke on national television - no one gets it” when responding to neutral sentiments.
- The bot also displays human traits like sarcasm, sassiness, and inspirational tidbits, which are all traits embodied by Hillary Clinton (or at least the popular media depiction of her!)
	- We spent a lot of time researching Clinton-esque speech and crafting dialogues to reflect her personality, and thus, list this as a creative feature.
	- Many of the phrases used in the responses stem from famous Hillary Clinton quotes!

10. We implement our own Creative feature: “Easter egg hunt”: The user can elect to enter an “alternate universe” in which Hilary Clinton is President by typing in the appropriate sentinel value (specified by the bot). Here, the user can type in Days of the Presidency and see what Clinton would have done. The user can exit the alternative universe at whatever time he/she sees fit. We credit these tweets to the account @ifHilaryHad on Twitter.  We thought this would be a fun additional feature to implement that makes our chatbot more engaging!

Although we always run in creative mode, we still satisfy all the starter bot requirements. In particular:

“Identifying movies in quotation marks with correct capitalization”: This feature is covered by our creative feature on identifying movies without proper capitalization/quotation marks.

“Speaking reasonably fluently”: This feature is covered by our creative feature on “Speaking very fluently.” We meet all the baseline requirements -- bot not always saying the same thing, never returning None/null, not printing extraneous output, and sounding naturalistic -- in addition to more requirements that we describe in our “Creative features” implementation for this criterion.

“Failing gracefully”: Our creative bot covers this.   In response to a neutral sentiment in which a movie is mentioned, the bot confirms whether the user likes the movie or not. Also, in response to a movie not in the database, the bot realizes that the movie is not there and reprompts the user for input. Additional checks are implemented as part of our “speaking fluently” and “bot personality (Hillary Clinton bot)” mentioned in our creative features that add to this criterion.

“Extracting sentiment from simple inputs”: Because we conducted fine-grained sentiment extraction in our creative features, all the cases mentioned in the rubric for this are handled in addition to more sophisticated sentiment analysis described in the “Creative Features” section. Some examples of basic features implemented are handling common negation words like not, n’t, never; having a word between the negation word and the verb; Porter Stemming and ensuring stemmed words are in the dictionary; mixed sentiment; and ignoring sentiment words in the movie title.

“Making reasonable movie recommendations”: When inputting a cluster of similar movies, the chatbot gives reasonable recommendations. For instance, if positive opinions are expressed about a cluster of five comedy movies, comedy/romance/drama movies are recommended. Also, recommendations take less than 5 seconds to make.
