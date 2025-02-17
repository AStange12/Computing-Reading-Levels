#============================================================================
# Author:	Aaron Stange

# Summary:	This script calculates the Flesch Reading Ease and Flesch-Kincaid 
# Grade Level scores for a given text file. It processes the text to remove 
# punctuation, count syllables, words, and sentences, and then computes the 
# readability scores. The results are written to a CSV file along with the 
# top N most frequent words in the text.

# INPUT: Asks the user to enter a filename. The file should contain the text
# they want analyzed.

# OUTPUT: Generates a CSV file named "report.csv" containing the following
# information: total syllables, words, sentences, Flesch Reading Ease score,
# Flesch-Kincaid Grade Level score, and the top N most frequent words in the text.

# Date Last Modified:
#	 (aws) 01/29/2025 -- converting python code to a jupiter notebook


# My EXTENDED definition of READING LEVEL: Reading level is a measure of how
# difficult a text is to read. It is calculated based on the number of syllables,
# words, and sentences in the text. The Flesch Reading Ease score indicates how
# easy a text is to read, with higher scores indicating easier readability. The
# Flesch-Kincaid Grade Level score estimates the grade level required to understand
# the text, with lower scores indicating easier readability.

# Flesh Reading Ease score formula: 
# 206.835 - (1.015 * (total words / total sentences)) - (84.6 * (total syllables / total words))

# Flesh-Kincaid Grade Level score formula:
# 0.39 * (total words / total sentences) + 11.8 * (total syllables / total words) - 15.59

#============================================================================

import string
import os



# CONSTANTS
SENTENCE_MARKER = "XXX"

TOP_N_WORDS = 10

    
#----------------------\
# remove_punctuation()  \
#-----------------------------------------------------------
# This function accepts one string (s) and removes all
# the punctuation symbols found in the string and returns
# the new string.

# IN:  string (a passage/text)

# RETURNS: that same string but with all punctuation gone
#-----------------------------------------------------------
def remove_punctuation(s: str) -> str:
	"""
	Removes punctuation from input string then returns new string.

	Parameters:
		s (str): The input string from which punctuation will be removed.

	Returns:
		str: A new string with all punctuation removed.
	"""
	s_without_punct = ""
	for letter in s:
		if letter not in string.punctuation:
			s_without_punct += letter
	    
	return s_without_punct

# end remove_punctuation()



#-----------\
# getData()  \
#-----------------------------------------------------------
# Asks user to enter a filename, if the file doesn't exist
# it sends an error msg. If it does exist it strips all the
# blank spaces from the end of each line and turns the whole
# thing to lower case, then marks the end of each sentence
# with the delimiter XXX replacing the punctuation at the
# end of each sentence. Finally it compiles each line into
# a single string.

# IN:  None 

# RETURNS: string (file as one lower case string with no 
# punctuation or extra space)
#-----------------------------------------------------------
def getData() -> str:
	"""
	Prompts the user to enter a filename, reads the content of the file, processes it, and returns the content as a single string.

	The function performs the following steps:
	1. Prompts the user to enter a filename.
	2. Checks if the file exists. If not, prints an error message and prompts the user to try another filename.
	3. If the file exists, opens the file and reads its content line by line.
	4. Converts each line to lowercase and handles some common abbreviations.
	5. Adds a delimiter for the end of sentences by replacing periods, question marks, and exclamation marks with a specified marker.
	6. Concatenates all lines into a single string and returns it.

	Parameters:
		None

	Returns:
		str: The processed content of the text as a single string.
	"""
	
	theFileName = input("\nEnter filename: ")
	while not os.path.exists(theFileName):
		print("\nSORRY, the file",theFileName, "does not exist.")
		theFileName = input("Try another filename: ")
		

	INPUT = open(theFileName, 'r')

	fileAsOneString = ""
	for nextLine in INPUT:
		nextLine = nextLine.rstrip()
		nextLine = nextLine.lower()
		
		# handle some abbreviations - edited uncapatalised abbreviations to lowercase as we already used .lower()
		nextLine = nextLine.replace(r"mr.", "mr")
		nextLine = nextLine.replace(r"mrs.", "mrs")
		nextLine = nextLine.replace(r"ms.", "ms")
		nextLine = nextLine.replace(r"dr.", "dr")
		nextLine = nextLine.replace(r"st.", "st")
		nextLine = nextLine.replace(r"prof.", "prof")
		
		# should we do this now? - No because we want to mark the end of every sentence with a delimiter
		# remove_punctuation(nextLine)
		
		MARK = " " + SENTENCE_MARKER + " "
		# add delimiter for end of the sentences
		nextLine = nextLine.replace(".", MARK)
		nextLine = nextLine.replace("?", MARK)
		nextLine = nextLine.replace("!", MARK)
		
		
		fileAsOneString = fileAsOneString + nextLine
	# end for
	
	INPUT.close()
	
	return fileAsOneString
	
# end getData()


#--------------------\
# syllablesPerWord()  \
#-----------------------------------------------------------
# This function accepts one string (word) and calculates the
# number of syllables in the word based on the number of vowels
# following these rules:
# (1) Counts all vowels ('a', 'e', 'i', 'o', 'u', and sometimes 'y').
# (2) Subtracts one for a silent 'e' at the end, unless the word 
# is a special case.
# (3) Subtracts one for every diphthong.

# IN: string (a single word)

# RETURNS: integer (number of syllables in the word)
#-----------------------------------------------------------
def syllablesPerWord(word: str) -> int:
	"""
	Calculate the number of syllables in a given word.

	The function follows these steps:
	1. Count the number of vowels in the word.
	2. Subtract the silent 'e' at the end of a word, except for special cases.
	3. Subtract 1 vowel from every diphthong. A diphthong is when two vowels make only 1 sound.

	Parameters:
		word (str): The word for which to count the syllables.

	Returns:
		int: The number of syllables in the word. The function ensures that there is at least one syllable in the word.
	"""
	#(1) Count the number of vowels (‘a’, ‘e’, ‘i’, ‘o’, ‘u’, and sometimes ‘y’) in the word.
	#(2) Subtract any silent vowels (like the silent ‘e’ at the end of a word).
	#(3) Subtract 1 vowel from every diphthong. 
	# 	 A diphthong is when two vowels make only 1 sound (oi, oy, ou, ow, au, aw, oo, ie, ea, ee, ai).
	
	diphtohongList = ["oi", "oy", "ou", "ow", "ai", "au", "ay", "aw", "oo", "ie", "ea", "ee"]
	vowelList = ["a", "e", "i", "o", "u", "y"]
	
	word = word.lower()
	
	# (1) count vowels in the word
	wordVowels = 0
	for nextVowel in vowelList:
		wordVowels += word.count(nextVowel)
	# end each vowel
	print("(1) total vowels in", word, ":", wordVowels)

	
	# (2) subtract a vowel for a silent 'e' at the end of a word (what about special cases?)
	specialCases = ["recipe", "apostrophe", "catastrophe", "acne", "epitome", "karate", "sesame", "posse", "vigilante", "cliche", "fiance", "resume", "middle", "the"]
	if word.endswith("e") and word not in specialCases:
		if wordVowels != 0:
			wordVowels -= 1

	print("(2) after silent e check", word, ":", wordVowels)

	# (3) subtract 1 for every diphthong
	for diphthong in diphtohongList:
		wordVowels -= word.count(diphthong)

	print("(3) after removing diphthongs: ", word, ":", wordVowels)
	
	# be careful, there must be at least one syllable, right?
	if (wordVowels == 0):
		return 1
	else:
		return (wordVowels)
		
# end syllablesPerWord()


#-------------------------\
# getNumberOfTotalWords()  \
#----------------------------------------------------------------
# Accepts one string (s), which contains the entire contents of an 
# input as returned from getData() and returns the number of words
# in the file.

# IN: string (contents of a file)

# RETURNS: integer (total number of words in the string)
#----------------------------------------------------------------
def getNumberOfTotalWords(s: str) -> int:
	"""
	Calculate the total number of words in a given string.

	This function replaces sentence markers with spaces and then splits the string
	into a list of words, returning the length of this list as the total word count.

	Parameters:
		s (str): string which contains the entire contents of an input file.

	Returns:
		int: The total number of words in the input string.
	"""
	withOutDelimiters = s.replace(SENTENCE_MARKER, " ")
	wordList = withOutDelimiters.split()
	return len(wordList)

# end getNumberOfTotalWords()


#-----------------------------\
# getNumberOfTotalSentences()  \
#----------------------------------------------------------------
# Accepts one string (s), which contains the entire contents of an 
# input as returned from getData() and returns the number of
# sentences in the file based on the number of sentence markers.

# IN: string (contents of a file)

# RETURNS: integer (total number of sentences in the string)
#----------------------------------------------------------------
def getNumberOfTotalSentences(s: str) -> int:
	"""
	Calculate the number of sentences in a given string.

	This function counts the occurrences number of the SENTENCE_MARKER
	in the input string `s` to determine the total number of sentences.

	Parameters:
		s (str): string which contains the entire contents of an input file.

	Returns:
		int: The total number of sentences in the input string.
	"""
	numSent = s.count(SENTENCE_MARKER)

	return numSent

# end getNumberOfTotalSentences()


#-----------------------------\
# getNumberOfTotalSyllables()  \
#----------------------------------------------------------------
# Accepts one string (s), which contains the entire contents of an 
# input as returned from getData(). It calculates and returns the
# total number of syllables in the string by splitting the text into
# individual words and uses the syllablesPerWord() to count syllables 
# for each.

# IN: string (contents of a file)

# RETURNS: integer (total number of syllables in the string)
#----------------------------------------------------------------
def getNumberOfTotalSyllables(s: str) -> int:
	"""
	Calculate the total number of syllables in a given string.

	This function processes a string by first replacing sentence markers with spaces,
	then splitting the string into individual words. It then counts the syllables in
	each word and returns the total count.

	Parameters:
		s (str): string which contains the entire contents of an input file.

	Returns:
		int: The total number of syllables in the input string.
	"""
	# Initializes count
	totalSyllables = 0

	withOutDelimiters = s.replace(SENTENCE_MARKER, " ")

	# Splits string into words and creates list
	words = withOutDelimiters.split()

	# Process each word and count syllables
	for word in words:
		# Add the syllable count for this word
		totalSyllables += syllablesPerWord(word)

	return totalSyllables

    
# end getNumberOfTotalSyllables()


#-----------------------------\
# compute_FleschReadingEase()  \
#-----------------------------------------------------------
# Accepts 3 integers, the total syllables, total words, and total 
# sentences from a text file. It then calculates and returns the 
# Flesch Reading Ease score as a float.
# The formula for the score is:
# 206.835 - (1.015 * (total words / total sentences)) 
# 										- (84.6 * (total syllables / total words))

# IN: int (total number of syllables), int (total number of words), int (total number of sentences)

# RETURNS: float (Flesch Reading Ease score)
#-----------------------------------------------------------
def compute_FleschReadingEase(totalSyllables: int, totalWords: int, totalSentences: int) -> float:
	"""
	Computes the Flesch Reading Ease score for a given text.

	The Flesch Reading Ease score is a readability test designed to indicate how difficult a passage
	in English is to understand. The higher the score, the easier it is to understand the text.
	Formula: 206.835 - (1.015 * (total words / total sentences)) - (84.6 * (total syllables / total words))

	Parameters:
		totalSyllables (int): The total number of syllables in the text.
		totalWords (int): The total number of words in the text.
		totalSentences (int): The total number of sentences in the text.

	Returns:
		float: The Flesch Reading Ease score.
					 Returns 0 if any of the input values are 0 to prevent division by zero.
	"""
	# If file had 0 syllables/words/sentences returns 0 to prevent division by 0
	if totalSyllables == 0 or totalWords == 0 or totalSentences == 0:
		return 0
	
	# Use formula to calculate score
	ease = 206.835 - (1.015 * (totalWords / totalSentences)) - (84.6 * (totalSyllables / totalWords))
	
	return ease

# end compute_FleschReadingEase()

	
	
#-----------------------------------\
# compute_FleschKincaidGradeLevel()  \
#-----------------------------------------------------------
# Accepts 3 integers, the total syllables, total words, and total 
# sentences from a text file. It then calculates and returns the 
# Flesch–Kincaid grade level score as a float.
# The formula for the score is:
# (0.39 * (total words / total sentences)) 
# 							+ (11.8 * (total syllables / total words)) - 15.59

# IN: int (total number of syllables), int (total number of words), int (total number of sentences)

# RETURNS: float (Flesch–Kincaid grade level score)
#-----------------------------------------------------------	
def compute_FleschKincaidGradeLevel(totalSyllables: int, totalWords: int, totalSentences: int) -> float:
	"""
	Computes the Flesch-Kincaid Grade Level for a given text.

	The Flesch-Kincaid Grade Level is a readability test designed to indicate 
	what grade level a passage is.
	Formula: 0.39 * (totalWords / totalSentences) + 11.8 * (totalSyllables / totalWords) - 15.59

	Parameters:
		totalSyllables (int): The total number of syllables in the text.
		totalWords (int): The total number of words in the text.
		totalSentences (int): The total number of sentences in the text.

	Returns:
		float: The Flesch-Kincaid Grade Level. 
					 Returns 0 if any of the input values are 0 to prevent division by zero.
	"""
	# If file had 0 syllables/words/sentences returns 0 to prevent division by 0
	if totalSyllables == 0 or totalWords == 0 or totalSentences == 0:
		return 0
	
	# Use formula to calculate score
	level = (0.39 * (totalWords / totalSentences)) + (11.8 * (totalSyllables / totalWords)) - 15.59
		
	return level

# end compute_FleschKincaidGradeLevel()


#---------------------------\
# printReadingLevelReport()  \
#-----------------------------------------------------------	
# Generates a reading level report and writes it to a CSV file.

# IN: int (total number of syllables), int (total number of words), int (total number of sentences),
#  		float (Flesch Reading Ease score), float (Flesch–Kincaid grade level score)

# RETURNS: None
#-----------------------------------------------------------	
def printReadingLevelReport(totalSyllables: int, totalWords: int, totalSentences: int, readingEase: float, readingLevel: float):
	"""
	Generates a reading level report and writes it to a CSV file.

	1. Opens a CSV file named "report.csv" in write mode.
	2. Writes the header row: "Syllables, Words, Sentences, Reading Ease, Reading Level".
	3. Writes a row containing the provided values for total syllables, words, sentences, reading ease, and reading level.
	4. Closes the CSV file.

	Parameters:

		totalSyllables (int): The total number of syllables in the text.
		totalWords (int): The total number of words in the text.
		totalSentences (int): The total number of sentences in the text.
		readingEase (float): The reading ease score of the text.
		readingLevel (float): The reading level score of the text.

	Returns:
		None
	"""
	CSV = open("report.csv", "w")
	
	CSV.write("Syllables, Words, Sentences, Reading Ease, Reading Level\n")
	CSV.write("%d,%d,%d,%6.2f,%6.2f\n" % (totalSyllables, totalWords, totalSentences, readingEase, readingLevel) )
	
	CSV.close()

# end printReadingLevelReport()


	
#------------------\
# printTopNwords()  \
#-----------------------------------------------------------	
# Analyzes a given string to identify the top N most frequent words and writes the results to a CSV file.

# IN: str (string which contains the entire contents of an input file) 
# 	  int (number of top frequent words to be written to the CSV file)

# RETURNS: None
#-----------------------------------------------------------	
def printTopNwords(s: str, N: int): 
	"""
	Analyzes a given string to identify the top N most frequent words and writes the results to a CSV file.
	
	The function performs the following steps:
	1. Removes punctuation from the input string.
	2. Splits the string into individual words.
	3. Counts the occurrences of each word and stores them in a dict.
	4. Sorts the words by their frequency in descending order.
	5. Writes header row to the CSV file: "TOP WORDS HERE".
	6. Writes the top N words and their counts to a CSV file named "report.csv".

	Parameters:
		s (str): string which contains the entire contents of an input file.
		N (int): The number of top frequent words to be written to the CSV file.

	Returns:
		None
	"""

	CSV = open("report.csv", "a")
	
	CSV.write("\n\nTOP WORDS HERE\n")
	
	
	#print("***", s)
	s_sansPunct = remove_punctuation(s)
	#print(s_sansPunct)
	#junk = input("pause...")
	
	WC: dict[str, int] = {}

	listOfWords = s_sansPunct.split()
	#print(listOfWords)
	for nextWord in listOfWords:
		if ( nextWord in WC.keys()):
			WC[nextWord] = WC[nextWord] + 1
		else:
			WC[nextWord] = 1
	# end for each word
	
	# Sort by counts in reverse order
	sorted_WC = dict(sorted(WC.items(), key=lambda x: x[1], reverse=True))		
	print(sorted_WC)
	
	count = 1
	for (nextWord, nextCount) in sorted_WC.items():
		if (str(nextWord) != "XXX" and count <= N):
			line = str(nextCount) + "," + str(nextWord) + "\n"
			CSV.write(line)
			count += 1
		# end if top-N words
		
	# end for each (count,word) pair
	
	
	CSV.close()

# end printTopNwords()



#--------\
# main()  \
#-------------------------------------------
def main():
	
    
	fileAsString = getData()
	#print(fileAsString)
	
	#noPunctString = remove_punctuation(fileAsString)
    
	totalSyllables = getNumberOfTotalSyllables(fileAsString)
	totalWords     = getNumberOfTotalWords(fileAsString)
	totalSentences = getNumberOfTotalSentences(fileAsString)
	
	if (totalWords > 0 and totalSentences > 0):
		
		readingEase = compute_FleschReadingEase( totalSyllables, totalWords, totalSentences)
	
		readingLevel = compute_FleschKincaidGradeLevel( totalSyllables, totalWords, totalSentences)
		
		printReadingLevelReport(totalSyllables, totalWords, totalSentences, readingEase, readingLevel)
	
		printTopNwords(fileAsString, TOP_N_WORDS)
		
		# dump values to the console (just for debugging purposes)
		print ("\ntotal syllables: ", totalSyllables)
		print ("total words:     ", totalWords)
		print ("total sentences: ", totalSentences)
		
		print ("\nReading Ease:    %5.2f" % readingEase)
		print ("Grade Level:    %5.2f" % readingLevel)
		
	else:
		print("ERROR:  Can not compute metrics without words.")
	
	
	

	
# end main()





#-----------\
# START HERE \
#-----------------------------------------------------------	
if (__name__ == '__main__'):
	
	main()
	


#-----------------------------------------------------

