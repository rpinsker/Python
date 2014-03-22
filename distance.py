#!/usr/bin/env python3.3                                                                                                                      
#NOTE: THIS IS WRITTEN IN PYTHON 3.3
import sys
import re
from math import sqrt

freq = {}      # a map from words to number of occurrences for file2                                                                          
freq2 = {}     # a map from words to number of occurrences for file2                                                                          
# process input for file 1                                                                                                                    
for line in open(sys.argv[1]):
# for each word add 1 to the frequency count                                                                                                  
        for word in re.split("[^a-z]+",line.lower()):
            freq.setdefault(word,0)
            freq[word] += 1
del freq[""]
sumSquares = 0
# iterate over freq to get the sum of the squares of the frequencies in file1                                                                 
for word in freq:
    sumSquares = sumSquares + (freq[word] * freq[word])
# iterate over freq to normalize each frequency (divide frequency by square root of sum of squares of other frequencies)                      
for word in freq:
    freq[word] = freq[word]/(sqrt(sumSquares))
# process input for file 2                                                                                                                    
for line in open(sys.argv[2]):
# for each word add 1 to the frequency count                                                                                                  
        for word in re.split("[^a-z]+",line.lower()):
            freq2.setdefault(word,0)
            freq2[word] += 1
del freq2[""]
sumSquares2 = 0
# iterate over freq2 to get the sum of the squares of the frequencies in file2                                                                
for word in freq2:
    sumSquares2 = sumSquares2 + (freq2[word] * freq2[word])
# iterate over freq2 to normalize each frequency (divide frequency by square root of sum of squares of other frequencies)                     
for word in freq2:
    freq2[word] = freq2[word]/(sqrt(sumSquares2))
# compute distance                                                                                                                            
distances = {}
# get normalized frequencies from file1                                                                                                       
for word in freq:
    distances[word] = freq[word]
# get normalized frequencies from file2, subtracting the value from the normalized frequency of that word in file1 (making that 0 if the word was not present in file1)                                                                                                                    
for word in freq2:
    distances.setdefault(word,0)
    distances[word] = distances[word] - freq2[word]
# square all of the distances                                                                                                                 
for d in distances:
    distances[d] = distances[d] * distances[d]
sumSquaresDists = 0
# get the sum of the squares of the distances                                                                                                 
for d in distances:
    sumSquaresDists = sumSquaresDists + distances[d]
# print out the squart of the sum of the squares of the distances (overall distances between file1 and file2)                                 
print(sqrt(sumSquaresDists))
