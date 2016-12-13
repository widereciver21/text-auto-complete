#!/usr/bin/env python

import pickle
import pprint
from load import load_cache, DUMP_FILE, dump_cache

sents = None

FILTERED="../filtered.pickle"

def filter_data(sents):
    news = {}
    for k, v in sents.items():
        if v<=1:
            continue
        if len(k)<2:
            continue
        news[k]=v

    dump_cache(FILTERED, news, -1)
    return news


def main():
    global sents
    sents,_ = load_cache(DUMP_FILE)
    print("Loaded", len(sents))
    sents=filter_data(sents)
    slist = list(sents.items())
    slist.sort(key=lambda x: -x[1])
    print("Filtered", len(sents))
    with open("../result.txt", "w") as out:
        pprint.pprint(slist, out)
    quit()

m=main

if __name__=="__main__":
    main()
