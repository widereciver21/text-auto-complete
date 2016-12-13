#!/usr/bin/env python

import nltk
#nltk.download()

sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
tokens = nltk.word_tokenize(sentence)
print("tok:",tokens)
#['At', 'eight', "o'clock", 'on', 'Thursday', 'morning',
#'Arthur', 'did', "n't", 'feel', 'very', 'good', '.']
tagged = nltk.pos_tag(tokens)
print(tagged)
#[('At', 'IN'), ('eight', 'CD'), ("o'clock", 'JJ'), ('on', 'IN'),
#('Thursday', 'NNP'), ('morning', 'NN')]
