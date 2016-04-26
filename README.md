Synopsis

--------------------

hbs-twitter-space -- Experiments on spatial distribution of linguistic variables on 
Twitter for Croatian, Bosnian and Serbian. 


Files
--------------------

extract_variables.py -- extracts specific linguistic variables present in Croatian, Bosnian, Serbian and Montenegrinian varieties

hrsrTweets.gz -- Twitter Corpus
hrsrTweets.var.gz -- Twitter Corpus with annotated features for each tweet

custom-lexicons/ -- contains customized lexicons needed for extraction of linguistic variables
	apertium-diftong-v-lexicon.gz -- words having eu/ev or au/av opposition and their labels
	apertium-hdrop-lexicon.gz -- words having h/h-drop opposition at the beginning of words and their labels
	apertium-kh-lexicon.gz -- words containing k/h opposition at the beginning of words and their labels
	apertium-rdrop-lexicon.gz -- words having h/h-drop opposition at the end of words and their labels
	apertium-st-c-lexicon.gz -- words containing št/ć opposition and their labels
	apertium-yat-lexicon.gz -- words with e and (i)je yat-reflex and their labels
	ch-lexicon.gz -- words containing č and/or ć and their lables
	genitiv-og-eg-lexicon.gz -- adjectives, pronouns and numeralia in masc/neutr sg. ending with -og/eg 
	hr_months.gz -- croatian months (siječanj, veljača, ...)
	int_months.gz -- international months (januar, februar, ...)
	inter-stem-lexicon.gz -- stems of verbs ending with -ovati/isati/irati
	verbs-inf-lexicon.gz -- verbs in infinitive
	verbs-lexicon.gz -- verbs
	verbs-pres-lexicon.gz -- verbs in presens
	verbs-vmf-stem-lexicon.gz -- stems of verbs in synthetic future tense 


scripts/ -- contains scripts for extracting customized lexicons

	extract_discr_lexicons.py -- extracts customized lexicons for discriminative features (either "HR" or "SR")
	extract_not_discr_lexicons.py -- extracts customized lexicons for non-discriminative features (list may contain same items for "SR" and "HR")
	extract_irovis_stems.py -- extracts stems of verbs ending with -ovati/isati/irati
	extract_vmf_stems.py -- extracts stems of verbs in synthetic future tense (tag: Vmf) 

evaluation/ -- contains evaluation tables for each linguistic variable extracted with extract_variables.py

lang-id/ -- contains manually annotated tweets according to their language (Croatian/Bosnian/Serbian/Montenegrinian)


Calling the scripts
--------------------

For extracting the variables:

$ python extract_variables.py 


For creating customized lexicons:

$ python extract_discr_lexicons.py
$ python extract_not_discr_lexicons.py
$ python extract_irovis_stems.py
$ python extract_vmf_stems.py 


Contact
--------

scopes.reldi@gmail.com



