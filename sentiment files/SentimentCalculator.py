from __future__ import division
import nltk
from nltk.corpus import stopwords
from nltk import stem
from nltk.stem import WordNetLemmatizer
from collections import Counter

lemma = WordNetLemmatizer()
newstr=''

file = open('Sentiment.txt', 'w+')
with open('AFINN-111.txt', 'r') as document:
    #Weighted word dictionary
    answer = {}
    for line in document:
        line = line.split()
        if not line:
            continue
        newstr = line[1:]
        answer[line[0]] = newstr[0]       
print(answer)

reviews = open("Micromax Canvas Spark 2 4 GB Black.txt").read()

#Reading the text file containing the reviews
review_processed = reviews.lower()
words = ""
for w in review_processed.split(' '):
    if len(w) >=3 and not w in stopwords.words('english'):
        words += w + ' '
# Removing stopwords and converting text to lowercase

s = ''
my_words = words.split(' ')
my_words.remove('')
tag_tuples = nltk.pos_tag(my_words)
for (string, tag) in tag_tuples:
    if tag.startswith('NN'):
        s+= lemma.lemmatize(string)+' '
    elif tag.startswith('VB'):
        s+=lemma.lemmatize(string, 'v')+' '
    elif tag.startswith('JJ'):
        s+=lemma.lemmatize(string, 'a')+' '
    elif tag.startswith('RB'):
        s+=lemma.lemmatize(string, 'r')+' '
    else:
        s+=string+' '

# Lemmatizing each word from the text

# s = s.encode("utf-8")

words_processed = s.split(' ')
word_count=len(words_processed)
print(word_count)

# Reading positive and negative
pos_sent = open("positive-words.txt").read()
positive_words = pos_sent.split('\n')

neg_sent = open("negative-words.txt").read()
negative_words = neg_sent.split('\n')

positive_counter = 0
negative_counter = 0

pos_words = ''
neg_words = ''
pos_weight = 0
neg_weight = 0

# Comparing words with those from the dictionaries to calculate positive and negative scores
for word in words_processed:
    if word in positive_words:
        pos_words += word + ' '
        positive_counter = positive_counter + 1
        print(answer.get(word, 1))
        pos_weight += int(answer.get(word, 1))
    elif word in negative_words:
        neg_words += word + ' '
        neg_weight += int(answer.get(word, -1))*(-1)
        negative_counter=negative_counter+1

total = pos_weight+ neg_weight
t = positive_counter + negative_counter
file.write("Number of sentiment words : %d\n\n" %t)

t1 = Counter(pos_words.split(' ')).most_common(20)
file.write("Most used positive words : \n")
for (word, freq) in t1:
    file.write('%s - %d\n' %(word, freq))

t2 = Counter(neg_words.split(' ')).most_common(20)
file.write("\nMost used negative words : \n")
for (word, freq) in t2:
    file.write('%s - %d\n' %(word, freq))

pos = pos_weight/total*100
file.write("\nPercentage of positive words : %f\n" %pos)

neg = neg_weight/total*100
file.write("Percentage of negative words : %f\n" %neg)

file.write("------------------------------------------------------------------------------------------------------------------\n")
