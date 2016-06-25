Synopsis
====

hbs-twitter-space -- Experiments on spatial distribution of linguistic variables on 
Twitter for Croatian, Bosnian and Serbian. 


Files
====

extract_variables.py -- extracts specific linguistic variables present in Croatian, Bosnian, Serbian and Montenegrinian
varieties presented in Twitter corpus (hrsrTweets.gz). It outputs the Twitter corpus annotated according the presence
of specific linguistics variables in each tweet.


hrsrTweets.gz -- Twitter corpus (input). It contains metainformation about:
* tweet id
* user
* time
* "guessed" tweet language
* longitude
* latitude
* tweet

hrsrTweets.var.gz -- Twitter corpus with annotated features for each tweet (output)

custom-lexicons/ -- contains customized lexicons needed for extraction of linguistic variables

* diftong-v-lexicon.gz -- words having eu/ev or au/av opposition and their labels
* hdrop-lexicon.gz -- words having h/h-drop opposition at the beginning of words and their labels
* kh-lexicon.gz -- words containing k/h opposition at the beginning of words and their labels
* rdrop-lexicon.gz -- words having h/h-drop opposition at the end of words and their labels
* st-c-lexicon.gz -- words containing št/ć opposition and their labels
* yat-lexicon.gz -- words with e and (i)je yat-reflex and their labels
* ch-lexicon.gz -- words containing č and/or ć and their lables
* genitiv-og-eg-lexicon.gz -- adjectives, pronouns and numeralia in masc/neutr sg. ending with -og/eg
* hr-months.gz -- Croatian months (siječanj, veljača, ...)
* int-months.gz -- international months (januar, februar, ...)
* ir-is-lexicon.gz -- stems of verbs ending with -isati/irati
* ir-ov-lexicon.gz -- stems of verbs ending with -ovati/irati
* verbs-inf-lexicon.gz -- verbs in infinitive
* verbs-lexicon.gz -- verbs
* verbs-pres-lexicon.gz -- verbs in presens
* verbs-vmf-lexicon.gz -- verbs in synthetic future tense


scripts/ -- contains scripts for extracting customized lexicons

* extract-diff-lexicons.py -- extracts customized lexicons for discriminative features (either "HR" or "SR")
* extract-ind-lexicons.py -- extracts customized lexicons for non-discriminative features (list may contain same items for "SR" and "HR")

evaluation/ -- contains evaluation tables for each linguistic variable extracted with extract_variables.py

lang-id/ -- contains manually annotated tweets according to their language (Croatian/Bosnian/Serbian/Montenegrinian)


Calling the scripts
====

For extracting the linguistic variables:

* $ python extract-variables.py

For creating customized lexicons:

* $ python extract-diff-lexicons.py
* $ python extract-ind-lexicons.py


Contact
====

scopes.reldi@gmail.com



