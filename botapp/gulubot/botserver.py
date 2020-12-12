from django.shortcuts import render
import os

# Imports for the Bot server

import  nltk
import random
import string
import re, unicodedata

from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict

import warnings
import wikipedia as wk


def botserver(request):
    
    query = request.POST.get('query')
    # query = str(query)
    
    
    warnings.filterwarnings("ignore")
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
    
    
    module_dir = os.path.dirname(__file__)
    data_path = os.path.join(module_dir,'data.txt')
    data = open(data_path, 'r',errors = 'ignore')
    raw  = data.read()
    raw = raw.lower()
    
    sent_tokens = nltk.sent_tokenize(raw)
    
    def Normalize(text):
        remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        # word tokenization
        word_token = nltk.word_tokenize(text.lower().translate(remove_punct_dict))
    
        # remove ascii
        new_words = []
        for word in word_token:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii','ignore').decode('utf-8','ignore')
            new_words.append(new_word)
        
        # Remove tags
        rmv = []
        for w in new_words:
            text=re.sub("&lt;/?.*?&gt;","&lt;&gt;",w)
            rmv.append(text)
        
        # Pos tagging and lematization
        tag_map = defaultdict(lambda : wn.NOUN)
        tag_map['J'] = wn.ADJ
        tag_map['V'] = wn.VERB
        tag_map['R'] = wn.ADV
    
        lmtzr = WordNetLemmatizer()
        lmtzr_list = []
        rmv = [i for i in rmv if i]
        for token, tag in nltk.pos_tag(rmv):
            lemma = lmtzr.lemmatize(token, tag_map[tag[0]])
            lmtzr_list.append(lemma)
        return lmtzr_list
    
    welcome_input = ["hello", "hi", "greetings", "sup", "what's up", "hey"]
    welcome_respose = ["Hi", "Hey", "**nods**", "Hi there", "Hello"]
    
    def welcome(query):
        for word in query.split():
            if(word.lower() in welcome_input):
                return random.choice(welcome_respose)
                # return render(request, 'index.html',{'ans':ans, 'query':query})
    
    def generateResponse(query):
        robo_response=''
        sent_tokens.append(query)
        TfidfVec = TfidfVectorizer(tokenizer=Normalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = linear_kernel(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf==0) or "tell me about" or "what is" or "who is" in query:
            # print("Checking wikipedia") **Can't do it yet
            if query:
                robo_response = wikipedia_data(query)
                # return render(request,'index.html',{'ans': robo_response, 'query':query})
                return robo_response
            else:
                robo_response = robo_response+sent_tokens[idx]
                # return render(request,'index.html',{'ans': robo_response, 'query':query})
                return robo_response
                
    def wikipedia_data(query):
        if "tell me about" in query:
            reg_ex = re.search('tell me about (.*)', query)
            try:
                if reg_ex:
                    topic = reg_ex.group(1)
                    wiki = wk.summary(topic, sentences = 4)
                    return wiki
            except Exception as e:
                return ("Sorry...! No content found.")
        elif "what is" in query:
            reg_ex = re.search('what is (.*)', query)
            try:
                if reg_ex:
                    topic = reg_ex.group(1)
                    wiki = wk.summary(topic, sentences = 4)
                    return wiki
            except Exception as e:
                return ("Sorry...! No content found.")
        elif "who is" in query:
            reg_ex = re.search('who is (.*)', query)
            try:
                if reg_ex:
                    topic = reg_ex.group(1)
                    wiki = wk.summary(topic, sentences = 4)
                    return wiki
            except Exception as e:
                return ("Sorry...! No content found.")
        else:
            reg_ex = re.search('(.*)', query)
            try:
                if reg_ex:
                    topic = reg_ex.group(1)
                    wiki = wk.summary(topic, sentences = 4)
                    return wiki
            except Exception as e:
                return ("Sorry...! No content found.")
            
    # flag = True
    # while(flag==True):
    
    query = query.lower()
    if(query=='thanks' or query=='thank you'):
        return render(request,'index.html',{'ans': 'You are welcome', 'query':query})
    else:
        if(query in welcome_input):
            ans = welcome(query)
            return render(request,'index.html',{'ans': ans, 'query':query})
        else:
            ans = generateResponse(query)
            return render(request,'index.html',{'ans': ans, 'query':query})