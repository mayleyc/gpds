from text_process_module import text_process
import matplotlib
import pandas as pd
import re
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import copy
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud, ImageColorGenerator
nltk.download('punkt')
nltk.download('stopwords')



class program:
    def __init__(self, bg_folder, txt_folders,info_template, rule_dict, output_folder,  output_dir: dict, text_process):
        self.bg_folder = bg_folder
        self.bg_dir = [os.path.join(bg_folder, t) for t in os.listdir(bg_folder) if t.endswith(".jpg")]
        self.info_template = info_template
        self.txt_folders = txt_folders
        self.txt_files = [os.path.join(txt_folders, t) for t in os.listdir(txt_folders) if t.endswith(".txt")]
        self.rule_dict = rule_dict
        self.output_dir = output_dir
        self.text_process = text_process
        self.output_folder = output_folder

##### Preprocess part
    def is_preprocess(self):    
        
        """
        Prompt user for preprocessing choice.
        Returns:
        bool: True if user wants to reselect files, False otherwise.
        """
        use_proc = input('Welcome to GPTS!\nDo you wish to reselect files before using the program? \nIf yes, type Y or y. If no, press Enter to start:\n')
        if use_proc == 'Y' or use_proc == 'y':
          print('WARNING! This will rewrite all existing .csv files.\n')
          return True
        else:
          return False
       
    def get_one_book_info(self,dir):
        """
        Retrieve information for a single book.

        Parameters:
        - dir (str): Path to the text file.

        Returns:
        dict: Information dictionary for the book.
        """
        book_info = {}
        print(f'Opening: {dir} ...')
        print('Completing book data:')
        info_template = self.info_template
        with open(dir, 'r', encoding="utf8") as f:
            f = f.read()
            book_info['filename'] = str(dir)
            while True:
              is_gutenberg = input("Is this a Gutenberg Ebook that contains the phrase 'START OF THE PROJECT GUTENBERG EBOOK'? \nY/N\n")
              if is_gutenberg == "N":
                for item in info_template:
                  if item == 'start_section':
                      prompt = input("Type in the first sentence of the section you want to keep:\n")
                  elif  item == 'end_section': 
                      prompt = input("Type in the last sentence of the section you want to keep:\n")
                  else: 
                      prompt = 'Please type in the book ' + info_template[item] + ', then press Enter to continue: '
                  book_info[item] = input(prompt)
                break
              elif is_gutenberg == "Y":
                start_section = "START OF THE PROJECT GUTENBERG EBOOK"
                end_section = "END OF THE PROJECT GUTENBERG EBOOK"
                book_info['start_section'] = start_section
                book_info['end_section'] = end_section
                temp_txt = f.split('\n')
                auto_info = ['title', 'author_sur', 'author_init']
                for i in temp_txt:
                  if "Title: " in i:
                    book_info['title'] = re.sub('Title: ',"", i)
                  if "Author: " in i:
                    name = re.sub('Author: ',"", i).split()
                    book_info['author_sur'] = name[-1]
                    init = ' '.join(name[:-1])
                    book_info['author_init'] = self.text_process.make_abbreviator(init)
                for j in auto_info:
                  if j not in book_info:
                    print(f'Unable to autoretrieve book {j}. Requesting manual input...')
                if 'title' in book_info:
                  print(f"The book title is: '{book_info['title']}'")
                for item in info_template:
                  if item not in book_info:
                    prompt = 'Please type in the book ' + info_template[item] + ', then press Enter to continue: '
                    book_info[item] = input(prompt)
                break
              else:
                print("Please type in a valid answer: Y for Yes, N for No: \n")
            return book_info

    def process_all_book(self):
        """
        Process all books and return a dictionary containing book information.

        Returns:
        dict: Dictionary containing information for all books.
        """
        txt_files = self.txt_files
        all_books = {}
        book_count = 0
        for dir in txt_files: 
              with open(dir, 'r', encoding="utf8") as f:
                  f = f.read()
                  book_info = self.get_one_book_info(dir)
                  book_info['content'] = self.text_process.split_sentence(f, book_info['start_section'], book_info['end_section']) #create new key in book info, which contains all the sentence in correspond book
                  abb_title = self.text_process.make_abbreviator(book_info['title'].lower()) + "_" + str(book_count)
                  all_books[abb_title] = book_info
                  book_count += 1
        return all_books


    def flatten_dict(self, all_books:dict): 
## Input: 3-layered dict with a possible list as value: {'x':{'y':['abc', 'def']}}. Each of these value should be appended the corresponding book_info as keys.
        flat_dict = []
        info_list = list(self.info_template.keys())
        for abb, abb_value in copy.deepcopy(all_books).items():
          content_list = abb_value.pop('content')
          for sentence in content_list: #append every corresponding info, to make a csv with each sentence as the object
            flat_dict.append(dict({'Sentence' : sentence, 'Abbreviation': abb} | abb_value)) #union to merge 2 dictionaries
        return flat_dict

    def export_csv(self, all_books:dict):
        flat_dict = self.flatten_dict(all_books)
        df = pd.DataFrame.from_dict(flat_dict)
        df.to_csv(self.output_dir['all_books'], index=True)

    def export_json(self, all_books:dict):
        json_object = json.dumps(all_books, indent=4)
        with open("all_books.json", 'w') as outfile:
          outfile.write(json_object)
    
    def seperate_sent_from_all_book(self, all_book_df, rule_dict):
        '''Use to divide sentences from all books into 2 subset: 
        one subset with definition sentences (based on provided rule) and one subset with remaining sentences
        '''
        df = all_book_df
        data_with_scores = []
        data_nan_scores = []
        #Loop through all sentences and assign highest defition score to each sentence 
        for _, row in df.iterrows():
            sentence = row['Sentence']
            score = np.nan
            for rule, value in rule_dict.items():
                if re.search(rule, sentence, flags=re.IGNORECASE):
                    score = value
                    break  # Break once a match is found to get the highest score

            if np.isnan(score):
                data_nan_scores.append(row.to_dict())
            else:
                row_with_score = row.to_dict()
                row_with_score['Score'] = score
                data_with_scores.append(row_with_score)

        df_sent_def = pd.DataFrame(data_with_scores)
        df_sent_other = pd.DataFrame(data_nan_scores)
        df_sent_def.to_csv(self.output_dir['sent_def'], index=False)
        df_sent_other.to_csv(self.output_dir['sent_other'], index=False)
        return df_sent_def, df_sent_other

    def get_keyword_from_list_sent(self,sent_list):
        """
        Extract keywords from a list of sentences.

        Parameters:
        - sent_list (list): List of sentences.

        Returns:
        pd.DataFrame: DataFrame containing keywords.
        """

        keyword_dict = {}
        for i in sent_list:
            keywords = self.text_process.extract_nouns_and_verbsing(i)
            for j in keywords:
                keyword_dict[j] = ''
        df_keyword = pd.DataFrame(keyword_dict, columns = ['keyword']).sort_values(by = 'keyword', ascending = True)
        keyword = df_keyword.to_csv(self.output_dir['keyword'], index=False)
        return df_keyword    

    def preprocess(self):
      """
      Combile all steps neeeded to process all books from txt format to final format, which is 4 csv file 
      First csv file contains all sentences from all book, with one sentence in one row, and have following columns: sentence, book title, book author, ....
      Second csv file contains definition sentences (based on provided rule) and same column as first csv file
      Third csv file contains remaining sentences and same column as first csv file
      4th csv file contains keywords from all books ( keyword is a noun or Ving )
      """  
      rule_dict = self.rule_dict
      #create output folder for output files
      os.makedirs(self.output_folder, exist_ok=True)
      #create a dictionary that has all books information, which also includes sentences of book
      print("Start of preprocessing")
      all_books = self.process_all_book()
      #export dictionary to csv file
      self.export_csv(all_books)
      print('Exported .txt files to .csv files.')
      #Divide all book sentences csv file into 2 small csv file: definition sentences csv file and remaining sentences csv file
      all_book_df = pd.read_csv(self.output_dir['all_books'])
      df_sent_def, df_sent_other = self.seperate_sent_from_all_book(all_book_df, rule_dict)
      #Create csv files that contains keyword from all book 
      self.get_keyword_from_list_sent(all_book_df['Sentence'])
      print("End of preprocessing, please check output directory")


#### Main function part

    def get_definition(self, keyword):
        
        """
        Get definitions for a given keyword.

        Parameters:
        - keyword (str): Keyword to search for.

        Returns:
        str: Concatenated sentences and book information.
        """
        sent_def =  pd.read_csv(self.output_dir['sent_def'])
        sent_other = pd.read_csv(self.output_dir['sent_other'])

        # Remove sentences longer than 600 characters, because most of those sentence is mistake when split sentence
        sent_def = sent_def[sent_def['Sentence'].str.len() <= 600]
        sent_other = sent_other[sent_other['Sentence'].str.len() <= 600]

        # Get 2 Sentences with the lowest rank
        filtered_def = sent_def[sent_def['Sentence'].str.contains(keyword, case=False)].nsmallest(2, ['Score'])

        # Search for keyword in sent_other and count occurrences
        sent_other['keyword_count'] = sent_other['Sentence'].str.lower().str.count(keyword.lower())

        # Get 3 Sentences with the most keyword occurrences
        filtered_other = sent_other[sent_other['Sentence'].str.contains(keyword, case=False)].nlargest(3, 'keyword_count')

        # Concatenate the Sentences
        result_Sentences = pd.concat([filtered_def['Sentence'], filtered_other['Sentence']])

        # Print the concatenated Sentences
        #print("\nConcatenated Sentences:")
        output_text = []
        
        for idx, Sentence in enumerate(result_Sentences, 1):
            if len(Sentence) <= 600:
                output_text.append(f"{idx}. {Sentence}\n")
              
        # Extract book info for the selected Sentences
        all_book_info = pd.concat([filtered_def[['title','author_sur', 'editn']], filtered_other[['title','author_sur', 'editn']]])

        # Remove duplicate book info entries
        unique_book_info = all_book_info.drop_duplicates()

        #print("\nAll Book Infos:")
        for _, row in unique_book_info.iterrows():
            info_str = ', '.join([f"{column}: {value}" for column, value in row.items()])
            output_text.append(info_str)
        return '#'.join(output_text)

    def search_keyword_all_text(self, keyword): #all_books.csv with read_csv
        """
        Search for a keyword in all book text.

        Parameters:
        - keyword (str): Keyword to search for.

        Returns:
        tuple: (contains_keyword (bool), all_relw (dict)).
        """
        stop_words = set(stopwords.words('english'))
        all_books = pd.read_csv(self.output_dir['all_books'])
        all_relw = {} #dict of all words in sentences containing the keyword
        for sentence in all_books['Sentence']:
          words = sentence.split()
          words = [re.sub(r"[\;\:\"\.\,\!\?\[\]\(\)\{\}\/]", '', word) for word in words]
          if keyword in sentence.lower():
            words = [word for word in words if word.lower() not in stop_words and re.match(keyword, word, re.I) == None]
            for word in words:
              if word in all_relw:
                all_relw[word] += 1
              else:
                all_relw[word] = 1
        if not all_relw:
          contains_keyword = False
        else:
          contains_keyword = True
        return contains_keyword, all_relw 

    def top_related(self, all_relw):
        """
        Get top related words based on frequency.

        Parameters:
        - all_relw (dict): Dictionary containing word frequencies.

        Returns:
        pd.DataFrame: DataFrame containing top related words.
        """
        word_rank = pd.DataFrame.from_dict(all_relw, orient='index', columns=['Frequency']).sort_values(by='Frequency', ascending=False)
        word_rank.index.name = 'Related Word'
        cloud_text = word_rank.head(20)
        return cloud_text

    def create_wordcloud(self, cloud_text, bg): 
        """
        Create and save a word cloud image.

        Parameters:
        - cloud_text (pd.DataFrame): DataFrame containing words and frequencies.
        - bg (str): Path to the background image.

        Returns:
        None
        """
        bg = bg 

        cloud_text_to_list = cloud_text.index.tolist()

        cloud_colors = np.array(Image.open(bg))
        wordcloud = WordCloud(background_color="#1C2833",
                              mask=cloud_colors,
                              max_font_size=70)
        wordcloud.generate(' '.join(cloud_text_to_list)) #convert cloud_text from dataframe to string
        # create coloring
        image_colors = ImageColorGenerator(cloud_colors)
        #pyplot display images as png
        plt.axis('off')
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
        time = datetime.now()
        filename = 'cloud_result_' + time.strftime("%Y%m%d_%H%M%S")+'.png'
        plt.savefig(os.path.join(self.output_folder,filename))

    def get_wordcloud(self, keyword, bg):
        '''Combine all steps to make a word cloud'''
        
        contains_keyword, all_relw = self.search_keyword_all_text(keyword)

        if contains_keyword == False:
          pass
        else:
          cloud_text = self.top_related(all_relw)
          self.create_wordcloud(cloud_text, bg)
        
        return contains_keyword