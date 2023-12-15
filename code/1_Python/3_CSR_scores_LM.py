# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 16:55:13 2022

@author: bianca
"""

# Scores creation according to Loughran & McDonald

'''
Program to provide generic parsing for all files in a user-specified directory.
The program assumes the input files have been scrubbed,
  i.e., HTML, ASCII-encoded binary, and any other embedded document structures that are not
  intended to be analyzed have been deleted from the file.

Dependencies:
    Python:  MOD_Load_MasterDictionary_vxxxx.py
    Data:    LoughranMcDonald_MasterDictionary_XXXX.csv

The program outputs:
   1.  File name
   2.  File size (in bytes)
   3.  Number of words (based on LM_MasterDictionary)
   4.  Proportion of positive words (use with care - see LM, JAR 2016)
   5.  Proportion of negative words
   6.  Proportion of uncertainty words
   8.  Proportion of modal-strong words
   9.  Proportion of modal-weak words
  10.  Proportion of constraining words (see Bodnaruk, Loughran and McDonald, JFQA 2015)
  11.  Number of alphanumeric characters (a-z, A-Z)
  12.  Number of digits (0-9)
  13.  Number of numbers (collections of digits)
  14.  Average number of syllables
  15.  Average word length
  16.  Vocabulary (see Loughran-McDonald, JF, 2015)

  ND-SRAF
  McDonald 201606 : updated 201803; 202107; 202201
  
  Source: https://sraf.nd.edu/textual-analysis/code/ --> Generic_Parser.py
'''


import csv
import glob
import re
import string
import sys
import datetime as dt
import MOD_Load_MasterDictionary_v2022 as LM

# User defined directory for files to be parsed --> change to own path
TARGET_FILES = ('./data/reports_us/*.*')

# User defined file pointer to LM dictionary
MASTER_DICTIONARY_FILE =  ('./data/external/Loughran-McDonald_MasterDictionary_1993-2021.csv')

#r'\CSR_scores_calculation_Python\input\\' + \
 #                        r'Loughran-McDonald_MasterDictionary_1993-2021.csv'
# User defined output file --> change to own path
OUTPUT_FILE = ('./data/generated/1_csr_scores_us_06-12-2023.csv')
# Setup output
OUTPUT_FIELDS = ['folder_name', 'file_size', 'number_of_words', 'perc_negative', 'perc_positive',
                 'perc_uncertainty', 'perc_litigious', 'perc_strong_modal', 'perc_weak_modal',
                 'perc_constraining', 'No_of_alphabetic', 'No_of_digits',
                 'No_of_numbers', 'avg_No_of_syllables_per_word', 'avg_word_length', 'vocabulary']

# load dictonary
lm_dictionary = LM.load_masterdictionary(MASTER_DICTIONARY_FILE, print_flag=True)

def main():

    f_out = open(OUTPUT_FILE, 'w')
    wr = csv.writer(f_out, lineterminator='\n')
    wr.writerow(OUTPUT_FIELDS)

    folder_list = glob.glob(TARGET_FILES)
    n_folder = 0
    for folder in folder_list:
        n_folder += 1
    #    print(f'{n_files:,} : {file}')
        print('folder')
        with open(folder, 'r', encoding='UTF-8', errors='ignore') as f_in:
            doc = f_in.read()
        doc = re.sub('(May|MAY)', ' ', doc)  # drop all May month references
        doc = doc.upper()  # for this parse caps aren't informative so shift

        output_data = get_data(doc)
      #  output_data[0] = file
        output_data[0] = folder # folder path
        output_data[1] = len(doc) # file size
        wr.writerow(output_data)
  #      if n_files == 430: break

def get_data(doc):

    vdictionary = dict()
    _odata = [0] * 16
    total_syllables = 0
    word_length = 0
    
    tokens = re.findall('\w+', doc)  # Note that \w+ splits hyphenated words
    for token in tokens:
        if not token.isdigit() and len(token) > 1 and token in lm_dictionary:
            _odata[2] += 1  # word count
            word_length += len(token)
            if token not in vdictionary:
                vdictionary[token] = 1
            if lm_dictionary[token].negative: _odata[3] += 1 # perc_negative
            if lm_dictionary[token].positive: _odata[4] += 1 # perc_positive
            if lm_dictionary[token].uncertainty: _odata[5] += 1 # perc_uncertainty
            if lm_dictionary[token].litigious: _odata[6] += 1 # perc_litigious
            if lm_dictionary[token].strong_modal: _odata[7] += 1 # perc_strong_modal
            if lm_dictionary[token].weak_modal: _odata[8] += 1 # perc_weak_modal
            if lm_dictionary[token].constraining: _odata[9] += 1 # perc_constraining
            total_syllables += lm_dictionary[token].syllables

    _odata[10] = len(re.findall('[A-Z]', doc)) # No_of_alphabetic
    _odata[11] = len(re.findall('[0-9]', doc)) # No_of_digits
    # drop punctuation within numbers for number count
    doc = re.sub('(?!=[0-9])(\.|,)(?=[0-9])', '', doc)
    doc = doc.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    _odata[12] = len(re.findall(r'\b[-+\(]?[$€£]?[-+(]?\d+\)?\b', doc)) # No_of_numbers
    _odata[13] = total_syllables / _odata[2] # avg_No_of_syllables_per_word
    _odata[14] = word_length / _odata[2] # avg_word_length
    _odata[15] = len(vdictionary) # vocabulary langth

    
    # Convert counts to %
    for i in range(3, 9 + 1):
        _odata[i] = (_odata[i] / _odata[2]) * 100
    # Vocabulary
        
    return _odata


if __name__ == '__main__':
    start = dt.datetime.now()
    print(f'\n\n{start.strftime("%c")}\nPROGRAM NAME: {sys.argv[0]}\n')
    main()
    print(f'\n\nRuntime: {(dt.datetime.now()-start)}')
    print(f'\nNormal termination.\n{dt.datetime.now().strftime("%c")}\n')
    
##############################################################################################################################################
    
