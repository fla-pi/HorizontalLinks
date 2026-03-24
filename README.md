# Horizontal Links: Appendix
This repository contains the datasets and the scripts employed in the case studies of the PhD thesis "_Horizontal Links. A view of paradigmatic relations from the Italian lexicon-grammar continuum_". The content of each file is described below, divided by chapter and section, as presented in the thesis.

## Chapter 3: Paradigms, in and beyond word-formation: the case of analytic and synthetic psych-predicates

### Section 3.2

* [**1_list_psych_nouns.csv**](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.2/1_list_psych_nouns.csv):
  This dataset contains the list of 217 nouns selected from ItEM (Italian EMotive lexicon) (Passaro et al. 2015) and later integrated with data from the appendix     in Zmmuner (1998). The dataset is referenced in Section 4.1. Columns include: 

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

* [**3_full_dataset.csv**](https://github.com/fla-pi/HorizontalLinks/blob/main/Chapter3/Section3.2/3_full_dataset.csv)
  This dataset contains all the predicates found for each noun. It is referenced in Section 4.1. Given its format, it is not intended to be used for statistical     analysis (see instead dataset 5), but as a visualization tool. Columns include:

  - noun: the lemma of the noun

  - freq_noun: the frequency of the noun extracted from ItWaC small

  - 20 columns, one for each possible predicate. The cell is filled with the predicate only when it was found in GRADIT or ItWaC. The schema used for the column       names was: 

    > TypeOfCxn(sv/lvc)_EventType(stative/causative/inchoative)_Name(process/pattern)

### Section 3.3

#### Section 3.3.1

#### Section 3.3.2

### Section 3.4

### Section 3.5

## Chapter 4: How horizontally linked constructions interact: evaluative constructions of ‘half-quantity’

### Section 4.2

### Section 4.3

### Section 4.5
