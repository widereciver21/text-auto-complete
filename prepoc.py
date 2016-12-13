#!/usr/bin/env python3
import nltk
import re
import sys
import json
import string
from nltk.corpus import stopwords
import pymorphy2
from pprint import pprint

stop_words = stopwords.words('russian')
stop_words.extend(
    ['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на', "«","»"]
)

def stw(word):
    if word == '':
        return True
    if word in string.punctuation:
        return True
    if word in stop_words:
        return True
    return False

def tokenizer(file_text, sents, error_mark=""):
    try:
        tokens = nltk.word_tokenize(file_text)
    except TypeError:
        return sents
    #tokens = [i for i in tokens if not stw(i)]
    # print(tokens)
    words = []
    morph = pymorphy2.MorphAnalyzer()
    for token in tokens:
        p = morph.parse(token)
        if stw(token):
            if len(words)>0:
                idx = tuple(words)
                c = sents.setdefault(idx, 0) + 1
                sents[idx]=c
                words = []
            # len < 0
            continue
        if len(p) == 0:
            words.add(error_mark+token)
            continue
        normal = p[0].normal_form
        words.append(normal)
    if words:
        idx = tuple(words)
        c = sents.setdefault(idx, 0) + 1
        sents[idx]=c
    return sents

if __name__ == '__main__':
    TXT ='Мама мыла раму, быстрая рыжая лисица переперпрыгнула ленивую собаку и жирную кошку.'
    d={}
    d=tokenizer(TXT, d)
    d=tokenizer(TXT, d)
    print(TXT)
    pprint(d)
    