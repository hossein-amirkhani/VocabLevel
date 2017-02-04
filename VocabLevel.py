from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import os
import codecs
from collections import Counter
import operator
import enchant
from nltk.metrics import edit_distance
import csv

class SpellCorrection(object):
    def __init__(self, dict_name='en-US', max_dist=2):
        self.spell_dict = enchant.Dict(dict_name)
        self.max_dist = max_dist
    def replace(self, word): # If the edit distance is greater than max_dist, it returns None
        if self.spell_dict.check(word):
            return word
        suggestions = self.spell_dict.suggest(word)
        if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
            return suggestions[0]
        else:
            return None
        
### To Do: we can consider words with different POS as different words
### To Do: we can check whether the user really knows the answer or not (for example by multiple choices questions)
        
if os.path.exists('word_list.csv'):
    with open('word_list.csv', 'r') as f:
        csv_in = csv.reader(f)
        sorted_words = [row for row in csv_in]
else:
    # extract words
    # a. Remove proper nouns
    # b. Keep only alphabetic words
    # c. Correct misspellings
    # d. Lemmatize words
    # e. Lower-case words
    words = []
    for subdir, _, files in os.walk('Subtitles/'):
        for file in files:
            f = codecs.open(os.path.join(subdir, file), 'r', 'latin-1')
            tagged_sent = pos_tag(word_tokenize(f.read()))
            words.extend([word for word,pos in tagged_sent if pos != 'NNP']) 
    
    replacer = SpellCorrection()
    lemmatizer = WordNetLemmatizer()
    filtered = []
    for w in words:
        if str.isalpha(w):
            modif_word = replacer.replace(w)
            if modif_word and str.isalpha(modif_word):
                filtered.append(lemmatizer.lemmatize(modif_word.lower()))

    # count words and sort according to their frequencies
    sorted_words = sorted(Counter(filtered).items(), key=operator.itemgetter(1))

    # save the word lists
    with open('word_list.csv','w') as f:
        csv_out = csv.writer(f)
        for row in sorted_words:
            csv_out.writerow(row)
            
# interact with user to find his/her vocabulary level
start = 0
end = len(sorted_words)-1
while start <= end:
    pos = int((start+end)/2)
    print('Do you know the meaning of "%s" (y,n)?' % sorted_words[pos][0])
    if input()=='y':
        end = pos - 1
        pos -= 1
    else:
        start = pos + 1
# pos: the position where the user does not knows its meaning and the meaning of the words after that

total = len(sorted_words)
knows = total-(pos+1)
print("************************RESULTS***********************")
print("You approximately knows %d words out of %d (%%%.1f)" %(knows,total,knows*100/total))
print("******************************************************")

# We can give the separate lists of words that the user knows and does not know




