#PA 4

import re

"Miscellaneous functions to practice Python"

class Failure(Exception):
    """Failure exception"""
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)

# Problem 1

# data type functions

#returns the element of the list l closest in value
#to v. In case of a tie, the first such element is returned. 
#If l is empty None is returned
def closest_to(l,v):
   if l == []:
     return None
   else:
     difference = abs(v-(l[0]))        #takes absolute value of difference of element and v
     tempClosest = l[0]                #and sets it to the temporary closest
     for x in l[1:]:
       if abs(v-x) < difference :      #gets the difference between value and each element
         tempClosest = x               #and updates temporary closest if needed
         difference = abs(v-x)
   return tempClosest

#takes in a list of keys and a list of values and returns
#a dictionary pairing keys to corresponding values
def make_dict(keys,values):
  d={}
  for i in range(0,len(keys)):
    d[keys[i]] = values[i]
  return d
   
# file IO functions
#takes a string fn (file name) and returns a dictionary
#mapping words to the number of times they occur in the file fn
def word_count(fn):
  with open(fn, 'r') as f:                  #opens file
    d = {}
    for line in f:
      wordList = re.split('\W+',line)      #splits each line in file
      for word in wordList:                #if the word is already in the dictionary
        if word!=(''):                     #then it just updates the counter, 
	  wordL = word.lower()             #else it adds it to the dictionary
          if wordL in d: d[wordL]+=1
          else: d[wordL] = 1
  f.closed
  return d
