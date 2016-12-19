#!/usr/bin/env python

import pickle
import pprint
from load import load_cache, DUMP_FILE, dump_cache
import marisa_trie


sents = None

FILTERED = "../filtered.pickle"

def filter_data(sents):
    news = {}
    for k, d in sents.items():
        if len(k) == 1 and len(k[0]) <= 2:
            continue
        newd={}
        for mkb, v in d.items():
            if v <= 1:
                continue
            newd[mkb]=v
        if newd:
            news[k] = newd

    dump_cache(FILTERED, news, -1)
    return news

class TrieExt(object):
    def __init__(self, dict_map):
        self.trie = marisa_trie.Trie(dict_map.keys())
        self.trie_idx=[0] * len(self.trie)
        for k,v in dict_map.items():
            self.trie_idx[self.trie.key_id(k)] = v

    def get(self, key):
        try:
            code = self.trie.key_id(key)
        except KeyError:
            keys = self.trie.prefixes(key)
            return self.get(keys[0]) # FIXME: 0 examples
        return self.trie_idx[code]

    def check(self, key):
        return key in self.trie

class Helm(object):
    def __init__(self, sents):
        self.sents=sents
        self.make_trie()

    def make_trie(self):
        mkbs=set()
        for word, d in self.sents.items():
            for mkb, v in d.items():
                mkbs.add(mkb)
        self.maintrie = marisa_trie.Trie(mkbs)
        tries={}
        for word, d in self.sents.items():
            for mkb, v in d.items():
                code = self.maintrie.key_id(mkb)
                tr = tries.setdefault(code, {})
                tr[word] = v
        self.tries = [None] * len(tries)
        for mkbcode, d in tries.items():
            all_words = {}
            for words, v in d.items():
                for w in words:
                    all_words.setdefault(w, set()).add(words)

            self.tries[mkbcode] = TrieExt(all_words)


    def query(self, mkb10, prefixes=[]):
        if mkb10 in self.maintrie:
            code = self.maintrie.key_id(mkb10)
            print (code, len(self.tries))
            trie = self.tries[code]
            if not prefixes:
                raise RuntimeError("wrong parameter")
            return trie.get(prefixes[0]) # FIXME: Just first prefix
        return None

def fact(n):
    if n==0: return 1
    if n==1: return 1
    return n * fac(n-1)

# fact(100)

def main():
    global sents
    sents, _ = load_cache(DUMP_FILE)
    print("Loaded", len(sents))
    sents = filter_data(sents)
    #slist = list(sents.items())
    #slist.sort(key=lambda x: -x[1])
    print("Filtered", len(sents))
    #with open("../result.txt", "w") as out:
    #    pprint.pprint(slist, out)
    helm = Helm(sents)
    return helm.query(mkb10="C34.0", prefixes=["арт","гип"])

if __name__ == "__main__":
    main()
