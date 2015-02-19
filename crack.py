from misc import *
import crypt

#takes in a filename and a regular expression regexp
#and returns an array containing the words of the file
#that matches the regular expression
def load_words(filename,regexp):
  with open(filename,'r') as f:                 #opens file
    wordList = []
    for line in f:                            
      x = re.match(regexp,line)                #splits each line of file according
      if x:                                    #to regular expression
       word = line.strip()                     #and adds it to list wordList
       wordList+=[word]
  f.closed
  return wordList

#takes in a string str and returns a list with the original 
#string and the reversal of the string 
def transform_reverse(str):
   rev_str = ''                                  #instantiate reverse string to empty string
   for i in range((len(str)-1),-1,-1):           #traverse string starting from last character
     rev_str+=str[i]                             #and adds character to reverse string
   return [str,rev_str] 

#takes in a string str and returns a list 
#of all possible ways to capitalize the string
def transform_capitalize(str):
  def helper(x,l,str1):               #helper recursive function           
    if (not str1 in l):               #doesn't add the instance of str that is already on the list
      l.append(str1)                  #to account for '-' and characters
    for i in range(x,len(str1)):                              #recursively capitalizes the elements of the string
      mod_str = str1[:i] + str1[i].upper() + str[i+1:]
      helper(i+1,l,mod_str)
    return l
  return helper(0,[],str.lower())

#takes in a string str and returns a list of all possible ways to replace letters with similar
#looking digits according to the dictionary
def transform_digits(str):
   d = {'O':['0'],'Z':['2'],'A':['4'],'B':['6','8'],'I':['1'],'L':['1'],'E':['3'],'S':['5'],'T':['7'],'G':['9'],'Q':['9']}
   def helper(x,l,str1):                                 
     l.append(str1)
     for i in range(x,len(str1)):                           #for every element of the string
       if (str1[i].upper() in d):                           #checks to see if it is a key in the dictionary
          valList = d[str1[i].upper()]                      #and gets the list of values
          for j in range(0,len(valList)):                   #recursively replaces the letters with the possible digits
            mod_str = str1[:i] + valList[j] + str1[i+1:]
            helper(i+1,l,mod_str)
     return l
   return helper(0,[],str)

#takes in a plain-text password plain and an encrypted 
#password enc and returns True if plain encrypts to enc
#else returns False
def check_pass(plain,enc):
   encrypted = crypt.crypt(plain,enc[0:2])        #calls crypt.crypt with the plain password and first two elements of enc
   if (encrypted == enc): return True
   else: return False

#takes a string filename and returns a list of dictionaries with 
#different fields, each mapping to corresponding field of the file
def load_passwd(filename):
   with open(filename, 'r') as f:
      dictList = []
      for line in f:                              #for each line in the file, 
        fieldList = re.split(':',line)            #splits it according to fields
        d = {}                                    #and adds them to the corresponding key
        if (len(fieldList) == 7):                 #in the dictionary
          d['account'] = fieldList[0]
          d['shell'] = fieldList[6].strip()
          d['UID'] = int(fieldList[2])
          d['GID'] = int(fieldList[3])
          d['GECOS'] = fieldList[4]
          d['directory'] = fieldList[5]
          d['password'] = fieldList[1] 
          dictList.append(d)
   f.closed
   return dictList
    
#takes three strings corresponding to a password file, list of words
#and output file, and cracks passwords. As they are discovered, 
#the passwords and corresponding usernames are written out to file
def crack_pass_file(fn_pass,words,out):
  with open(out, 'w') as f:                              #open output file.
    passList = load_passwd(fn_pass)                      #gets list of dictionary of passwords.
    wordList = load_words(words,'\S+')                   #gets the word list.
    alreadyCracked = []                                  #list to keep track of number of cracked passwords.
    for word in wordList:                                #first will crack passwords without transformed words
      if (len(alreadyCracked) == len(passList)):         #if all passwords have been cracked returns
        return
      else:
        p = 0                                           
        isCracked = False                                      
        while ((not isCracked) and (p < len(passList))):       
          if (p in alreadyCracked): p+=1                       #if that password has already been cracked, then go on to next one
          else:
             d = passList[p]                                   #else use check_pass to check if the password is the encryption of word
             isCracked = check_pass(word,d['password'])
             if isCracked:                                     #if it is then it writes output to output file
                f.write(d['account'] + '=' + word + '\n')
                f.flush()
                alreadyCracked.append(p)                       #appends number of password that has been cracked to alreadyCracked
             p+=1
    for word in wordList:                                      #now runs throught the remaining passwords that haven't been cracked
      if (len(alreadyCracked) == len(passList)):               #using the transformed versions of the words
        return
      else:
        transformed_wordList = transform_reverse(word) + transform_capitalize(word)[1:] + transform_digits(word)[1:]  #list of all transformations of words.   
        for trans_word in transformed_wordList:
          p = 0
          isCracked = False
          while ((not isCracked) and (p < len(passList))):
           if (p in alreadyCracked): p+=1
           else:
               d = passList[p]
               isCracked = check_pass(trans_word,d['password'])
               if isCracked:
                    f.write(d['account'] + '=' + trans_word + '\n')
                    f.flush()
                    alreadyCracked.append(p)
               p+=1
  f.closed
  return 
       
