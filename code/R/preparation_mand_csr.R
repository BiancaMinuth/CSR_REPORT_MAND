# --- Header -------------------------------------------------------------------
## WORKING PAPER 2: MANDATORY CSR REPORTING ##
## DATA PREPARATION ##
# ------------------------------------------------------------------------------

# select libraries
library(readr)
library(dplyr)
library(DescTools)

# set directory 
setwd("C:/Dokumente/1 PhD Programm/Research Projects/wp_2")

# --- OPEN DATA BASE -----------------------------------------------------------

## OPEN

#open data
df_csr <- read_csv(
  'data/generated/2_csr_scores_prep_06-12-2023.csv',
  col_types = cols() 
)

#open data
df_refinitiv <- read_csv(
  'data/pulled/4_refinitiv_prep_04-10-2023.csv', 
  col_types = cols()
)

# --- PREPARATION --------------------------------------------------------------

# change variables to numeric
df_refinitiv <- df_refinitiv %>%
  mutate(fiscal_year = as.numeric(fiscal_year),
         ni_m = as.numeric(ni_m),
         at_m = as.numeric(debt_m),
         lt_m = as.numeric(lt_m),
         beta = as.numeric(beta),
         market_cap_m =as.numeric(market_cap_m),
         esg_score = as.numeric(ESG_score),
         #     esg_comb_score = as.numeric(ESG_comb_score),
         #     esg_contro_score = as.numeric(ESG_contro_score),
         #      env_innov_score = as.numeric(Env_innov_score),
         #     env_prod_score = as.numeric(Env_prod_score),
         board_gen_div_score = as.numeric(board_gen_div_score),
  )

# change variables to numeric and filter only CSR reports
df_csr <- df_csr %>%
  mutate(fiscal_year = as.numeric(fiscal_year))
    #%>%
#  filter(report_type == 1)

# merge dfs
csr_refinitiv_merge <- df_refinitiv %>%
  left_join(df_csr, by = c("ISIN", "fiscal_year"))

# prepare the variables  
csr_refinitiv <- csr_refinitiv_merge %>%
 # filter(report_type == 1 
#  ) %>%
  mutate(
    ln_at = log(at_m),
    roa = ni_m/at_m,
    size = log(market_cap_m),
    market_book = (market_cap_m+lt_m)/at_m,
    ln_market_book = log(market_book),
    sales = rev_m,
    ln_sales = log(sales),
    loss = ni_m < 0,
    equity_m = debt_m-lt_m,
    leverage = lt_m/equity_m,
    debt_assets = lt_m/at_m, 
    pos_sentim = perc_positive/100,
    neg_sentim = perc_negative/100,
    pos_words = pos_sentim*number_of_words,
    neg_words = neg_sentim*number_of_words,
    optimism = (pos_words-neg_words)/(number_of_words),
    neg_avoid = (100-perc_negative)/100,
    uncer_sentim = perc_uncertainty/100,
    constr_sentim = perc_constraining/100,
    litig_sentim = perc_litigious/100, 
    ESG = esg_score/100,
    ln_words = log(1+number_of_words),
    env_score = Env_pillar_score/100,
    social_score = social_pillar_score/100,
    us_dummy = ifelse(country == 'United States of America', 1, 0),
    eu_dummy = ifelse(country != 'United States of America', 1, 0)
  ) %>%
  select(
    Instrument, ISIN, comp_name, fiscal_year, country, 
    report_type,   
    neg_sentim, pos_sentim, optimism, neg_avoid, uncer_sentim, constr_sentim, 
    litig_sentim, 
    number_of_words, file_size, No_of_alphabetic, No_of_digits, No_of_numbers, 
    avg_No_of_syllables_per_word, avg_word_length, vocabulary,  
    at_m, ln_at, lt_m, equity_m, debt_m, ni_m, sales, ln_sales, market_cap_m, roa, 
    size, market_book, ln_market_book, loss, leverage, debt_assets,
    ESG, env_score, emissions_score, social_score, board_gen_div_score,
# esg_comb_score, esg_contro_score, env_innov_score, env_prod_score, 
# board_fem, 
    NAICS_code, NAICS_name,
    us_dummy, eu_dummy
  )
  #%>%
#  filter(!is.na(report_type)
 # ) 

# select the variables within the sample  
csr_ref_sample <- csr_refinitiv %>%
  select(
    ISIN, comp_name, fiscal_year,  
    neg_sentim, pos_sentim, optimism, neg_avoid, uncer_sentim, constr_sentim, 
    litig_sentim,
    file_size, number_of_words, avg_word_length, avg_No_of_syllables_per_word, 
    vocabulary, 
    at_m, market_cap_m, ln_at, size, ni_m, roa, leverage, 
    ESG, env_score, emissions_score, social_score, board_gen_div_score,
    country, NAICS_code, NAICS_name, us_dummy, eu_dummy)

# check for outliers
#CSR_scores_outlier <- treat_outliers(CSR_scores, by = "fiscal_year")
#CSR_scores_outlier

# winsorise selected variables at p = 0.01 and 0.99
wins_vars <- function(x, pct_level = 0.01){
  if(is.numeric(x)){
    Winsorize(x, probs = c(pct_level, 1-pct_level), na.rm = T)
  } else {x}
}
csr_ref_sample <- bind_cols(
  lapply(csr_ref_sample, wins_vars))



# --- SAVE DATA  ---------------------------------------------------------------

save(
  "csr_ref_sample",
  file = "output/csr_ref_data.rda"
)

saveRDS(csr_ref_sample, "data/generated/csr_ref_data.rds")

















