class SuffixNode(object):

    def __init__(self, text):
        self.children = {}
        self.parent = None
        self.suffix_link = None
        self.i_from = 0
        self.i_to = 0
        self.text = text

    @property
    def length(self):
        return self.i_to - self.i_from

    def add(self, i_from, i_to):
        child = SuffixNode(self.text)
        child.i_from = i_from
        child.i_to = i_to
        child.parent = self
        self[self.text[i_from]] = child
        return child

    def split(self, i_split):
        i_from = self.i_from
        i_to = self.i_to
        assert i_split > i_from
        assert i_split < i_to
        self.i_to = i_split
        child = SuffixNode(self.text)
        child.i_from = i_split
        child.i_to = i_to
        child.parent = self
        child.children = self.children
        self.children = {}
        self[self.text[i_from]] = child

    @property
    def label(self):
        return repr(self.text[self.i_from : self.i_to])

    def __getitem__(self, ident):
        return self.children[ident]

    def __setitem__(self, ident, child):
        self.children[ident] = child

    def __str__(self, indent=0):
        return '%s%s\n%s' % (
            indent * '  ',
            self.label,
            ''.join(
                child.__str__(indent + 1)
                for key, child in sorted(self.children.iteritems())
            )
        )

    def McCreight(text):

        '''Build suffix tree for the text.
        >>> print McCreight('ananas$')
        ''
        '$'
        'a'
            'na'
            'nas$'
            's$'
            's$'
        'na'
            'nas$'
            's$'
        's$'
        <BLANKLINE>
        '''

        def fast_scan(node, i_from, i_to):
            assert node is not None
            length = i_to - i_from
            assert length >= 0
            if length == 0:
                return node, node.i_from
            node = node[text[i_from]]
            while length > node.length:
                i_from += node.length
                length -= node.length
                node = node[text[i_from]]
            return node, node.i_from + length

        def slow_scan(node, i_from, i_to):
            assert node is not None
            assert i_from <= i_to
            delta = 0
            loop = True
            try:
                node = node[text[i_from]]
                while i_from < i_to and loop:
                    if node.i_from + delta < node.i_to:
                        if text[i_from] == text[node.i_from + delta]:
                            delta += 1
                            i_from += 1
                        else:
                            break
                    else:
                        delta = 0
                        node = node[text[i_from + delta]]
            except KeyError:
                pass
            if delta > 0:
                node.split(node.i_from + delta)
            leaf = node.add(i_from, i_to)
            return node, leaf

        text_len = len(text)
        root = SuffixNode(text)
        head = root
        leaf = root.add(0, text_len)
        for j in range(1, text_len):
            if head == root:
                head, leaf = slow_scan(root, leaf.i_from + 1, leaf.i_to)
                continue
            parent = head.parent
            if parent == root:
                head_sl, i = fast_scan(parent, head.i_from + 1, head.i_to)
            else:
                head_sl, i = fast_scan(parent.suffix_link, head.i_from, head.i_to)
            if i < head_sl.i_to:
                # s(head) is in the middle of an edge
                head_sl.split(i)
                new_head = head_sl
                leaf = new_head.add(leaf.i_from, leaf.i_to)
            else:
                # s(head) is a node
                new_head, leaf = slow_scan(head_sl, leaf.i_from, leaf.i_to)
            head.suffix_link = head_sl
            head = new_head

        return root



s_tree = SuffixNode('mississippi')
print(s_tree.McCreight())

