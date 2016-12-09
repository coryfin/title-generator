import xml.etree.ElementTree as ET
import sys
import preprocessing


class SemanticRelevance:

    def __init__(self, ontology_filename):
        self.ontology = self.load_ontology(ontology_filename)

    def compute(self, a, b):
        """
        Computes the semantic relevance between two words
        :param a:
        :param b:
        :return:
        """

        # Relevance for same words is 1
        if a == b:
            return 1

        # Always start with word (not concept)
        a = 'w::' + a
        b = 'w::' + b

        # Make sure a and b are in the ontology
        if a not in self.ontology or b not in self.ontology:
            return 0

        # Find shortest path from a to b
        path = self.shortest_path(self.ontology, a, b)
        if path is None:
            return 0
        else:
            return 1.0 / (len(path) - 1)

    def load_ontology(self, filename):
        """
        Loads the ontology as an undirected graph.
        :param filename:
        :return:
        """
        xml_root = ET.parse(filename).getroot()
        graph = {}
        for concept in xml_root.findall('concept'):  # find all concept nodes

            concept_name = concept.get('name')
            if concept_name not in graph:
                graph[concept_name] = set()

            # Add edges for the parent
            parents = concept.findall("relation[@label='inherit']")
            if len(parents) > 0:

                parent_name = parents[0].text.strip()

                # Point the parent to the child
                if parent_name not in graph:
                    graph[parent_name] = {concept_name}
                else:
                    graph[parent_name].add(concept_name)

                # Point the child to the parent
                graph[concept_name].add(parent_name)

            # Add edge for each child node (words instead of concepts)
            for word in concept.findall("relation[@label='word']"):
                child_name = word.text.strip()

                # Point the child to the parent
                if child_name not in graph:
                    graph[child_name] = {concept_name}
                else:
                    graph[child_name].add(concept_name)

                # Point the parent to the child
                graph[concept_name].add(child_name)

        return graph

    def bfs_paths(self, graph, start, goal):
        """
        Finds all paths from start to goal using breadth-first search
        http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
        :param graph:
        :param start:
        :param goal:
        :return:
        """
        queue = [(start, [start])]
        while queue:
            (vertex, path) = queue.pop(0)
            for next in graph[vertex] - set(path):
                if next == goal:
                    yield path + [next]
                else:
                    queue.append((next, path + [next]))

    def shortest_path(self, graph, start, goal):
        """
        Finds the shortest path in a graph using breadth-first search.
        http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
        :param graph:
        :param start:
        :param goal:
        :return:
        """
        try:
            return next(self.bfs_paths(graph, start, goal))
        except StopIteration:
            return None

    def extract_vectors(self, stories, cap):
        """
        Extracts truncated semantic relevance vectors (top 10 most relevant words in order of relevance).
        :param stories:
        :param cap:
        :return:
        """

        stories = [preprocessing.clean(row, True, True).split(' ') for row in stories]
        sorted_vecs = []

        for story in stories:
            relevance = [0] * len(story)
            for i in range(len(story)):
                for j in range(len(story)):
                    if i != j:
                        relevance[i] += self.compute(story[i], story[j])
            vec = sorted(set(zip(relevance, story)), reverse=True)
            sorted_vecs.append(vec[:cap])
            # relevance, words = (list(t) for t in zip(*sorted(zip(relevance, story))))
            # sorted_vecs.append(words[:cap], relevance[:cap])

        return sorted_vecs


ont_filename = sys.argv[1]
story_filename = sys.argv[2]
num_stories = int(sys.argv[3])

semantic_relevance = SemanticRelevance(ont_filename)
ids, stories, titles = preprocessing.load_stories(story_filename, num_stories)
vectors = semantic_relevance.extract_vectors(stories, 5)
for vector in vectors:
    rel, words = zip(*vector)
    print(str(list(words)) + ': ' + str(list(rel)))
