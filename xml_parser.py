# https://github.com/explosion/spaCy/issues/1530
import lxml
from lxml import etree

xml_path = "data/xml_legal_case_exemple/CA-2013-sem-06.xml"
tree = etree.parse(xml_path)

r = tree.xpath('//TexteJuri/P|//MetaJuri/DecisionTraitee/Date|//MetaJuri/DecisionTraitee/Numero')
r = tree.xpath('//TexteJuri/P')


def replace_none(s: str) -> str:
    if s is None:
        return ""
    return "[" + s.strip() + "]"


def get_person_name(node: lxml.etree._Element)-> tuple:
    assert node.tag == "Personne"
    for t in node.iterchildren(tag="Texte"):
        return t.text, node.tail


def get_paragraph_text(parent_node: lxml.etree._Element) -> str:
    content: list = list()
    for node in parent_node.iter():
        if node.tag == "Personne":
            name, after = get_person_name(node)
            content.append(replace_none(name))
            content.append(replace_none(after))
        elif node.tag in ["P", "Adresse"]:
            content.append(replace_none(node.text))
        elif node.tag in ["Texte", "TexteAnonymise"]:
            pass
        else:
            raise NotImplementedError("Unexpected type of node: [" + node.tag + "]")
    content = [x for x in content if len(x) > 0]
    return ' '.join(content)


for i in r:
    print(get_paragraph_text(i))

