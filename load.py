#!/usr/bin/env python
from lxml import etree
from prepoc import tokenizer
from pprint import pprint
import pickle 

# TUTORIAL is here:

DUMP_FILE="../onko-texts.pickle"

def load(xmlfile):
    with open(xmlfile, "rb") as inp:
        tree = etree.parse(inp)

    return tree


def dump_cache(filename, sents, cnt=None):
    print("Saving the progress into a pickle")
    with open(filename, "wb") as f:
        if cnt is not None:
            sents["__count__"]=cnt
        pickle.dump(sents, f)
        f.flush()
        if cnt is not None:
            del sents["__count__"]

def load_cache(filename):
    print(filename)
    with open(filename, "rb") as f:
        print("Loading pickle.")
        sents=pickle.load(f)
        if "__count__" in sents:
            cnt=sents["__count__"]
            del sents["__count__"]
        else:
            cnt=None
    return sents,cnt

def phrases(tree, count=2, pcount=100):
    sents = {}
    all_count = count
    # TODO: Load progress
    try:
        sents,lcnt=load_cache(DUMP_FILE)
    except OSError:
        print("No Progress found!")
        lcnt = 0
    cnt = 0
    for node in tree.iterfind("//row"):
        if count == 0:
            break        
        if cnt<lcnt:
            cnt+=1
            continue
        # print(etree.tostring(node))
        #print("mkb10={}".format(node.get("mkb10", None)))
        #print("diagnose={}".format(node[0].text))
        sents = tokenizer(node.text, sents, error_mark="-")
        #print("TEXT:=========================\n{}".format(node.text))
        #print("TAIL:====must be empty========\n{}".format(node.tail))
        count -= 1
        # print("C:{}".format(count))
        print(".", end="")
        cnt +=1
        if cnt % pcount == 0:
            print("Dumping for {} of {}".format(cnt, all_count))
            dump_cache(DUMP_FILE, sents, cnt)
    else:
        print("No records found.") 
    dump_cache(DUMP_FILE,sents,cnt)
    return sents


def example2(tree, count=2):
    print("="*40)
    print("Printing some diagnoses.")
    print("="*40)
    for diagnose in tree.xpath("//row/diagnose/text()"):
        print(diagnose)
        count -= 1
        if count == 0:
            break
    else:
        print("No records found.")


XML = "../eugeneai.xml"

def main():
    t = load(XML)
    r = t.getroot()
    rl = len(r)
    print("Records No: {}".format(rl))
    phs = phrases(t, rl, 100)
    pprint(phs)
    # example2(t)
    quit()

if __name__ == "__main__":
    main()
