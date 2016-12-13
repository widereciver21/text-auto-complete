from lxml import etree
from prepoc import tokenizer
from pprint import pprint

# TUTORIAL is here:


def load(xmlfile):
    with open(xmlfile, "rb") as inp:
        tree = etree.parse(inp)

    return tree


def phrases(tree, count=2):
    sents = {}
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

if __name__ == "__main__":
    t = load(XML)
    phs = phrases(t, 100)
    pprint(phs)
    # example2(t)
