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
