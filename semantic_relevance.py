from ontology import Ontology

class SemanticRelevance:

    def __init__(self, ontology_filename):
        self.ontology = Ontology(ontology_filename)


    def compute_relevance(self, a, b):
        """
        Computes the semantic relevance between two words
        :param a:
        :param b:
        :return:
        """
        # Find a
        node_a = self.ontology.find(a)

        # Find shortest path from b to a