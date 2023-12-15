# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 18:09:42 2023

@author: bianca
"""

##############################################################################################################################################

# Adjustment of Refinitiv file

import pandas as pd 
import os
import numpy as np


# open csv file
df_refinitiv = pd.read_csv("./data/pulled/3_csr_refinitiv_api_eu_us_04-10-2023.csv")     
# drop unnecessary columns                    
df_refinitiv = df_refinitiv.drop(columns=['Unnamed: 0'])
#.drop(columns=['Unnamed: 34']).drop(columns=['Unnamed: 35'])
# rename colums and set index 
#df_refinitiv = df_refinitiv.rename({'Unnamed: 1': 'Identifier'}, axis=1)
df_refinitiv.set_index('Instrument', inplace=True)

# fill nan values with prior (not-nan)value
#df_refinitiv['Instrument'] = df_refinitiv['Instrument'].fillna(method='ffill')
df_refinitiv['ISIN'] = df_refinitiv['ISIN'].fillna(method='ffill')
df_refinitiv['SEDOL'] = df_refinitiv['SEDOL'].fillna(method='ffill')
df_refinitiv['CUSIP'] = df_refinitiv['CUSIP'].fillna(method='ffill')
df_refinitiv['Company Name'] = df_refinitiv['Company Name'].fillna(method='ffill')
df_refinitiv['Country of Headquarters'] = df_refinitiv['Country of Headquarters'].fillna(method='ffill')
df_refinitiv['NAICS Sector Code'] = df_refinitiv['NAICS Sector Code'].fillna(method='ffill')
df_refinitiv['NAICS Sector Name'] = df_refinitiv['NAICS Sector Name'].fillna(method='ffill')

# rename date and display only the fiscal year 
df_refinitiv["date"] = df_refinitiv["Date"].apply(str)
df_refinitiv['fiscal_year'] = [name[0:4] for name in df_refinitiv['date']]

# change column names
df_refinitiv["comp_name"] = df_refinitiv["Company Name"].apply(str)
df_refinitiv["market_cap_m"] = df_refinitiv["Company Market Capitalization"].apply(str)
df_refinitiv["ni_m"] = df_refinitiv["Net Income - Actual"].apply(str)
df_refinitiv["at_m"] = df_refinitiv["Total Assets - Actual"].apply(str)
#df_refinitiv["cat_m"] = df_refinitiv["Total Current Assets"].apply(str)
df_refinitiv["lt_m"] = df_refinitiv["Total Liabilities"].apply(str)
df_refinitiv["debt_m"] = df_refinitiv["Total Liabilities And Shareholders' Equity"].apply(str)
df_refinitiv["rev_m"] = df_refinitiv["Total Revenue"].apply(str)
#df_refinitiv["growth_lt_m"] = df_refinitiv["Long Term Growth - Mean"].apply(str)
df_refinitiv["NAICS_code"] = df_refinitiv["NAICS Sector Code"].apply(str)
df_refinitiv["NAICS_name"] = df_refinitiv["NAICS Sector Name"].apply(str)
#df_refinitiv["ESG_date"] = df_refinitiv["ESG Period Last Update Date"].apply(str)
df_refinitiv["ESG_score"] = df_refinitiv["ESG Score"].apply(str)
#df_refinitiv["ESG_comb_score"] = df_refinitiv["ESG Combined Score"].apply(str)
#df_refinitiv["ESG_contro_score"] = df_refinitiv["ESG Controversies Score.1"].apply(str)
#df_refinitiv["Env_innov_score"] = df_refinitiv["Environmental Innovation Score"].apply(str)
df_refinitiv["Env_pillar_score"] = df_refinitiv["Environmental Pillar Score"].apply(str)
#df_refinitiv["Env_contro_score"] = df_refinitiv["Environmental Controversies Score"].apply(str)
#df_refinitiv["Env_prod_score"] = df_refinitiv["Environmental Products Score"].apply(str)
df_refinitiv["emissions_score"] = df_refinitiv["Emissions Score"].apply(str)
#df_refinitiv["exec_gen_div_score"] = df_refinitiv["Executive Members Gender Diversity, Percent Score"].apply(str)
df_refinitiv["board_gen_div_score"] = df_refinitiv["Board Gender Diversity, Percent"].apply(str)
#df_refinitiv["board_culture_div_score"] = df_refinitiv["Board Cultural Diversity, Percent Score"].apply(str)
#df_refinitiv["board_fem"] = df_refinitiv["Female on Board"].apply(str)
df_refinitiv["social_pillar_score"] = df_refinitiv["Social Pillar Score"].apply(str)
df_refinitiv["wacc"] = df_refinitiv["Weighted Average Cost of Capital, (%)"].apply(str)
df_refinitiv["wacc_debt"] = df_refinitiv["WACC Cost of Debt, (%)"].apply(str)
df_refinitiv["wacc_equity"] = df_refinitiv["WACC Cost of Equity, (%)"].apply(str)
df_refinitiv["beta"] = df_refinitiv["Beta"].apply(str)
df_refinitiv["country"] = df_refinitiv["Country of Headquarters"].apply(str)
df_refinitiv["age"] = df_refinitiv["Date of Incorporation"].apply(str)
df_refinitiv["analysts"] = df_refinitiv["Number of Analysts"].apply(str)


# drop unnecessary columns
df_refinitiv = df_refinitiv.drop(columns=['Date'])
df_refinitiv = df_refinitiv.drop(columns=['Company Name'])
df_refinitiv = df_refinitiv.drop(columns=['Company Market Capitalization'])
df_refinitiv = df_refinitiv.drop(columns=['Net Income - Actual'])
df_refinitiv = df_refinitiv.drop(columns=['Total Assets - Actual'])
df_refinitiv = df_refinitiv.drop(columns=['Total Current Assets'])
df_refinitiv = df_refinitiv.drop(columns=['Total Liabilities'])
df_refinitiv = df_refinitiv.drop(columns=["Total Liabilities And Shareholders' Equity"])
df_refinitiv = df_refinitiv.drop(columns=['Total Revenue'])
df_refinitiv = df_refinitiv.drop(columns=['Long Term Growth - Mean'])
df_refinitiv = df_refinitiv.drop(columns=['NAICS Sector Code'])
df_refinitiv = df_refinitiv.drop(columns=['NAICS Sector Name'])
df_refinitiv = df_refinitiv.drop(columns=['ESG Period Last Update Date'])
df_refinitiv = df_refinitiv.drop(columns=['ESG Score'])
df_refinitiv = df_refinitiv.drop(columns=['ESG Combined Score'])
df_refinitiv = df_refinitiv.drop(columns=['ESG Controversies Score.1'])
df_refinitiv = df_refinitiv.drop(columns=['Environmental Innovation Score'])
df_refinitiv = df_refinitiv.drop(columns=['Environmental Pillar Score'])
df_refinitiv = df_refinitiv.drop(columns=['Environmental Controversies Score'])
df_refinitiv = df_refinitiv.drop(columns=['Environmental Products Score'])
df_refinitiv = df_refinitiv.drop(columns=['Environmental Expenditures Investments Score'])
df_refinitiv = df_refinitiv.drop(columns=['Emissions Score'])
df_refinitiv = df_refinitiv.drop(columns=['Executive Members Gender Diversity, Percent Score'])
df_refinitiv = df_refinitiv.drop(columns=['Board Gender Diversity, Percent'])
df_refinitiv = df_refinitiv.drop(columns=['Board Cultural Diversity, Percent Score'])
df_refinitiv = df_refinitiv.drop(columns=['Female on Board'])
df_refinitiv = df_refinitiv.drop(columns=['Social Pillar Score'])
df_refinitiv = df_refinitiv.drop(columns=['Weighted Average Cost of Capital, (%)'])
df_refinitiv = df_refinitiv.drop(columns=['WACC Cost of Debt, (%)'])
df_refinitiv = df_refinitiv.drop(columns=['WACC Cost of Equity, (%)'])
df_refinitiv = df_refinitiv.drop(columns=['Beta'])
df_refinitiv = df_refinitiv.drop(columns=['Country of Headquarters'])
df_refinitiv = df_refinitiv.drop(columns=['Date of Incorporation'])
df_refinitiv = df_refinitiv.drop(columns=['Number of Analysts'])

df_refinitiv.to_csv("./data/pulled/4_refinitiv_prep_04-10-2023.csv")  
df_refinitiv.to_csv("./C_CSR_analysis_R/data/generated/5.Refinitiv_API_prep_04-10-2023.csv") 


df_CSR_scores_group = pd.read_csv("./B_CSR_scores_calculation_Python/output/2.CSR_scores_preparation_29-09-2023.csv")
df_CSR_scores_refinitiv = pd.concat([df_refinitiv, df_CSR_scores_group], join='inner')
df_CSR_scores_refinitiv
  