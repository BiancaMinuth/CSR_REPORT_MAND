# Install required packages if not already installed
if (!require("tm")) install.packages("tm", dependencies=TRUE)
if (!require("topicmodels")) install.packages("topicmodels", dependencies=TRUE)
library(tm)
library(topicmodels)
#install.packages("tidytext")
library(tidytext)
library(ggplot2)
library(dplyr)
#install.packages(c("tm", "topicmodels", "ggplot2"))

# Define paths

file_path <- "C:\\Dokumente\\1 PhD Programm\\Research Projects\\wp_2\\data\\eu_before_reg"
folder_path <- "C:\\Dokumente\\1 PhD Programm\\Research Projects\\wp_2\\data\\eu_before_reg"

# Function to read all reports from a folder
read_reports <- function(folder_path) {
  # Get the list of file paths in the folder
  file_paths <- list.files(folder_path, full.names = TRUE)
  # Read text from each file
  reports <- sapply(file_paths, function(file_path) {
    text <- tolower(readLines(file_path, warn = FALSE))
    return(paste(text, collapse = " "))
  })
  # Return the vector of reports
  return(reports)
}
all_reports <- read_reports(folder_path)

# ----------------------------------------------------------------------------------
# Files ante

folder_path_ante <- "C:\\Users\\bianc\\AppData\\Local\\Programs\\Python\\Python39\\CSR_reports_wp_2\\A_PDF_convert_Python\\data_EUROSTOXX_ex"
file_path_ex <- "C:\\Users\\bianc\\AppData\\Local\\Programs\\Python\\Python39\\CSR_reports_wp_2\\A_PDF_convert_Python\\data_EUROSTOXX_ex"

# Function to read all reports from a folder
read_reports_ex <- function(folder_path_ex) {
  # Get the list of file paths in the folder
  file_paths_ex <- list.files(folder_path_ex, full.names = TRUE)
  # Read text from each file
  reports_ex <- sapply(file_paths_ex, function(file_path_ex) {
    text_ex <- tolower(readLines(file_path_ex, warn = FALSE))
    return(paste(text_ex, collapse = " "))
  })
  # Return the vector of reports
  return(reports_ex)
}
all_reports_ex <- read_reports_ex(folder_path_ex)

# ----------------------------------------------------------------------------------
# Files post

folder_path_post <- "C:\\Users\\bianc\\AppData\\Local\\Programs\\Python\\Python39\\CSR_reports_wp_2\\A_PDF_convert_Python\\data_EUROSTOXX_post"
file_path_post <- "C:\\Users\\bianc\\AppData\\Local\\Programs\\Python\\Python39\\CSR_reports_wp_2\\A_PDF_convert_Python\\data_EUROSTOXX_post"

# Function to read all reports from a folder
read_reports_post <- function(folder_path_post) {
  # Get the list of file paths in the folder
  file_paths_post <- list.files(folder_path_post, full.names = TRUE)
  # Read text from each file
  reports_post <- sapply(file_paths_post, function(file_path_post) {
    text_post <- tolower(readLines(file_path_post, warn = FALSE))
    return(paste(text_post, collapse = " "))
  })
  # Return the vector of reports
  return(reports_post)
}
all_reports_post <- read_reports_post(folder_path_post)

# ----------------------------------------------------------------------------------

# Create a corpus
corpus <- Corpus(VectorSource(all_reports))
#corpus <- Corpus(VectorSource(all_reports))

# Preprocess the corpus
corpus <- tm_map(corpus, content_transformer(tolower)) #transform the content of a text corpus to lowercase.
corpus <- tm_map(corpus, removePunctuation) #remove punctuation from each document in the corpus
corpus <- tm_map(corpus, removeNumbers) #remove numbers from each document in the corpus
corpus <- tm_map(corpus, removeWords, stopwords("english")) #remove english stopwords from each document in the corpus
corpus <- tm_map(corpus, stripWhitespace) #remove leading, trailing, and extra whitespaces from the text in a corpus

dtm <- DocumentTermMatrix(corpus)
dtm

# Create an LDA model
lda_model <- LDA(dtm, k = 5)  # Adjust the number of topics (k) as needed

top_words <- terms(lda_model, 15)  # Adjust the number of top words as needed
print(top_words)

# Print the topic distribution for each document
doc_topics <- tidy(lda_model, matrix = "beta")
print(doc_topics)

# Fit an LDA model
lda_model <- LDA(mat, k = 3, control = list(seed = 1234))

# Visualize the topics
lda_vis <- createJSON(lda_model, dtm)
serVis(lda_vis)

# Extract topic distribution for each document
topic_distribution <- as.data.frame(lda_model@gamma)
colnames(topic_distribution) <- paste0("Topic_", 1:num_topics)
print(topic_distribution)

ap_top_terms <- doc_topics %>%
  group_by(topic) %>%
  slice_max(beta, n = 10) %>% 
  ungroup() %>%
  arrange(topic, -beta)

ap_top_terms %>%
  mutate(term = reorder_within(term, beta, topic)) %>%
  ggplot(aes(beta, term, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  scale_y_reordered()

###############################################################################

# Function to apply LDA to reports over time
apply_lda_over_time <- function(report_data, num_topics = 5) {
  # Preprocess the reports
  preprocess_reports <- function(reports) {
    corpus <- Corpus(VectorSource(reports))
    corpus <- tm_map(corpus, content_transformer(tolower))
    corpus <- tm_map(corpus, removePunctuation)
    corpus <- tm_map(corpus, removeNumbers)
    corpus <- tm_map(corpus, removeWords, stopwords("english"))
    corpus <- tm_map(corpus, stripWhitespace)
    dtm <- DocumentTermMatrix(corpus)
    return(dtm)
  }
  
  # Apply LDA for each time period
  lda_models <- lapply(report_data, function(reports) {
    dtm <- preprocess_reports(reports)
    return(LDA(dtm, k = num_topics))
  })
  
  # Print top words for each topic in each time period
  for (i in seq_along(lda_models)) {
    cat("Time Period", i, "\n")
    top_words <- terms(lda_models[[i]], 5)  # Adjust the number of top words as needed
    print(top_words)
    cat("\n")
  }
  # Print the topic distribution for each document in each time period
  for (i in seq_along(lda_models)) {
    cat("Time Period", i, "\n")
    doc_topics <- tidy(lda_models[[i]], matrix = "beta")
    print(doc_topics)
    cat("\n")
  }
}
  
# Create a list of reports over time (replace this with your actual data structure)
time_series_reports <- list(
  reports_1 = all_reports_ex,
  reports_2 = all_reports_post
)

# Set the number of topics
num_topics <- 5

# Apply LDA over time
apply_lda_over_time(time_series_reports, num_topics)

# Create an LDA model
lda_model <- LDA(all_reports_ex, k = 5)  # Adjust the number of topics (k) as needed
top_words <- terms(lda_model, 5)  # Adjust the number of top words as needed
print(top_words)

# Extract topic distribution for each document
topic_distribution <- as.data.frame(lda_model@gamma)
colnames(topic_distribution) <- paste0("Topic_", 1:num_topics)
print(topic_distribution)

ap_top_terms <- doc_topics %>%
  group_by(topic) %>%
  slice_max(beta, n = 10) %>% 
  ungroup() %>%
  arrange(topic, -beta)

ap_top_terms %>%
  mutate(term = reorder_within(term, beta, topic)) %>%
  ggplot(aes(beta, term, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  scale_y_reordered()

doc_topics <- as.data.frame(topics(lda_model))

# Visualize the main topic distribution
ggplot(doc_topics, aes(x = as.factor(row.names(doc_topics)), y = Freq, fill = as.factor(topic))) +
  geom_bar(stat = "identity") +
  labs(title = "Main Topic Distribution", x = "Document", y = "Frequency") +
  theme_minimal()


#cosine similarity
library(lsa)
library(SnowballC)

cosine(lda_matrix)
lda_matrix <- posterior(lda_model)$topics
cosine_similarity <- proxy::proxy_dist(lda_matrix, lda_matrix, method = "cosine")
print(cosine_similarity)
#Structural Topic Model
