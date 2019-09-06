from flask import Flask, render_template, request,redirect
import requests
import random
import json
import time
import text_analysis
import pygal
from bs4 import BeautifulSoup as soup
#from __future__ import division # kena atas skali
from urllib.request import urlopen,Request
from urllib.request import FancyURLopener
import pandas as pd

import nltk
from nltk import word_tokenize
import string

import matplotlib.pyplot as plt
from wordcloud import WordCloud , STOPWORDS
import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)

app = Flask(__name__)

app.jinja_env.filters['zip'] = zip
@app.route('/')
def home():
	#global sentence
	return render_template('index.html')

@app.route('/limit')
def limit():
	return render_template('limit.html')

@app.route('/analysis',methods = ['POST', 'GET'])

def analysis():

	if request.method == 'POST':
		#global dictionary,score
		person = request.form.to_dict()
		person = person['person']
		sentence = request.form.to_dict()
		sentence = sentence['sentence']

		dictionary,score = text_analysis.dictionary(sentence)
		#file_contents = session.get('list_text')
		#pos_sent ,neg_sent,total_pos,total_neg = text_analysis.get_pos_neg(str(list_text))

		#result = analyzed_sent[result]
		word_cloud = text_analysis.render_word_cloud(str(sentence))
		#word_cloud = text_analysis.render_word_cloud
		pie_chart = text_analysis.plot(str(sentence))
		pie_chart.render()
		graph_data = pie_chart.render_data_uri()

		try:
    #word_relevance()
    #dictionary = ["fraud", "tax"]
    #person = "trump+"
    #person=input("Please Insert Suspected Account Name : ")
			headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
		
			headline = []
			link = []
			total = 0
			#print("sentence : ",sentence)
			for i in dictionary:
				time.sleep(0.5 * random.random())
				query = person+" "+i
				print("iiii : ",i)
				news_url="https://news.google.com/news/rss/search?q={"+query+"}"
				print(news_url)
				class MyOpener(FancyURLopener):
					version = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'   # Set this to a string you want for your user agent

				myopener = MyOpener()
				page = myopener.open(news_url)
				#urlopen(Request(url, headers={'User-Agent': 'Mozilla'}))
				#Client=urlopen(news_url)
				xml_page=page.read()
				#Client.close()

				soup_page=soup(xml_page,"xml")
				news_list=soup_page.findAll("item")
				# Print news title, url and publish date
				number=0

				for news in news_list:
					print(news.title.text)
					new = news.title.text
					print(news.link.text)
					newl= news.link.text
					print(news.pubDate.text)
					print("-"*100)
					headline.append(new)
					link.append(newl)
					number = number+1

					print("Number of Article : ",number)
					#df.to_csv(r'Path where you want to store the exported CSV file\File Name.csv')
				total = total+number
				df = pd.DataFrame(headline)
				df.to_csv("dataset.csv")
				print("Total all of the article : ", total)
			#return headline
		except ValueError :
			    print("limit requests")
			    return render_template("limit.html")
	return render_template('analysis.html', dictionary=dictionary, score=score, word_cloud=word_cloud,headline=headline,link=link,total=total,person=person,pie_chart=graph_data)  

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
   app.run(debug = True)


