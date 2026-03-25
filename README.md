# Horizontal Links: Appendix
This repository contains the datasets and the scripts employed in the case studies of the PhD thesis "_Horizontal Links. A view of paradigmatic relations from the Italian lexicon-grammar continuum_". The content of each file is described below. Files are grouped by chapter and section, as presented in the thesis.

* [Chapter 3 - Paradigms, in and beyond word-formation: the case of analytic and synthetic psych-predicates](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#chapter-3---paradigms-in-and-beyond-word-formation-the-case-of-analytic-and-synthetic-psych-predicates)
  - [Section 3.2 - Data collection](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#section-32---data-collection)
  - [Section 3.3 - Looking for relational patterns in the paradigm of psych-predicates](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#section-33---looking-for-relational-patterns-in-the-paradigm-of-psych-predicates)
    - [Section 3.3.1 - Cross-table analysis: LVCs and SVs across event types](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#section-331---cross-table-analysis-lvcs-and-svs-across-event-types)
    - [Section 3.3.2 - Network analysis: the relational behaviour of LVCs and SVs](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#section-332---network-analysis-the-relational-behaviour-of-lvcs-and-svs)
  - [Section 3.4 - Differential exponence: the case of causative patterns](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#section-34---differential-exponence-the-case-of-causative-patterns)
  - [Section 3.5 - Overabundance: the division of labour between analytic and synthetic predicates](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#section-35---overabundance-the-division-of-labour-between-analytic-and-synthetic-predicates)
* [Chapter 4: How horizontally linked constructions interact: evaluative constructions of ‘half-quantity’](https://github.com/fla-pi/HorizontalLinks/tree/main?tab=readme-ov-file#chapter-4---how-horizontally-linked-constructions-interact-evaluative-constructions-of-half-quantity)
  - [Section 4.2 - Delimiting the space of polymorphism](https://github.com/fla-pi/HorizontalLinks/tree/main?tab=readme-ov-file#section-42---delimiting-the-space-of-polymorphism)
  - [Section 4.2.3 - The productivity of _semi_-X and _mezzo_ X, between quantity and approximation](https://github.com/fla-pi/HorizontalLinks/tree/main?tab=readme-ov-file#section-423---the-productivity-of-semi-x-and-mezzo-x-between-quantity-and-approximation)
  - [Section 4.3 - Developing polymorphism: the coevolution of evaluative _semi_-X and _mezzo_ X](https://github.com/fla-pi/HorizontalLinks/tree/main?tab=readme-ov-file#section-43---developing-polymorphism-the-coevolution-of-evaluative-semi-x-and-mezzo-x)
  - [Section 4.5 - A closer look at division of constructional labor: the case of adjectives](https://github.com/fla-pi/HorizontalLinks/tree/main?tab=readme-ov-file#section-45---a-closer-look-at-division-of-constructional-labor-the-case-of-adjectives)
 
## Chapter 3 - Paradigms, in and beyond word-formation: the case of analytic and synthetic psych-predicates

### Section 3.2 - Data collection

* [**1_list_psych_nouns.csv**](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.2/1_list_psych_nouns.csv):
  This dataset contains the list of 217 nouns selected from [ItEM (Italian EMotive lexicon) (Passaro et al. 2015)](https://github.com/Unipisa/ItEM) and later integrated with data from the appendix in [Zammuner (1998)](https://doi.org/10.1080/026999398379745). The dataset is referenced in Section 4.1. Columns include: 

  - id: the identifier of the noun

  - source: the source where the noun was collected, namely ItEM or Zammuner (1998)

  - noun: the lemma of the noun

  - marche_uso: usage labels from GRADIT (De Mauro 2007) dictionary, pointing at the frequency of the lemma. The labels in the dataset include, from the most frequent to the least frequent: FO = fundamental; AU = high usage;  AD = highly available; CO = commonly used; LE = literary; TS = technical and special languages.

  - derived: data on the etymology of the noun, extracted from GRADIT. Basic labels: no = underived; denominal; deadjectival; deverbal; compound; from_locution. Labels can be stacked to indicate that a noun is derived from a derived lemma, e.g., deadjectival_deverbal means that the noun is derived from a deverbal adjective. Finally, we preposed the prefix "latin_" to the labels in case the noun is not derived from an italian lemma, but comes from a derived word in latin.

  - selected: whether the noun was selected and included in the final list to create the database (y/n). With reference to "derived" field, we kept all the lemmas apart from deverbal and deadjectival ones, since they would have involved more patterns (e.g., Verb+Adjective LVCs, underived verbs, and so on). We also kept in our list the "latin_" prefixed nouns, since they generally do not have a transparent derivational link to italian verbs and adjectives.

* [**2_list_for_itwac_query.csv**](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.2/2_list_for_itwac_query.csv):
    This dataset was used to list all the possible LVC patterns by crossing the selected nouns and the LVC patterns. Columns include:

    - id: the identifier of the noun

    - noun: the lemma of the noun

    - 10 columns, one for each LVC pattern

* [**3_full_dataset.csv**](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.2/3_full_dataset.csv):
  This dataset contains all the predicates found for each noun. Given its format, it is not intended to be used for statistical analysis, but as a visualization tool. Columns include:

  - noun: the lemma of the noun

  - freq_noun: the frequency of the noun extracted from [ItWaC small](https://bellatrix.sslmit.unibo.it/noske/public/#dashboard?corpname=itwac1)

  - 20 columns, one for each possible predicate. The cell is filled with the predicate only when it was found in GRADIT or ItWaC. The schema used for the column       names was: 

    > TypeOfCxn(sv/lvc)_EventType(stative/causative/inchoative)_Name(process/pattern)

### Section 3.3 - Looking for relational patterns in the paradigm of psych-predicates

#### Section 3.3.1 - Cross-table analysis: LVCs and SVs across event types

* [**1_full_dataset_counts.csv**](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.3/Section3.3.1/1_full_dataset_counts.csv):
  This dataset contains the information on the number of predicates and event types created from the nouns in the list. Columns include:

  - noun: the lemma of the noun

  - freq_noun: the frequency of the noun extracted from ItWaC small

  - n_preds: number of predicates created from the noun

  - n_cells: number of event types (0 to 3) expressed by the predicates created from the noun

  - log_freq: logarithm (base = 10) of the frequency of the noun

  - n_lvcs: number of LVCs created from the noun

  - n_svs: number of SVs created from the noun


#### Section 3.3.2 - Network analysis: the relational behaviour of LVCs and SVs

* [**1_pivot_longer_preds.csv**](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.3/Section3.3.2/1_pivot_longer_preds.csv):
This dataset displays the data from [3_full_dataset.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.2/3_full_dataset.csv) (Section 3.2) in long format, and adds the frequency of the predicates extracted from ItWaC small. Each row corresponds to a predicate. Columns include:

  - noun: the lemma of the noun used to create the predicate

  - cxn: whether the predicate is a SV or a LVC 

  - cxn_spec: the specific morphological process or multiword pattern employed to create the predicate, prefixed by SV or LVC.

  - event_type: the event type expressed by the predicate

  - n: the frequency of the predicate in ItWaC small. Frequencies were manually checked and disambiguated when there was an anticausative verb involving -si, since they are often lemmatized by automatic taggers as their causative counterparts.

* [**2_schema_frequency_info.csv**](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.3/Section3.3.2/2_schema_frequency_info.csv):
This dataset was obtained by adding up the token frequencies of each predicate ([**1_pivot_longer_preds.csv**](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.3/Section3.3.2/1_pivot_longer_preds.csv)) by schema (Section 3.2). Columns include:

  - cxn: the name of the schema

  - n_types: number of preicates formed via that schema

  - n_tokens: cumulative token frequency of the schema (calculated by adding up the token frequencies of all its types)

  - max_n_tokens: maximum token frequency of a type of that schema

  - avg_n_tokens: average token frequency of the types of that schema

  - median_n_tokens: median token frequency of the types of that schema

  - asp_c_type: event type associated to the schema

  - freq_pmw: token frequency per million words in itWac small of the schema
 
* [**3_graph_paradigmatic.csv**](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.3/Section3.3.2/3_graph_paradigmatic.csv):
This dataset contains all pairs of schemas belonging to different event types with at least 1 shared filler. The columns contain:
  - pred1: first schema
  
  - pred2: second schema
   
  - n: number of shared fillers
   
  - aspc1: event type expressed by the first schema
   
  - aspc2: event type expressed by the second schema
 
* [**3_graph_synonymy.csv**](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.3/Section3.3.2/3_graph_synonymy.csv):
This dataset contains all pairs of schemas belonging to the same event type with at least 1 shared filler. The columns contain:
  - pred1: first schema
  
  - pred2: second schema
   
  - n: number of shared fillers
   
  - aspc1: event type expressed by the first schema
   
  - aspc2: event type expressed by the second schema
 
* [4_network_analysis.py](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.3/Section3.3.2/4_network_analysis.py):
  Script for modeling the network, calculating graph metrics and plotting the network.

### Section 3.4 - Differential exponence: the case of causative patterns

* [1_nouns.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.4/1_nouns.csv):
  This dataset is a copy of [**1_pivot_longer_preds.csv**](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.3/Section3.3.2/1_pivot_longer_preds.csv) from Section 3.3.2.

* [2_phonological_annotation.R](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.4/2_phonological_annotation.R):
  Script for the automatic annotation of [1_nouns.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.4/1_nouns.csv), based on the data contained in the phonological Italian lexicon [phonItaliaR](https://github.com/stefanocoretta/phonItaliaR).

* [3_data_phonetics.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.4/3_data_phonetics.csv):
  This dataset contains the phonological annotation of nouns. Note that each row corresponds to a fully specified predicate, and thus is represented as a noun/schema pairing. Thus, the same noun may appear in multiple rows. Columns contain:

  - noun: lemma of the noun
 
  - cxn: schema
 
  - event_type: event type expressed by the predicate
 
  - PhoneSyll: phonemic transcription
 
  - NumPhones: number of phonemes
 
  - SumSylls: number of syllables
    
  - PhonVCV: phonological pattern of the word. V stands for vowel, G for geminate consonant and C for consonant

  - InitialPhoneme: initial phoneme
  
  - InitialSyll: initial syllable
  	
  - SonorityScale: annotation of the sound class of the first phoneme
  
  - SonorityScaleRank: ranking on the sonority scale of the first phoneme, based on its sound class	
  
  - SonoritySimple: annotation of the sound macro-class of the first phoneme, obtained by merging sound classes to three macro-groups: vowels, obstruents and sonorants

  - SonoritySimpleRank: ranking on the sonority scale of the first phoneme, based on its macro-class
 
* [4_psychnouns_ratings.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.4/4_psychnouns_ratings.csv):
This dataset contains the list of nouns employed in psych-predicates, annotated by basic emotion ratings and VAD (valence, arousal and dominance). The ratings were extracted from the emotional lexicon [ELIta](https://github.com/elianadipalma/ELIta). Columns include:

  - noun: the lemma of the noun

  - 8 columns corresponding to basic emotion ratings (joy: anticipation)

  - 3 columns corresponding to VAD ratings

  - 3 colums including valence, intensity and duration ratings extracted from Zammuner (1998), not included in the analysis.

  - 8 columns corresponding to the presence of basic emotions, expressed as binary value (0/1) (see [ELIta](https://github.com/elianadipalma/ELIta))

* [5_create_df_pca.py](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.4/5_create_df_pca.py):
Script for aligning schemas with the ratings of the nouns employed with them.

* [6_data_pca_caus.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.4/6_dataset_pca_caus.csv):
This dataset is the output of [5_create_df_pca.py](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.4/5_create_df_pca.py). It contains the same columns as [4_psychnouns_ratings.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.4/4_psychnouns_ratings.csv), plus 5 additional columns corresponding to the five main causative shemas, specifying whether the noun is employed with that schema or with not (other).

* [7_pca_plutchik.R](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.4/7_pca_plutchik.R):
  Script for performing pca on the nouns, based on basic emotion ratings, and to generate pca plots with average vectors for each schema.

### Section 3.5 - Overabundance: the division of labour between analytic and synthetic predicates

* [1_alternations_dataset](https://github.com/fla-pi/HorizontalLinks/tree/main/Chapter3/Section3.5/1_alternations_dataset.csv):
This dataset includes the occurrences of synonymous sets of SVs and LVCs annotated and analyzed in the mixed effect model (formula and results in the thesis), extracted from [CORIS](https://corpora.ficlit.unibo.it/coris_ita.html), [KIParla](https://search.corpuskiparla.it/corpus/crystal/#dashboard?corpname=KIPARLA) and [LIP](https://www.volip.it/). Columns include:
  - ID: identifier of the occurrence, expressed as: CORIS_n for CORIS data; RCast_n for RadioCast-it data; KIParla_ConversationID for KIParla data; LIP_ConversationID for LIP data.

  - Occurrences: the occurences extracted from the corpora.

  - Noun: the nominal base of the predicate.

  - Cxn: the type of predicate, i.e., whether it is a SV or a LVC: SV; LVC.

  - Process: the process or pattern employed to create the predicate.

  - Verb: the lemma form of the predicate.

  - Event_Type: the event type expressed by the predicate

  - Modification: whether the predicate is modified
    
  - Sem_NonSubjExperiencer: Semantic annotation of the Direct/Indirect Object expressing the Experiencer (for causative predicates)
    
  - Sem_SubjStimulus: Semantic annotation of the Subject expressing the Stimulus (for causative predicates)
    
  - Verb_Form: the verb form of the predicate in the occurrence.
  
  - Time: timeframe when the occurrence was produced. Timeframes are specified in CORIS metadata, and in the publications relative to spoken corpora. They were grouped in three time slices: 1980_2000, 2001_2010, 2011_2021.

  - Corpus: whether the corpus includes Written or Spoken data.

  - Text_genre: text genre or communicative situation where the occurrence was produced. Text genres were extracted from the metedata of the corpora and grouped together in 7 categories: Dialogic_speech = face-to-face (KIParla and LIP) and telephone conversations; Monologic_speech = university lessons (KIParla), public speeches (LIP); Broadcast = radio and TV speech (LIP and RadioCast-it); Fiction_prose = Friction prose in CORIS; Press = Newspapers and Magazines in CORIS; NonFiction_prose = Academic and Legal prose in CORIS; Websites = Ephemera in CORIS.

## Chapter 4 - How horizontally linked constructions interact: evaluative constructions of ‘half-quantity’

### Section 4.2 - Delimiting the space of polymorphism

* [1_excluded_from_query.txt](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.2/1_excluded_from_query.txt): List of words and patterns excluded from the query in CORIS.

* [2_dataset_clean.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.2/2_dataset_clean.csv): This dataset contains all the occurrences of _semi_-X and _mezzo_ X (false positive excluded) retrieved in CORIS. Columns contain:
  
  - CORIS_Year: timeframe when the occurrence was produced. Timeframes are specified in CORIS metadata.
  - Text_genre: text genre to which the occurrence belongs (extracted from CORIS metadata).
  - Text_genre_specific: subtype of the text genre, as specified in CORIS.
  - Type: lemmatized type of the KWIC in the occurrence
  - Cxn: either semi- or mezzo
  - Base: lemma of the filler
  - Pos: part of speech of the filler
  - Function: Broad semantic annotation. Below, we show the equivalence between labels in the dataset and labels in the thesis:
  
      | annotation label                                     | label employed in the thesis        |
    | ---------------------------------------------------- | ----------------------------------- |
    | half_of_a_whole                                      | half of a whole                     |
    | middle_point_position, middle_among_Xs               | median point/value                  |
    | great_part_of                                        | large amount                        |
    | evaluative                                           | approximation                       |
    | idiomatic_lexicalized, not_even_halfX, halfX_&_halfY | idiomatic/opaque/constructionalized |

  - Occurrence: KWIC (enclosed in <>) surrounded by its left and right context

#### Section 4.2.3 - The productivity of _semi_-X and _mezzo_ X, between quantity and approximation

* [1_lexical_productivity.py](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.2/Section4.2.3/1_lexical_productivity.py): Script for calculating lexical productivity measures.

* [2_semantic_prod_optimal_k.py](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.2/Section4.2.3/2_semantic_prod_optimal_k.py): Script for calculating optimal _k_ for clustering on UMAP reduction of the word2vec vectors of the fillers.

* [3_fillers_not_found.txt](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.2/Section4.2.3/3_fillers_not_found.txt): List of fillers not found in the vocabulary of the word2vec model.

* [4_clust_eval_evaluative.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.2/Section4.2.3/4_clust_eval_evaluative.csv): Results for the evalutation metrics for clustering fillers of evaluative constructions. The best _k_ was found by human judgement, by balancing the best scores for the two indices employed. Columns include:
  - n_clusters: number of clusters (_k_) evaluated
  - DBI: Davies-Bouldin Index (the lower, the better)
  - CHI: Calinski-Harabasz Index (the higher, the better)
 
* [4_clust_eval_quantitative.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.2/Section4.2.3/4_clust_eval_evaluative.csv): Results for the evalutation metrics for clustering fillers of quantitative constructions. The best _k_ was found by human judgement, by balancing the best scores for the two indices employed. Columns include:
  - n_clusters: number of clusters (_k_) evaluated
  - DBI: Davies-Bouldin Index (the lower, the better)
  - CHI: Calinski-Harabasz Index (the higher, the better)
 
* [5_semantic_prod_evaluative.py](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.2/Section4.2.3/5_semantic_prod_evaluative.py): Script for clustering fillers of evaluative constructions (_k_ = 12).

* [5_semantic_prod_quantitative.py](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.2/Section4.2.3/5_semantic_prod_evaluative.py): Script for clustering fillers of quantitative constructions (_k_ = 6).

### Section 4.3 - Developing polymorphism: the coevolution of evaluative _semi_-X and _mezzo_ X

* [1_mezzo_full_codit.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.3/1_mezzo_full_codit.csv): This dataset contains the results of the extraction of _mezzo_ X constructions on [CODIT](https://wiki.korpus.cz/doku.php/en:cnk:codit) (including false positives). Columns include:
  - docnumber: document number in CODIT
  - period: period (see CODIT's subdivision) in which the occurrence was produced
  - title: title of the document to which the occurrence belongs
  - genre: text genre, as found in CODIT metadata
  - author: author of the text
  - title2: title of the text to which the occurrence belongs
  - year: year of publication of the text
  - variety: variety of Italian 
  - left: left context
  - kwic
  - right: right context
  - selection: whether the occurrence is considered evaluative (ev), non-evaluative (non_ev) or a false hit (-).
 
* [1_semi_full_codit.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.3/1_semi_full_codit.csv): This dataset contains the results of the extraction of _semi_-X constructions on CODIT (including false positives). Columns include:
  - docnumber: document number in CODIT
  - period: period (see CODIT's subdivision) in which the occurrence was produced
  - title: title of the document to which the occurrence belongs
  - genre: text genre, as found in CODIT metadata
  - author: author of the text
  - title2: title of the text to which the occurrence belongs
  - year: year of publication of the text
  - variety: variety of Italian 
  - left: left context
  - kwic
  - right: right context
  - selection: whether the occurrence is considered evaluative (ev), non-evaluative (non_ev) or a false hit (-).
 
* [2_semi&mezzo_codit.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.3/2_semi%26mezzo_codit.csv): This dataset contains the occurrences of _semi_-X and _mezzo_X annotated as evaluative in CODIT. Columns include:
  - docnumber: document number in CODIT
  - period: period (see CODIT's subdivision) in which the occurrence was produced
  - title: title of the document to which the occurrence belongs
  - genre: text genre, as found in CODIT metadata
  - author: author of the text
  - title2: title of the text to which the occurrence belongs
  - year: year of publication of the text
  - variety: variety of Italian 
  - left: left context
  - kwic
  - right: right context
  - pos_base: part-of-speech of the filler
  - lemma_base: lemma of the filler
  - construction: schema employed (_semi_- or _mezzo_)
  - cent: century in which the occurrence was produced
  - form_base: inflected form of the filler
 
* [3_createfreqlists.py](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.3/3_createfreqlists.py): Script employed to create frequency lists for the lemmas in lemma_base ([2_semi&mezzo_codit.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.3/2_semi%26mezzo_codit.csv)). In particular, for each lemma, we search all possible forms (extracted from [Morph-it!](https://docs.sslmit.unibo.it/doku.php?id=resources:morph-it)) in the training data of [BERToldo](https://github.com/dhfbk/historical-bert), to determine the frequency of individual forms.

* [4_train_historical_w2v.py](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.3/4_train_historical_w2v.py): script employed to train four word2vec models on BERToldo training datasets (one for each partition in the training dataset).

* [5_create_vec_list.py](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.3/5_create_vec_list.py): Script employed to create vectors for the lemmas in the dataset. Lemma vectors are calculated as the average between the vectors of forms of that lemma (see [3_createfreqlists.py](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.3/3_createfreqlists.py)), weighted by the frequency of each individual form.

* [6_umap_plots.py](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.3/6_umap_plots.py): Script for dimensionality reduction of the vectors with UMAP and for creating plots of UMAP-reduced vectors for each century.

* [7_calculate_metrics.py](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.3/7_calculate_metrics.py) : Script employed to calculate metrics of semantic distance and openness/coherence.


### Section 4.5 - A closer look at division of constructional labor: the case of adjectives

* [1_dataset_half_adj.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.5/1_dataset_half_adj.csv): This dataset contains 600 total occurrences of _semi_-Adj and _mezzo_ Adj, randomly sampled from [2_dataset_clean.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.2/2_dataset_clean.csv). Columns include:
  - n: unique identifier of the occurrence
  - CORIS_Year; Text_genre; Text_genre_specific; Type; Cxn; Pos; Occurrence: same annotations found in [2_conditional_inference_tree.R](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.5/2_conditional_inference_tree.R)   
  - Lemma_Base: corresponds to Base in [2_dataset_clean.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.2/2_dataset_clean.csv)
  - 7 columns with annotations not included in the analysis in [2_dataset_clean.csv](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.2/2_dataset_clean.csv):
    - Orthography: orthographic form of the occurrence (bound, hyphenated, unbound)
    - Syllables: orthographic transcription with syllabic segmentation of the lemma of the filler
    - SyllLength: n. of syllables of the lemma of the filler
    - MorphCat: morphological information on the lemma of the filler (conversion from a participle, simplex and complex word)
    - Function: syntactic function of the occurrence (attributive/appositive, predicative, secundary predicate)
    - SemClass: (tentative) manual semantic annotation of the lemma of the filler, loosely based on semantic classes for adjectives in [German WordNet](https://uni-tuebingen.de/en/faculties/faculty-of-humanities/departments/modern-languages/department-of-linguistics/chairs/general-and-computational-linguistics/ressources/lexica/germanet/description/adjectives/)
    - Approximation_Output2: recoding of Approximation_Output
  - 2 colums included in the analysis in [2_conditional_inference_tree.R](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.5/2_conditional_inference_tree.R):
    - ScalePoint_Base: type of scale point denoted by the lemma of the filler
    - Approximation_Output: the type of approximating sub-function of the occurrence

* [2_conditional_inference_tree.R](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter4/Section4.5/2_conditional_inference_tree.R): Script for fitting the Conditional Inference Trees on type and token counts. The scripts include commented lines with the outputs and the evaluation metrics of the two trees.
