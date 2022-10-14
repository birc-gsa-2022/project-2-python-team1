class STree():
    """Class representing the suffix tree."""

    def __init__(self, input=''):
        self.root = _SNode()
        self.root.depth = 0
        self.root.idx = 0
        self.root.parent = self.root
        self.root._add_suffix_link(self.root)

        self.build(input)
    
    def build(self, x):
        """Builds the Suffix tree on the given input"""
        x += '$'
        self.word = x
        self._build_McCreight(x)

    def _build_McCreight(self, x):
        """Builds a Suffix tree using McCreight O(n) algorithm."""
        u = self.root
        d = 0
        for i in range(len(x)):

            while u.depth == d and u._has_transition(x[d + i]):
                u = u._get_transition_link(x[d + i])
                d = d + 1
                while d < u.depth and x[u.idx + d] == x[i + d]:
                    d = d + 1
            if d < u.depth:
                u = self._create_node(x, u, d)
            self._create_leaf(x, i, u, d)
            if not u._get_suffix_link():
                self._compute_slink(x, u)
            u = u._get_suffix_link()
            d = d - 1
            if d < 0:
                d = 0

    def _create_node(self, x, u, d):
        i = u.idx
        p = u.parent
        v = _SNode(idx=i, depth=d)
        v._add_transition_link(u, x[i + d])
        u.parent = v
        p._add_transition_link(v, x[i + p.depth])
        v.parent = p
        return v

    def _create_leaf(self, x, i, u, d):
        w = _SNode()
        w.idx = i
        w.depth = len(x) - i
        u._add_transition_link(w, x[i + d])
        w.parent = u
        return w

    def _compute_slink(self, x, u):
        d = u.depth
        v = u.parent._get_suffix_link()
        while v.depth < d - 1:
            v = v._get_transition_link(x[u.idx + v.depth + 1])
        if v.depth > d - 1:
            v = self._create_node(x, v, d - 1)
        u._add_suffix_link(v)


  
    def find_all(self, y):
        node = self.root
        while True:
            edge = self._edgeLabel(node, node.parent)
            if edge.startswith(y):
                break

            i = 0
            while (i < len(edge) and edge[i] == y[0]):
                y = y[1:]
                i += 1

            if i != 0:
                if i == len(edge) and y != '':
                    pass
                else:
                    return []

            node = node._get_transition_link(y[0])
            if not node:
                return []

        leaves = node._get_leaves()
        return [n.idx for n in leaves]

    def _edgeLabel(self, node, parent):
        """Helper method, returns the edge label between a node and it's parent"""
        return self.word[node.idx + parent.depth: node.idx + node.depth]

    


class _SNode():
    

    """Class representing a Node in the Suffix tree."""

    def __init__(self, idx=-1, parentNode=None, depth=-1):
        # Links
        self._suffix_link = None
        self.transition_links = {}
        # Properties
        self.idx = idx
        self.depth = depth
        self.parent = parentNode
        self.generalized_idxs = {}


    def _add_suffix_link(self, snode):
        self._suffix_link = snode

    def _get_suffix_link(self):
        if self._suffix_link is not None:
            return self._suffix_link
        else:
            return False

    def _get_transition_link(self, suffix):
        return False if suffix not in self.transition_links else self.transition_links[suffix]

    def _add_transition_link(self, snode, suffix):
        self.transition_links[suffix] = snode

    def _has_transition(self, suffix):
        return suffix in self.transition_links

    def is_leaf(self):
        return len(self.transition_links) == 0


    def _get_leaves(self):
        # Python <3.6 dicts don't perserve insertion order (and even after, we
        # shouldn't rely on dicts perserving the order) therefore these can be
        # out-of-order, so we return a set of leaves.
        if self.is_leaf():
            return {self}
        else:
            return {x for n in self.transition_links.values() for x in n._get_leaves()}
