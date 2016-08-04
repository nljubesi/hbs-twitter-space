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

* hdrop-lexicon.gz -- words having h/h-drop opposition 
* kh-lexicon.gz -- words containing k/h opposition 
* rdrop-lexicon.gz -- words having r/r-drop opposition
* hdrop-lexicon.gz -- words having h/h-drop opposition
* st-c-lexicon.gz -- words containing št/ć opposition 
* yat-lexicon.gz -- words with e and (i)je yat-reflex 
* ch-lexicon.gz -- words containing č and/or ć and their lables
* genitiv-og-eg-lexicon.gz -- adjectives and numeralia in masc/neutr sg. ending with -og/eg
* hr-months.gz -- Croatian months (siječanj, veljača, ...)
* int-months.gz -- international months (januar, februar, ...)
* ir-is-lexicon.gz -- words having -isati/irati opposition
* ir-ov-lexicon.gz -- words having-ovati/irati opposition
* verbs-inf-lexicon.gz -- verbs in infinitive
* verbs-lexicon.gz -- verbs
* verbs-pres-lexicon.gz -- verbs in present tense
* verbs-vmf-lexicon.gz -- verbs in synthetic future tense
* modalverbs-lexicon.gz -- modal verbs
* desiti-desavati.gz -- conjugations of "desiti"/"dešavati" (to happen)
* dogoditi-dogadjati.gz -- conjugations of "dogoditi"/"događati" (to happen)
* kinja-ica-lexicon.gz -- words having the oppisition -kinja/ica
* ka-ica-lexicon.gz -- words having the opposition -ka-ica
* lac-telj-lexicon.gz -- words having the opposition -lac/telj


scripts/ -- contains scripts for extracting customized lexicons

* extract-diff-lexicons.py -- extracts customized lexicons for the features which differ Croatian and Serbian
* extract-ind-lexicons.py -- extracts customized lexicons for other features (list may contain same items for Serbian and Croatian)

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



