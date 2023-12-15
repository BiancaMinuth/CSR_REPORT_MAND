# --- Header -------------------------------------------------------------------
# "CSR SCORES" analysis and display 
#
# CSR Project 2022
# ------------------------------------------------------------------------------

# select libraries
#install.packages("tidyverse", type="binary")
library(tidyverse) # for most data handling tasks
library(ggplot2) # producing graphs
library(stargazer) # producing results tables
library(AER) # access to HS robust SE
library(sandwich) # cluster robust SE
library(dplyr) # data preparation and selection
library(lmtest) # linear regression test
library(coefplot) # create coefficient plots
library(plm)

#library(tidyr)
#library(plyr)
#library(factoextra)
#library(lfe)
#library(palmerpenguins)
#library(ExPanDaR)
#library(corrplot)
#library(rgl)
#library(plot3D)

# set directory 
setwd("C:/Dokumente/1 PhD Programm/Research Projects/wp_2")

# --- OPEN SAMPLE BASE ---------------------------------------------------------

csr_mand_sample <- readRDS("data/generated/csr_ref_data.rds")

# --- PREPARE DATA FOR DIFF-IN-DIFF --------------------------------------------

# make sure data if a df
csr_mand_sample <- as.data.frame(csr_mand_sample)

# create sample slits
csr_mand_sample <- csr_mand_sample %>%
  mutate(
    ESG_low = ESG <=  0.612,
    #  ESG_med = ESG > 0.653871 & ESG <= 0.78106,
    ESG_high = ESG >  0.612,
    ESG_low_d = ifelse(ESG <=  0.612, 1, 0),
    #    ESG_med_d = ifelse(ESG > 0.653871 & ESG <= 0.78106, 1, 0),
    ESG_high_d = ifelse(ESG >  0.612, 1, 0)
  )

sample_ESG_high <- csr_mand_sample %>%
  filter(ESG_high_d > 0) 

sample_ESG_low <- csr_mand_sample %>%
  filter(ESG_low_d > 0) 

# create treatment and event dummies
data <- csr_mand_sample %>%
  mutate(
    w = ifelse((eu_dummy == 1) & (fiscal_year >= 2014), 1, 0),
    d = ifelse(eu_dummy == 1, 'treated', 'control'),
    f2014 = ifelse(fiscal_year == 2014, 1, 0),
    f2015 = ifelse(fiscal_year == 2015, 1, 0),
    post = ifelse(fiscal_year >= 2014, 1, 0),
  #  fiscal_year = as.factor(fiscal_year),
    w = as.factor(w),
    ISIN = as.factor(ISIN)
   ) %>%
  filter(!is.na(ESG))

pdata <- pdata.frame(data, index = c("ISIN", "fiscal_year"))
is.pbalanced(csr_mand_sample)

# --- EMPIRICAL ANALYSIS -------------------------------------------------------

# (1) Estimate Restricted Model

mod1 <- lm(ESG ~ ISIN + fiscal_year + w, data = pdata)
mod1_robst_se <- sqrt(diag(vcovHC(mod1, type= "HC1")))
mod1_cr_se <- sqrt(diag(vcovCL(mod1, cluster = ~ ISIN)))

stargazer(mod1, keep='w', type='text', se=list(mod1_robst_se), digits=6,
          notes='HS Robust Clustered SE in parenthesis' )

# (2) Estimate Unrestricted Model

pdata <- pdata  %>%
  mutate(
    tr2015 = (fiscal_year=='2015')*(d=='treated'),
    tr2013 = (fiscal_year=='2013')*(d=='treated'),
    tr2014 = (fiscal_year=='2014')*(d=='treated')
  )

mod2 <- lm(optimism~ISIN+fiscal_year+tr2015+tr2013+tr2014+ln_at+leverage+roa+size, data=pdata)
mod2_cr_se <- sqrt(diag(vcovCL(mod2, cluster = ~ ISIN)))
coef_keep = c("fiscal_year", "tr2015", "tr2013", "tr2014")
stargazer(mod2, keep= coef_keep, type='text', se=list(mod2_cr_se), digits=6,
          notes='HS Robust Clustered SE in parenthesis' )

################################################################################
## TABLE 1: SAMPLE COMPOSITION ##
################################################################################

#ExPanD(CSR_wacc_sample_2)
count(CSR_scores_sample$fiscal_year)
tab_1 <- data.frame(Eurpean_CSR_Reports=c("Asset4_data", "Collected_reports",
                                          "-  Missing_values", "TOTAL"),
                    CSR_reports=c(9865, 3031, -960, 2071))

sample_df


################################################################################
## TABLE 2: DESCRIPTIVE STATISTICS ##
################################################################################

# table for r markdown
CSR_des <- as.data.frame(csr_mand_sample)
tab_des_sum <- summary(CSR_des)
tab_des_sum
# table to display descriptive statistics with rstudio
tab_des <- stargazer(CSR_des, type = "text", title = "Descriptive Statistics", 
                     summary.stat = c("n", "min", "p25", "median", "p75", "max", "mean", "sd"),
                     out = "des_stat.txt")

# table for laex 
#tab_desc_stat <- prepare_descriptive_table(CSR_sample_des)

#ExPanD(CSR_scores)
#count(CSR_scores$country)

################################################################################
## TABLE 3: DESCRIPTIVE STATISTICS ##
################################################################################

# --- DISPLAY DATA -------------------------------------------------------------
################################################################################
## FIGURE 1: ESG TREND ##
################################################################################

# calculate ESG means per fiscal year
CSR_ESG_mean <- csr_mand_sample %>%
  group_by(fiscal_year, eu_dummy) %>%
  filter(fiscal_year > 2010) %>%
  summarise_at(vars(ESG), 
               funs(median(., na.rm=TRUE)))

CSR_ESG_mean <- sample_ESG_low %>%
  filter(fiscal_year > 2010) %>%
  group_by(fiscal_year, eu_dummy) %>%
  summarise_at(vars(ESG), 
               funs(median(., na.rm=TRUE)))


fig_ESG_trend_1 <- list(ggplot(CSR_ESG_mean, aes( x = fiscal_year, 
                                                  y = ESG)) +
                          geom_line(aes(color = factor(eu_dummy))) 
                        + geom_vline(xintercept = 2014) + geom_vline(xintercept = 2017)) 

fig_ESG_trend_1

# Plot ESG means over year per region in separ. boxes
fig_ESG_trend_2 <- ggplot(data = CSR_ESG_mean, 
                          mapping = aes(x = fiscal_year, y = ESG, color = eu_dummy)) +
  geom_line() +
  facet_wrap(facets =  vars(eu_dummy)) +
  ggtitle("Plot of ESG over Fiscal Years") +
  xlab("Fiscal Year") + ylab("ESG Mean") +  geom_vline(xintercept = 2017)
fig_ESG_trend_2


################################################################################
## FIGURE 2: SENTIMENT TREND ##
################################################################################

# Calculate sentiment means per fiscal year
CSR_pos_mean <- csr_mand_sample %>%
  group_by(fiscal_year, eu_dummy) %>%
  filter(fiscal_year > 2010) %>%
  summarise_at(vars(number_of_words), 
               funs(median(., na.rm=TRUE)))

fig_sentim_trend_1 <- list(ggplot(CSR_pos_mean, aes( x = fiscal_year, 
                                                  y = number_of_words)) +
                          geom_line(aes(color = factor(eu_dummy))) 
                        + geom_vline(xintercept = 2014) + geom_vline(xintercept = 2017)) 

fig_sentim_trend_1

# Plot ESG sentiment over year per region in separ. boxes
fig_ESG_trend_2 <- ggplot(data = CSR_ESG_mean, 
                          mapping = aes(x = fiscal_year, y = ESG, color = eu_dummy)) +
  geom_line() +
  facet_wrap(facets =  vars(eu_dummy)) +
  ggtitle("Plot of Negativity over Fiscal Years") +
  xlab("Fiscal Year") + ylab("Negativity Median") +  geom_vline(xintercept = 2017)
fig_ESG_trend_2




CSR_pos_mean <- csr_mand_sample %>%
  filter(fiscal_year > 2010) %>%
  filter(ESG_low_d > 0) %>%
  group_by(fiscal_year, eu_dummy) %>%
    summarise_at(vars(optimism), 
               funs(median(., na.rm=TRUE)))

fig_sentim_trend_1 <- list(ggplot(CSR_pos_mean, aes( x = fiscal_year, 
                                                     y = optimism)) +
                             geom_line(aes(color = factor(eu_dummy))) 
                           + geom_vline(xintercept = 2014) + geom_vline(xintercept = 2017)) 

fig_sentim_trend_1


lubridate::ymd():
  
library(tidyverse)
library(lubridate)
# your data
CSR_pos_mean <- csr_mand_sample %>% 
  mutate(x = fiscal_year) %>%
  ggplot(aes(x = x, y = pos_sentim, colour = us_dummy)) +
  geom_line()


# create df with mean pos_sentiment
CSR_pos_mean <- csr_mand_sample %>%
  filter(fiscal_year > 2010) %>%
  group_by(fiscal_year, us_dummy) %>%
  summarise_at(vars(pos_sentim), 
  funs(mean(., na.rm=TRUE)))
CSR_pos_mean














CSR_wacc_mean
fig_hist <- hist(CSR_scores_sample$perc_positive)

fig_1 <- ggplot(CSR_pos_mean, aes(fiscal_year)) + # basic graphical object
  geom_line(aes(y=perc_positive), colour="cornflowerblue", size=0.70) +  # forth layer
  xlab("Fiscal Year") + ylab("Optimism")
fig_1

fig_2 <- ggplot(CSR_wacc_mean, aes(fiscal_year)) + # basic graphical object
  geom_line(aes(y=perc_negative), colour="cornflowerblue", size=0.65)   # forth layer
# xlab("Fiscal Year") + ylab("WACC")
fig_2

fig_tone_ESG <- ggplot(CSR_sample, aes(x = optimism, 
                                            y = ESG)) + 
  geom_point() + geom_smooth(method = "lm", se = FALSE)

fig_tone_ESG


fig_1 <- ggplot(CSR_scores, aes(x=fiscal_year)) +
  geom_histogram(aes(color = factor(report_type)), binwidth=1)
fig_1

# Plot percentage of negativity over fiscal year
fig_2 <- ggplot(CSR_scores, aes(x=ESG, y=pos_sentim)) +
  geom_point() 
fig_2

# Plot percentage of positivity over fiscal year
fig_3 <- ggplot(CSR_scores, aes(x=esg_score, y=perc_negative)) +
  geom_point() 
fig_3

# Plot percentage of positive words median over year per country in separ. boxes
plot_pos_year <- ggplot(data = CSR_pos_mean, 
                       mapping = aes(x = fiscal_year,
                       y = pos_sentim, 
                       color = NAICS_code)) +
  geom_line() +
  facet_wrap(facets =  vars(NAICS_name)) +
  ggtitle("Plot of Positivity over Fiscal Years") +
  xlab("Fiscal Year") + ylab("Positivity Median")
fig_8 <- plot_pos_year +   geom_vline(xintercept = 2020)
fig_8

# Plot percentage of negativity over fiscal year
fig_2 <- ggplot(CSR_scores_sample, aes(x=fiscal_year, y=perc_positive)) +
  geom_point() 
fig_2


# --- SAVE DATA -------------------------------------------------------------

write.csv(CSR_scores, "data\\generated\\CSR_scores_full_sample_04-10-2023.csv", row.names=TRUE)
#write.csv(CSR_scores_sample, "output\\CSR_scores_wacc_sample_new.csv", row.names=TRUE)
