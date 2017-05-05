#!/usr/bin/env python3
import re
import sys
import json
import string

from stop_words import get_stop_words

import pymorphy2
from pymorphy2.tokenizers import simple_word_tokenize
from pprint import pprint

stop_words = get_stop_words('russian')[:]
stop_words.extend(
    ['—', "«","»", "."]
)

# DOTRE=re.compile("")

def stw(word):
    """Test if the word is a stop word.
    """
    if word == '':
        return True
    if word in string.punctuation:
        return True
    if word in stop_words:
        return True
    try:
        _ = float(word)
        return True
    except ValueError:
        pass
    return False

GROUPING_SPACE_REGEX = re.compile(r'([^\w_-]|[+])', re.UNICODE)

def _split(s):
    return GROUPING_SPACE_REGEX.split(s)

def tokenizer(file_text, sents, error_mark="", mkb10=""):
    try:
        sentences = simple_word_tokenize(file_text, _split=_split)
        # print ("Sents:", sentences)
    except TypeError:
        return sents
    tokens = []
    for sentence in sentences:
        try:
            tokens.extend(simple_word_tokenize(sentence, _split=_split))
        except TypeError:
            return sents
    #tokens = [i for i in tokens if not stw(i)]
    #print("Tokens:", tokens)
    words = []
    morph = pymorphy2.MorphAnalyzer()
    nt = []
    for token in tokens:
        if token != "." and "." in token:
            try:
                _  = float(token)
                nt.append(token)
                continue
            except ValueError:
                pass
            spl = token.split(".")
            for s in spl[:-1]:
                nt.append(s)
                nt.append(".")
            nt.append(spl[-1])
        else:
            nt.append(token)
    tokens = nt

    def account_phrase(sents, phrase, mkb10):
        assert phrase
        idx = tuple(words)
        d = sents.setdefault(idx, {})
        for end in range(len(mkb10)+1):
            mkb = mkb10[:end]
            c = d.setdefault(mkb, 0) + 1
            d[mkb] = c
            sents[idx]=d

    # Now divide the word list by stop words on phrases.
    for token in tokens:
        p = morph.parse(token)
        if stw(token):
            if len(words)>0:
                account_phrase(sents, words, mkb10)
                words = []
            continue
        if len(p) == 0:
            words.add(error_mark+token)
            continue
        normal = p[0].normal_form
        words.append(normal)
    if words:
        account_phrase(sents, words, mkb10)
    return sents

def main():
    TXT ="""
    Мама мыла раму, быстрая рыжая лисица переперпрыгнула ленивую собаку и жирную кошку.
    Мама мыла раму.Папа выбрасывал мусор,играя на скрипке за 36.78 рубля.
    """
    d={}
    d=tokenizer(TXT, d)
    d=tokenizer(TXT, d)
    print(TXT)
    pprint(d)

if __name__ == '__main__':
    main()
