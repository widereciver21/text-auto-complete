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
        self.trie_idx=[None] * len(self.trie)
        #print("dm",dict_map)
        for k,v in dict_map.items():
            #print("V:",v, self.trie.key_id(k))
            self.trie_idx[self.trie.key_id(k)] = v

    def get(self, key, exact=False):
        if exact:
            try:
                code = self.trie.key_id(key)
                #print ("get-Code:", code)
                return self.trie_idx[code]
            except KeyError:
                #print ("get-notfound:", key)
                return set()
        keys = self.trie.iterkeys(key)
        com = set()
        for key in keys:
            com |= self.get(key, exact=True)
        return com

    def check(self, key):
        return key in self.trie

    def __str__(self):
        return

class Helm(object):
    def __init__(self, sents):
        self.sents=sents
        self.make_trie()

    def make_trie(self):
        mkbs=set()
        for word, d in self.sents.items():
            for mkb, v in d.items():
                mkbs.add(mkb)
        #print("mkbs:",mkbs)
        self.maintrie = marisa_trie.Trie(mkbs)
        tries={}
        for words, d in self.sents.items():
            for mkb, v in d.items():
                code = self.maintrie.key_id(mkb)
                tr = tries.setdefault(code, {})
                tr[words] = v
        self.tries = [None] * len(tries)
        for mkbcode, d in tries.items():
            all_words = {}
            for words, v in d.items():
                for w in words:
                    all_words.setdefault(w, set()).add(words)

            self.tries[mkbcode] = TrieExt(all_words)

    def query(self, mkb10, prefixes=[], op="int"):
        if mkb10 in self.maintrie:
            code = self.maintrie.key_id(mkb10)
            #print ("MKB", code, mkb10, len(self.tries))
            trie = self.tries[code]
            if not prefixes:
                raise RuntimeError("wrong parameter")
            com = None
            for prefix in prefixes:
                s = trie.get(prefix)
                #print("s:", s)
                if com is None:
                    com = s
                else:
                    if op == "int":
                        com &= s
                    elif op == "uni":
                        com |= s
            return com
        return set()


def main(out_result=False):
    global sents
    sents, _ = load_cache(DUMP_FILE)
    print("Loaded", len(sents))
    sents = filter_data(sents)
    print("Filtered", len(sents))
    if out_result:
        slist = list(sents.items())
        slist.sort(key=lambda x: -x[1])
        with open("../result.txt", "w") as out:
            pprint.pprint(slist, out)
    helm = Helm(sents)
    return helm

if __name__ == "__main__":
    main()
