# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 13:42:25 2023

@author: bianca
"""
#### API Refinitiv Data & Preparation ####


import eikon as ek
import datetime
import pandas as pd 
import os
import numpy as np


# Your configuration
ek.set_app_key('xxx')

####################################################################################################

0#.STOXX
# API refinitiv EU data
# 0#.SPX for S&P500, 0#.STOXX for Euro STOXX 600
EU_financial_data,err = ek.get_data('0#.STOXX', 
                               fields=['TR.ISIN; TR.CUSIP; TR.SEDOL; \
                                       TR.CompanyName; \
                                       TR.TotalAssetsReported(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).periodenddate;\
                                       TR.CompanyMarketCapitalization(SDate=0,EDate=-17,Frq=FY,Scale=6,Curn=EUR).value; \
                                       TR.NetProfitActValue(SDate=0,EDate=-17,Frq=FY, Scale=6,ActType=All,AlignType=PeriodEndDate,Curn=EUR).value;\
                                       TR.TotalRevenue(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).value;\
                                       TR.RevenueMean(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).value;\
                                       TR.TotalRevenue(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).value;\
                                       TR.TotalAssetsReported(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).value;\
                                       TR.TotalAssetsActual(SDate=0,EDate=-17,Frq=FY,ActType=All,AlignType=PeriodEndDate,Scale=6,Curn=EUR).value; \
                                       TR.TtlLiabShareholderEqty(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).value;\
                                       TR.TotalLiabilities(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).value; \
                                       TR.WACC(SDate=0,EDate=-17,Frq=FY).value;\
                                       TR.WACCCostofDebt(SDate=0,EDate=-17,Frq=FY).value; \
                                       TR.WACCCostofEquity(SDate=0, EDate=-17,Frq=FY).value; \
                                       TR.WACCBeta(SDate=0,EDate=-17,Frq=FY).value;\
                                       TR.OProfitActValue(SDate=0,EDate=-17,Frq=FY).value;\
                                       TR.NumberOfAnalysts(SDate=0,EDate=-17,Frq=FY,AlignType=PeriodEndDate).value; \
                                       TR.NAICSSectorCode; TR.NAICSSector;TR.HeadquartersCountry; \
                                       TR.CompanyIncorpDate; TR.DealAcquiror; \
                                       '])                                                                   

                                  
#TR.InvtrRevenue
#TR.DealAcquiror(DealDateType=CD,Entity=CMPY,SDate=0,EDate=-16,Frq=FY).value \
#TR.NetProfitActValue(Scale=6 ActType=All "&"AlignType=PeriodEndDate)
#TR.FH.Year;TR.MnATargetDateOfCurrentFiscalYrEndforFin; 
#TR.CompanyFYearEnd;                                                                                                              
EU_financial_data,err
# create a dataframe
df_EU_financials = pd.DataFrame(data=EU_financial_data)


# rename Date and display only the report year 
df_EU_financials["Date"] = df_EU_financials["Period End Date"].apply(str)
df_EU_financials['report_year'] = [name[0:4] for name in df_EU_financials['Date']]

df_EU_financials.to_csv("./B_CSR_scores_calculation_Python/output/4.Refinitiv_EU_financials_04-10-2023.csv")  
df_EU_financials = pd.read_csv("./B_CSR_scores_calculation_Python/output/4.Refinitiv_EU_financials_04-10-2023.csv")  
df_EU_financials['ISIN'] = df_EU_financials['ISIN'].fillna(method='ffill')
df_EU_financials['Company Name'] = df_EU_financials['Company Name'].fillna(method='ffill')
df_EU_financials['CUSIP'] = df_EU_financials['CUSIP'].fillna(method='ffill')
df_EU_financials['SEDOL'] = df_EU_financials['SEDOL'].fillna(method='ffill')
df_EU_financials['Country of Headquarters'] = df_EU_financials['Country of Headquarters'].fillna(method='ffill')
df_EU_financials['NAICS Sector Code'] = df_EU_financials['NAICS Sector Code'].fillna(method='ffill')
df_EU_financials['NAICS Sector Name'] = df_EU_financials['NAICS Sector Name'].fillna(method='ffill')
#df_financials['Age'] = EU_df_financials['Date of Incorporation'].fillna(method='ffill')
df_EU_financials = df_EU_financials.drop(columns=['Unnamed: 0'])

####################################################################################################

0#.STOXX
# API refinitiv US data
# 0#.SPX for S&P500, 0#.STOXX for Euro STOXX 600
US_financial_data,err = ek.get_data('0#.SPX', 
                               fields=['TR.ISIN; TR.CUSIP; TR.SEDOL; \
                                       TR.CompanyName; \
                                       TR.TotalAssetsReported(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).periodenddate;\
                                       TR.CompanyMarketCapitalization(SDate=0,EDate=-17,Frq=FY,Scale=6,Curn=EUR).value; \
                                       TR.NetProfitActValue(SDate=0,EDate=-17,Frq=FY, Scale=6,ActType=All,AlignType=PeriodEndDate,Curn=EUR).value;\
                                       TR.TotalRevenue(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).value;\
                                       TR.RevenueMean(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).value;\
                                       TR.TotalRevenue(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).value;\
                                       TR.TotalAssetsReported(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).value;\
                                       TR.TotalAssetsActual(SDate=0,EDate=-17,Frq=FY,ActType=All,AlignType=PeriodEndDate,Scale=6,Curn=EUR).value; \
                                       TR.TtlLiabShareholderEqty(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).value;\
                                       TR.TotalLiabilities(SDate=0,EDate=-17,Frq=FY,Scale=6,AlignType=PeriodEndDate,Curn=EUR).value; \
                                       TR.WACC(SDate=0,EDate=-17,Frq=FY).value;\
                                       TR.WACCCostofDebt(SDate=0,EDate=-17,Frq=FY).value; \
                                       TR.WACCCostofEquity(SDate=0, EDate=-17,Frq=FY).value; \
                                       TR.WACCBeta(SDate=0,EDate=-17,Frq=FY).value;\
                                       TR.OProfitActValue(SDate=0,EDate=-17,Frq=FY).value;\
                                       TR.NumberOfAnalysts(SDate=0,EDate=-17,Frq=FY,AlignType=PeriodEndDate).value; \
                                       TR.NAICSSectorCode; TR.NAICSSector;TR.HeadquartersCountry; \
                                       TR.CompanyIncorpDate; TR.DealAcquiror; \
                                       '])                                                                   


                                     


#TR.InvtrRevenue
#TR.DealAcquiror(DealDateType=CD,Entity=CMPY,SDate=0,EDate=-16,Frq=FY).value \
#TR.NetProfitActValue(Scale=6 ActType=All "&"AlignType=PeriodEndDate)
#TR.FH.Year;TR.MnATargetDateOfCurrentFiscalYrEndforFin; 
#TR.CompanyFYearEnd;                                                                                                              
US_financial_data,err
# create a dataframe
df_US_financials = pd.DataFrame(data=US_financial_data)


# rename Date and display only the report year 
df_US_financials["Date"] = df_US_financials["Period End Date"].apply(str)
df_US_financials['report_year'] = [date[0:4] for date in df_US_financials['Date']]

df_US_financials.to_csv("./B_CSR_scores_calculation_Python/output/4.Refinitiv_US_financials_04-10-2023.csv")  
df_US_financials = pd.read_csv("./B_CSR_scores_calculation_Python/output/4.Refinitiv_US_financials_04-10-2023.csv")  
df_US_financials['ISIN'] = df_US_financials['ISIN'].fillna(method='ffill')
df_US_financials['Company Name'] = df_US_financials['Company Name'].fillna(method='ffill')
df_US_financials['CUSIP'] = df_US_financials['CUSIP'].fillna(method='ffill')
df_US_financials['SEDOL'] = df_US_financials['SEDOL'].fillna(method='ffill')
df_US_financials['Country of Headquarters'] = df_US_financials['Country of Headquarters'].fillna(method='ffill')
df_US_financials['NAICS Sector Code'] = df_US_financials['NAICS Sector Code'].fillna(method='ffill')
df_US_financials['NAICS Sector Name'] = df_US_financials['NAICS Sector Name'].fillna(method='ffill')
#df_financials['Age'] = EU_df_financials['Date of Incorporation'].fillna(method='ffill')
df_US_financials = df_US_financials.drop(columns=['Unnamed: 0'])

###########################################################################################################

# API refinitiv ESG US data
ESG_EU_data,err = ek.get_data('0#.STOXX',
                           fields=['TR.TRESGScore(SDate=0,Period=FY0,EDate=-17,Frq=FY).date; \
                                   TR.TRESGScore(SDate=0,Period=FY0,EDate=-17,Frq=FY).value; \
                                   TR.EnvironmentPillarScore(SDate=0,EDate=-17,Frq=FY).value; \
                                   TR.TRESGEmissionsScore(SDate=0,EDate=-17,Frq=FY).value; \
                                   TR.EnvExpenditures(SDate=0,EDate=-17,Frq=FY).value; \
                                   TR.AnalyticEstimatedCO2Total(SDate=0,EDate=-17,Frq=FY).value; \
                                   TR.SocialPillarScore(SDate=0,EDate=-17,Frq=FY).value; \
                                   TR.AnalyticBoardFemale(SDate=0,EDate=-17,Frq=FY).value; \
                                   TR.AnalyticBoardCulturalDiversity(SDate=0,EDate=-17,Frq=FY).value;\
                                   TR.TrainingCostsTotal(SDate=0,EDate=-17,Frq=FY).value;\
                                   '])                                                                                                                                                                                  
ESG_EU_data,err

# create a dataframe
df_EU_ESG = pd.DataFrame(data=ESG_EU_data)


df_EU_ESG["Date"] = df_EU_ESG["Date"].apply(str)
df_EU_ESG['report_year'] = [name[0:4] for name in df_EU_ESG['Date']]
df_EU_ESG = df_EU_ESG.drop(columns=['Date'])

df_EU_ESG.to_csv("./B_CSR_scores_calculation_Python/output/4.Refinitiv_ESG_EU_04-10-2023.csv")  
df_EU_ESG = pd.read_csv("./B_CSR_scores_calculation_Python/output/4.Refinitiv_ESG_EU_04-10-2023.csv")  
df_EU_ESG = df_EU_ESG.drop(columns=['Unnamed: 0'])

###########################################################################################################

# API refinitiv ESG US data
ESG_US_data,err = ek.get_data('0#.SPX',
                           fields=['TR.TRESGScore(SDate=0,Period=FY0,EDate=-17,Frq=FY).date; \
                                   TR.TRESGScore(SDate=0,Period=FY0,EDate=-17,Frq=FY).value; \
                                   TR.EnvironmentPillarScore(SDate=0,EDate=-17,Frq=FY).value; \
                                   TR.TRESGEmissionsScore(SDate=0,EDate=-17,Frq=FY).value; \
                                   TR.EnvExpenditures(SDate=0,EDate=-17,Frq=FY).value; \
                                   TR.AnalyticEstimatedCO2Total(SDate=0,EDate=-17,Frq=FY).value; \
                                   TR.SocialPillarScore(SDate=0,EDate=-17,Frq=FY).value; \
                                   TR.AnalyticBoardFemale(SDate=0,EDate=-17,Frq=FY).value; \
                                   TR.AnalyticBoardCulturalDiversity(SDate=0,EDate=-17,Frq=FY).value;\
                                   TR.TrainingCostsTotal(SDate=0,EDate=-17,Frq=FY).value;\
                                   '])                                                                                                                                                                                  
ESG_US_data,err

# create a dataframe
df_US_ESG = pd.DataFrame(data=ESG_US_data)


df_US_ESG["Date"] = df_US_ESG["Date"].apply(str)
df_US_ESG['report_year'] = [name[0:4] for name in df_US_ESG['Date']]
df_US_ESG = df_US_ESG.drop(columns=['Date'])

df_US_ESG.to_csv("./B_CSR_scores_calculation_Python/output/4.Refinitiv_ESG_US_04-10-2023.csv")  
df_US_ESG = pd.read_csv("./B_CSR_scores_calculation_Python/output/4.Refinitiv_ESG_US_04-10-2023.csv")  
df_US_ESG = df_US_ESG.drop(columns=['Unnamed: 0'])

######################################################################################################

# merge datasets
df_EU_refinitiv = pd.merge(df_EU_ESG, df_EU_financials, on=['Instrument','report_year'])
df_EU_refinitiv

df_US_refinitiv = pd.merge(df_US_financials, df_US_ESG, on=['Instrument','report_year'])
df_US_refinitiv

dfs =[df_EU_refinitiv, df_US_refinitiv]
df_EU_US_refinitiv = pd.concat(dfs)
df_EU_US_refinitiv

# save df
df_EU_refinitiv.to_csv("./data/pulled/3_csr_refinitiv_api_eu_04-10-2023.csv")  
df_US_refinitiv.to_csv("./data/pulled/3_csr_refinitiv_api_us_04-10-2023.csv")  

df_EU_US_refinitiv.to_csv("./data/pulled/3_csr_refinitiv_api_eu_us_04-10-2023.csv")  



                                 #  
