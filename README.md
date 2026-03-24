# Horizontal Links: Appendix
This repository contains the datasets and the scripts employed in the case studies of the PhD thesis "_Horizontal Links. A view of paradigmatic relations from the Italian lexicon-grammar continuum_". The content of each file is described below, divided by chapter and section, as presented in the thesis.

* [Chapter 3 - Paradigms, in and beyond word-formation: the case of analytic and synthetic psych-predicates](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#chapter-3---paradigms-in-and-beyond-word-formation-the-case-of-analytic-and-synthetic-psych-predicates)
  - [Section 3.2 - Data collection](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#section-32---data-collection)
  - [Section 3.3 - Looking for relational patterns in the paradigm of psych-predicates](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#section-33---looking-for-relational-patterns-in-the-paradigm-of-psych-predicates)
    - [Section 3.3.1 - Cross-table analysis: LVCs and SVs across event types](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#section-331---cross-table-analysis-lvcs-and-svs-across-event-types)
    - [Section 3.3.2 - Network analysis: the relational behaviour of LVCs and SVs](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#section-332---network-analysis-the-relational-behaviour-of-lvcs-and-svs)
  - [Section 3.4 - Differential exponence: the case of causative patterns](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#section-34---differential-exponence-the-case-of-causative-patterns)
  - [Section 3.5 - Overabundance: the division of labour between analytic and synthetic predicates](https://github.com/fla-pi/HorizontalLinks?tab=readme-ov-file#section-35---overabundance-the-division-of-labour-between-analytic-and-synthetic-predicates)
* [Chapter 4: How horizontally linked constructions interact: evaluative constructions of ‘half-quantity’]()
  - [Section 4.2]()
  - [Section 4.3]()
  - [Section 4.5]()
 
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
  This dataset contains all the predicates found for each noun. It is referenced in Section 4.1. Given its format, it is not intended to be used for statistical     analysis (see instead dataset 5), but as a visualization tool. Columns include:

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

## Chapter 4: How horizontally linked constructions interact: evaluative constructions of ‘half-quantity’

### Section 4.2

### Section 4.3

### Section 4.5
