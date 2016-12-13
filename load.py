#!/usr/bin/env python
from lxml import etree
from prepoc import tokenizer
from pprint import pprint
import pickle 

# TUTORIAL is here:


def load(xmlfile):
    with open(xmlfile, "rb") as inp:
        tree = etree.parse(inp)

    return tree


def phrases(tree, count=2, pcount=100):
    sents = {}
    cnt = 0
    for node in tree.iterfind("//row"):
        if count == 0:
            break        
        # print(etree.tostring(node))
        #print("mkb10={}".format(node.get("mkb10", None)))
        #print("diagnose={}".format(node[0].text))
        sents = tokenizer(node.text, sents, error_mark="-")
        #print("TEXT:=========================\n{}".format(node.text))
        #print("TAIL:====must be empty========\n{}".format(node.tail))
        count -= 1
        print("C:{}".format(count))
        cnt +=1
        if cnt % pcount == 0:
            print("Saving pickle")
            with open("../onko-texts.pickle", "wb") as f:
                sents["__count__"]=cnt
                pickle.dump(sents, f)
                f.flush()
                del sents["__count__"]
    else:
        print("No records found.") 
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
    phs = phrases(t, 100)
    pprint(phs)
    # example2(t)

if __name__ == "__main__":
    main()
