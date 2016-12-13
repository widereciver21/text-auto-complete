from lxml import etree
import collections
import csv

DUMP = "../eugeneai.csv"

REPLS = [
    ("\\r\\n", "\n"),
    ("\\n", "\n"),
    ("\\r", "\n"),
    ("\x5c\x74", "\t"),
]

#print(REPLS)


def uncode(t):
    t = t.replace('"', '\\"')
    t = eval('"{}"'.format(t))
    return t.replace("\r", "")


def convert(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter="|")
        root = etree.Element("records")
        tree = etree.ElementTree(root)
        for row in reader:
            try:
                mkb10, diagnose, text = row
            except ValueError:
                print("FAIL: {}".format(row))
                continue
            r = etree.SubElement(root, "row")
            try:
                r.text = uncode(text)
            except ValueError:
                print("FAIL: {}".format(uncode(text)))
                continue
            r.set("mkb10", mkb10)
            d = etree.SubElement(r, "diagnose")
            try:
                d.text = uncode(diagnose)
            except ValueError:
                print("FAIL: {}".format(uncode(diagnose)))
                continue
    return tree


if __name__ == "__main__":
    tree = convert(DUMP)
    s = etree.tostring(
        tree,
        encoding="utf-8",
        xml_declaration=True,
        pretty_print=True,
        standalone=True)
    odump = DUMP.replace(".csv", ".xml")
    o = open(odump, "wb")
    o.write(s)
    o.flush()
    o.close()
