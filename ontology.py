import xml.etree.ElementTree as ET


class Ontology:

    def __init__(self, filename=None):
        if filename is None:
            self._nodes = []
            self._root = None
        else:
            xml_root = ET.parse(filename).getroot()
            self._nodes = []
            for concept in xml_root.findall('concept'):  # find all concept nodes
                concept_node = OntologyNode(concept)
                self._nodes.append(concept_node)

                words = concept.findall("relation[@label='word']")
                if len(words) > 0:
                    for word in words:
                        word_node = OntologyNode(name=word.text.strip())
                        word_node.parent = concept_node
                        self._nodes.append(word_node)
            self._root = None

            # Connect the nodes
            for node1 in self._nodes:
                if node1.name == 'ont::root':
                    self._root = node1
                elif node1.parent.parent is None:
                    nodes = self.find(node1.parent.name)
                    if len(nodes) > 0:
                        node1.parent = nodes[0]

    @property
    def root(self):
        return self._root

    def find(self, name):
        return list(filter(lambda x: x.name == name, self._nodes))


class OntologyNode:

    def __init__(self, concept=None, name=None):
        if concept is not None:
            self._name = concept.get('name')
            parents = concept.findall("relation[@label='inherit']")
            if len(parents) > 0:
                self.parent = OntologyNode(name=parents[0].text.strip())
            else:
                self.parent = None
        elif name is not None:
            self._name = name
            self._parent = None
        else:
            self._name = None
            self._parent = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def __str__(self):
        return self.name
