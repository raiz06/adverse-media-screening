import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nltk
import string
from nltk import word_tokenize
from wordcloud import WordCloud
import random
from flask import Flask, make_response,render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pygal
import pickle

global dictionary,score;
def dictionary(corpus):
    #global dictionary,score
    def clean(text):
        text = text.lower()
        return text

    Cleaned_text = clean(corpus)
    text = word_tokenize(Cleaned_text)

    POS_tag = nltk.pos_tag(text)

    from nltk.stem import WordNetLemmatizer

    wordnet_lemmatizer = WordNetLemmatizer()

    adjective_tags = ['JJ','JJR','JJS']

    lemmatized_text = []

    for word in POS_tag:
        if word[1] in adjective_tags:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0],pos="a")))
        else:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0]))) #default POS = noun
            
    POS_tag = nltk.pos_tag(lemmatized_text)

    stopwords = []

    wanted_POS = ['NN','NNS','NNP','NNPS','JJ','JJR','JJS','VBG','FW'] 

    for word in POS_tag:
        if word[1] not in wanted_POS:
            stopwords.append(word[0])

    punctuations = list(str(string.punctuation))

    stopwords = stopwords + punctuations

    stopword_file = open("long_stopwords.txt", "r")
    #Source = https://www.ranks.nl/stopwords

    lots_of_stopwords = []

    for line in stopword_file.readlines():
        lots_of_stopwords.append(str(line.strip()))

    stopwords_plus = []
    stopwords_plus = stopwords + lots_of_stopwords
    stopwords_plus = set(stopwords_plus)
    phrases = []

    phrase = " "
    for word in lemmatized_text:
        
        if word in stopwords_plus:
            if phrase!= " ":
                phrases.append(str(phrase).split())
            phrase = " "
        elif word not in stopwords_plus:
            phrase+=str(word)
            phrase+=" "


    from collections import defaultdict

    frequency = defaultdict(int)
    degree = defaultdict(int)
    word_score = defaultdict(float)

    vocabulary = []

    for phrase in phrases:
        for word in phrase:
            frequency[word]+=1
            degree[word]+=len(phrase)
            if word not in vocabulary:
                vocabulary.append(word)
                
    for word in vocabulary:
        word_score[word] = degree[word]/frequency[word]
        
    import numpy as np

    phrase_scores = []
    keywords = []
    phrase_vocabulary=[]

    for phrase in phrases:
        if phrase not in phrase_vocabulary:
            phrase_score=0
            for word in phrase:
                phrase_score+= word_score[word]
            phrase_scores.append(phrase_score)
            phrase_vocabulary.append(phrase)

    phrase_vocabulary = []
    j=0
    for phrase in phrases:
        
        if phrase not in phrase_vocabulary:
            keyword=''
            for word in phrase:
                keyword += str(word)+" "
            phrase_vocabulary.append(phrase)
            keyword = keyword.strip()
            keywords.append(keyword)
        
            #print( "Score of candidate keyword '"+keywords[j]+"': "+str(phrase_scores[j]))
            
            j+=1
            
    phrase_scores.sort(reverse=True)
    sorted_index = np.flip(np.argsort(phrase_scores),0)
    #print(sorted_index)
    keywords_num = 5
    #sorted_score= phrase_scores.sort(reverse=True) 
    print ("Keywords:\n")
    #global dictionary,score
    dictionary=[]
    score=[]
    for i in range(0,keywords_num):
        scores = str(phrase_scores[i])
        top_ten = str(keywords[sorted_index[i]])
        top_ten = top_ten.replace("’", "")
        top_ten = top_ten.strip()
        
        
        #top_ten = top_ten.replace(" ", "+")
        #print(top_ten)
        #top_ten_all = top_ten+","+score
        #print (top_ten_all)
        dictionary.append(top_ten)
        score.append(scores)
    return dictionary,score


def render_word_cloud(corpus):
  #  '

    fig_file = BytesIO()
    wordcloud = WordCloud(max_font_size=40, background_color='white').generate(corpus)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(fig_file, format='png')
    fig_file.seek(0)
    fig_data_png = fig_file.getvalue()
    result = base64.b64encode(fig_data_png)
    return result.decode('utf-8')

def plot(corpus):
    global dictionary,score
    #print(dictionary[0])

   # pie_cneg = cneg*100/(cneg+cpos)
    #pie_cpos = cpos*100/(cneg+cpos)

    pie_chart = pygal.Pie(inner_radius=.4)
    pie_chart.title = 'Sentiment of Product (in %)'
    pie_chart.add(dictionary[0],score[0])
    pie_chart.add(dictionary[1], score[1])
    pie_chart.add('')
    #pie_chart.value_formatter = lambda x: "" % x*100/cneg+cpos
    pie_chart.render()
    return pie_chart
   