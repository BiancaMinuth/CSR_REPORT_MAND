# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:15:47 2022

@author: bianca
"""

# Adjustment of CSR Scores file

import pandas as pd 
import os
import numpy as np


df_CSR_scores_us = pd.read_csv("./data/generated/1_csr_scores_us_06-12-2023.csv")
df_CSR_scores_eu_1 = pd.read_csv("./data/generated/1_csr_scores_eu_29-09-2023_1.csv")
df_CSR_scores_eu_2 = pd.read_csv("./data/generated/1_csr_scores_eu_29-09-2023_1.csv")
#df_CSR_scores_2 = pd.read_csv("./...")
#df_CSR_scores_3 = pd.read_csv("./B_CSR_scores_calculation_Python/output/1.CSR_scores_output_3.csv")

## 1. Merge two dataframes: df_CSR_scores_group & df_CSR_reports_collect
df_CSR_scores_eu = pd.concat([df_CSR_scores_eu_1, df_CSR_scores_eu_2], join='inner')

## Create column 'firm_abbr_pdf' based on 'folder_name' displaying the first 3 letters of the firm name
df_CSR_scores_us['ISIN'] = [name[18:30] for name in df_CSR_scores_us['folder_name']]
df_CSR_scores_eu['ISIN'] = [name[42:54] for name in df_CSR_scores_eu['folder_name']]

## Create column 'fiscal_year' based on 'folder_name'
df_CSR_scores_us['fiscal_year'] = [date[-11:-7] for date in df_CSR_scores_us['folder_name']]
df_CSR_scores_eu['fiscal_year'] = [date[-11:-7] for date in df_CSR_scores_eu['folder_name']]

## Create column 'report_type' based on 'folder_name' displaying the initials of reports (CSR or Integrated report [IR])
df_CSR_scores_us['report_type'] = [report[-6:-4] for report in df_CSR_scores_us['folder_name']]
df_CSR_scores_eu['report_type'] = [report[-6:-4] for report in df_CSR_scores_eu['folder_name']]

## create 'report_type_IR_dummy' in column
def dummy(report_type):    
    if report_type == 'SR': return(1)
    if report_type == 'IR': return(2)
    return (0)

df_CSR_scores_us['report_type'] = [dummy(i) for i in df_CSR_scores_us['report_type']] # for IR = 0, for CSR = 1
df_CSR_scores_eu['report_type'] = [dummy(i) for i in df_CSR_scores_eu['report_type']] # for IR = 0, for CSR = 1
#print(df_CSR_scores['report_type'])

## Create column 'firm_year_report' based on merge of 'fiscal_year' and  'firm_abbr_pdf'
#df_CSR_scores['firm_year_report'] = df_CSR_scores['firm_abbr_pdf'] + df_CSR_scores['fiscal_year'] + df_CSR_scores['report_type']
#df_CSR_scores['ISIN_year_report'] = df_CSR_scores.iloc[:,16:19].apply(lambda x: "".join(x.astype(str)), axis=1)

## define relevant columns for output file
df_CSR_us = df_CSR_scores_us.groupby(['ISIN', 'fiscal_year', 'report_type',
                                   ]).agg({
                                            'file_size': 'mean',
                                            'number_of_words': 'mean',
                                            'perc_negative': 'mean',
                                            'perc_positive': 'mean',
                                            'perc_uncertainty': 'mean',
                                            'perc_litigious': 'mean', 
                                            'perc_strong_modal': 'mean',
                                            'perc_weak_modal': 'mean',
                                            'perc_constraining': 'mean',
                                            'No_of_alphabetic': 'mean',
                                            'No_of_digits': 'mean',
                                            'No_of_numbers': 'mean',	
                                            'avg_No_of_syllables_per_word': 'mean',
                                            'avg_word_length': 'mean', 
                                            'vocabulary': 'mean'
#                                            'first_mention' == 'True': 'count'
                                            })
 

df_CSR_eu = df_CSR_scores_eu.groupby(['ISIN', 'fiscal_year', 'report_type',
                                   ]).agg({
                                            'file_size': 'mean',
                                            'number_of_words': 'mean',
                                            'perc_negative': 'mean',
                                            'perc_positive': 'mean',
                                            'perc_uncertainty': 'mean',
                                            'perc_litigious': 'mean', 
                                            'perc_strong_modal': 'mean',
                                            'perc_weak_modal': 'mean',
                                            'perc_constraining': 'mean',
                                            'No_of_alphabetic': 'mean',
                                            'No_of_digits': 'mean',
                                            'No_of_numbers': 'mean',	
                                            'avg_No_of_syllables_per_word': 'mean',
                                            'avg_word_length': 'mean', 
                                            'vocabulary': 'mean'
#                                            'first_mention' == 'True': 'count'
                                            })                                      
                                                                                                                                                                              
## merge dfs
df_CSR_eu_us = pd.concat([df_CSR_eu, df_CSR_us], join='inner')

## Save to csv
df_CSR_eu_us.to_csv("./data/generated/2_csr_scores_prep_06-12-2023.csv")        
#df_CSR_scores_group.to_csv("./C_CSR_analysis_R/data/generated/2.CSR_scores_preparation_29-09-2023.csv")  

##############################################################################################################################################

