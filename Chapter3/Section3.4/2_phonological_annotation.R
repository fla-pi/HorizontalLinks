library(tidyverse)
library(phonItaliaR)

data("phonitalia")


nounlist <- read.csv("1_nouns.csv", sep = ";", header = T)


phon_annotate <- function(main_df, reference_df) {
  # Merge dataframes
  merged_df <- merge(main_df, reference_df[, c("word", "PhoneSyll", "NumPhones", "SumSylls", "PhonVCV")], 
                     by.x = "noun", by.y = "word", all.x = TRUE)
  
  # Estract Initial Phoneme
  merged_df$InitialPhoneme <- substr(merged_df$PhoneSyll, 1, 1)
  
  # Count number n of phonemes in the first syllable
  merged_df$NumLettersBeforeDot <- sapply(merged_df$PhoneSyll, function(x) {
    if (is.na(x)) return(NA)
    split_x <- unlist(strsplit(x, "\\.")) 
    nchar(split_x[1]) 
  })
  
  # Extract n phonemes from PhonVCV
  merged_df$InitialSyll <- mapply(function(phonvcv, count) {
    if (is.na(phonvcv) | is.na(count)) return(NA)
    substr(phonvcv, 1, count)
  }, merged_df$PhonVCV, merged_df$NumLettersBeforeDot)
  
  merged_df <- distinct(merged_df)

 # map articulation manner on InitialPhoneme
  sonority_map <- list(
    plosive = c("t", "k", "p", "d", "G", "b"),
    affricate = c("g", "c", "Z", "z"),
    fricative = c("f", "v", "s", "S"),
    nasal = c("m", "n"),
    liquid = c("l", "r"),
    semiconsonant = c("w", "j"),
    vowel = c("a", "i", "o", "e", "u", "E", "O")
  )
  
 
  get_sonority <- function(letter) {
    for (category in names(sonority_map)) {
      if (letter %in% sonority_map[[category]]) {
        return(category)
      }
    }
    return(NA)
  }
  
  
  merged_df$SonorityScale <- sapply(merged_df$InitialPhoneme, get_sonority)
  
  #check print
  cat("nrows merged_df:", nrow(merged_df), "\n")
  cat("SonorityScale length:", length(merged_df$SonorityScale), "\n")
  

  
  # Remap articulation manner as sonority scale
  sonority_rank_map <- list(
    plosive = 7, affricate = 6, fricative = 5, nasal = 4, 
    liquid = 3, semiconsonant = 2, vowel = 1
  )
  
  sonority_simple_rank_map <- list(
    plosive = 3, affricate = 3, fricative = 3,
    nasal = 2, liquid = 2, semiconsonant = 2,
    vowel = 1
  )
  
  sonority_simple_map <- list(
    plosive = "obstruent", affricate = "obstruent", fricative = "obstruent",
    nasal = "sonorant", liquid = "sonorant", semiconsonant = "sonorant",
    vowel = "vowel"
  )
  
  unique_values <- unique(merged_df$SonorityScale)
  unmatched_values <- unique_values[!unique_values %in% names(sonority_rank_map)]
  print(unmatched_values)
 
  merged_df$SonorityScaleRank <- sapply(merged_df$SonorityScale, function(x) {
    if (!is.na(x) && x %in% names(sonority_rank_map)) {
      return(sonority_rank_map[[x]])
    } else {
      return(NA)
    }
  })
  
  merged_df$SonoritySimpleRank <- sapply(merged_df$SonorityScale, function(x) {
    if (!is.na(x) && x %in% names(sonority_simple_rank_map)) {
      return(sonority_simple_rank_map[[x]])
    } else {
      return(NA)
    }
  })
  
  merged_df$SonoritySimple <- sapply(merged_df$SonorityScale, function(x) {
    if (!is.na(x) && x %in% names(sonority_simple_map)) {
      return(sonority_simple_map[[x]])
    } else {
      return(NA)
    }
  })
  
  merged_df$SonorityScaleRank <- unlist(merged_df$SonorityScaleRank, use.names = FALSE)
  merged_df$SonoritySimpleRank <- unlist(merged_df$SonoritySimpleRank, use.names = FALSE)
  merged_df$SonoritySimple <-unlist(merged_df$SonoritySimple, use.names = FALSE)

  merged_df$NumLettersBeforeDot <- NULL
  write.csv(merged_df, "3_data_phonetics.csv",  row.names = FALSE)
  return(merged_df)
}

phon_annotate(nounlist, phonitalia)
