class Tree():
    """Class representing the suffix tree."""

    def __init__(self, input = ''):
        """Inits Tree

        Args:
            input (str, optional): input string. Defaults to ''.
        """        
        self.root = Node() 
        self.root.depth = 0 
        self.root.idx = 0 
        self.root.parent = self.root 
        self.root.suffix_link = self.root 
        self.word = input
        self.McCreight(input)
    
    def McCreight(self, input):
        """Builds a Suffix tree using McCreight O(n) algorithm

        Args:
            input (str): input string.
        """        
        u = self.root
        d = 0 

        input += '$' 

        for i in range(len(input)): 
            
            while u.depth == d and input[d + i] in u.transition_links:
            
                u = u.transition_links[input[d + i]]
                d = d + 1

                while d < u.depth and input[u.idx + d] == input[i + d]:
                    d = d + 1
            if d < u.depth:
                u = self.create_node(input, u, d)
            self.create_leaf(input, i, u, d) 
            if not u.suffix_link:
                self.compute_slink(input, u)
            u = u.suffix_link 
            d = d - 1
            
            if d < 0:
                d = 0
            
    def create_node(self, input, u, d):
        """Creates a new node.

        Args:
            input (str): input string.
            u (Node): current node.
            d (int): node depth of v.

        Returns:
            node
        """        
        i = u.idx
        p = u.parent
        v = Node(idx=i, depth=d)
        v.transition_links[input[i + d]] = u
        u.parent = v
        p.transition_links[input[i + p.depth]] = v
        v.parent = p
        return v

    def create_leaf(self, input, i, u, d):
        """Creates a new leaf

        Args:
            input (str): input string.
            i (int): index in input string.
            u (Node): current node.
            d (int): node depth of v.

        Returns:
            leaf node
        """        
        w = Node()
        w.idx = i
        w.depth = len(input) - i
        u.transition_links[input[i + d]] = w
        w.parent = u
        return w

    def compute_slink(self, input, u):
        """Computes suffix link to node u.

        Args:
            input (str): input string.
            u (node): current node.
        """        
        d = u.depth
        v = u.parent.suffix_link 
        while v.depth < d - 1:
            v = v.transition_links[input[u.idx + v.depth + 1]]
        if v.depth > d - 1:
            v = self.create_node(input, v, d - 1)
        u.suffix_link = v

    def find_all(self, pattern):
        """Finds all indexes where pattern can be found in input string.

        Args:
            pattern (str): pattern we are searching.

        Returns:
            list of index/ indexes.
        """        
        node = self.root
        while True:
            edge = self.word[node.idx + node.parent.depth: node.idx + node.depth]
        
            if edge.startswith(pattern):
                break

            i = 0
            while (i < len(edge) and edge[i] == pattern[0]):
                pattern = pattern[1:]
                i += 1

            if i != 0:
                if i == len(edge) and pattern != '':
                    pass
                else:
                    return []

            node = node.transition_links[pattern[0]]
            if not node:
                return []

        leaves = node._get_leaves()
        

        return [n.idx for n in leaves]

class Node():
    """Class representing a node in the suffix tree.
    """    
    def __init__(self, idx=-1, parent=None, depth=-1):
        # Links
        self.suffix_link = None
        self.transition_links = {}
        # Properties
        self.idx = idx
        self.depth = depth
        self.parent = parent
        self.generalized_idxs = {}

    def _get_leaves(self):
        """Get leaves from a given node.

        Returns:
            Leaf nodes
        """        
        if len(self.transition_links) == 0: #Checking if node is a leaf.
            return {self}
        else:
            return {x for n in self.transition_links.values() for x in n._get_leaves()}

