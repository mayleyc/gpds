import re
import os
import subprocess
import json
import copy
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize


nltk.download('punkt') #=> can we download the requirements on the same file, because they all need nltk downloads?
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')


class text_process:
    def __init__(self):
        pass
    def make_abbreviator(self,text:str):
        t = text.split()
        abb = []
        for word in t:
          a = word[0]
          abb.append(a)
        return ''.join(abb)

    def split_sentence(self, text, start_section, end_section):
    #Spit sentence of a input text
      print("Splitting the sentences...")
      text = sent_tokenize(text)
      text = [re.sub(r'(\n)+', ' ', i) for i in text]

      print(f"Removing the header and the footer...")
      hl = 0
      fl = -1
      for index, i in enumerate(text):
        if start_section in i:
          hl = index
        if end_section in i:
          fl = index
      text = text[hl+1:fl] #splicing to remove header and footer
      return text

    def extract_nouns_and_verbsing(self,text):
        # Tokenize the text into words
        words = word_tokenize(text)

        # Remove stopwords => test w new json file; stopwords.words() will give lowercase
        stop_words = set(stopwords.words('english'))
        words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words] # why not lower() all words first? :v is it harder to get stopwords then?
        # somehow, it works when you don't remove stopwords? Maybe only need to remove pronouns?

        # Perform part-of-speech tagging
        pos_tags = pos_tag(words)

        # Initialize the WordNetLemmatizer
        lemmatizer = WordNetLemmatizer()

        # Extract lemmatized nouns and verbs ending with "-ing" based on POS tagging
        result = []
        for word, pos in pos_tags:
            if pos.startswith('N'):
                lemmatized_noun = lemmatizer.lemmatize(word, pos='n')
                result.append(lemmatized_noun)
            elif pos == 'VBG' and word.endswith('ing'):
                result.append(word)

        return result

