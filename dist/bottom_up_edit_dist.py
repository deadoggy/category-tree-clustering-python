#coding:utf-8
from Queue import Queue

class BUEditTreeNode:

    def __init__(self, label, height, parent):
        '''
            init function of EditTreeNode

            @label: label of this node
            @height: height of this node
            @parent: parent node
        '''
        self.label = label
        self.height = height
        self.parent = parent
        self.des_sum = 0
        self.chd_set = []
        self.unprocessed_son_size = 0

class BUEditTree:

    def __init__(self, tree_name):
        '''
            init function of BUEditTree
            @tree_name: name of this tree
        '''
        self.root = BUEditTreeNode(tree_name, 0, None)
        self.leaves_set = []
        self.size = 1
    
    def insert(self, label_list):
        '''
            insert a list of label to this tree

            @label_list: a list of string, which is cate_path + business_id
        '''

        node_stack = []
        node_stack.append(self.root)
        p = self.root

        #insert node to tree
        for i, label in enumerate(label_list):
            next_p = None
            for chd in p.chd_set:
                if label!=label_list[-1] and label==chd.label:
                    next_p = chd
                    break
            if next_p is None:
                next_p = BUEditTreeNode(label, -1, p)
                p.chd_set.append(next_p)
                p.unprocessed_son_size += 1
                self.size += 1
            node_stack.append(next_p)
            
            #add leaf node to leaves set
            if i == len(label_list)-1:
                self.leaves_set.append(next_p)
            p = next_p

        #pop node_stack to update height and descendants sum
        while 0!=len(node_stack):
            current_node = node_stack.pop()
            if 0==len(current_node.chd_set):
                current_node.height = 1
                current_node.des_sum = 0
                continue
            max_height = -float('inf')
            total_des = len(current_node.chd_set)
            for chd in current_node.chd_set:
                max_height = chd.height if chd.height > max_height else max_height
                total_des += chd.des_sum
            current_node.height = max_height
            current_node.des_sum = total_des

class __GraphNode:

    def __init__(self, label, height, index):
        '''
            init function of __GraphNode

            @label: label represented by __GraphNode
            @height: height of nodes represented by __GraphNode
            @index: index of the __GraphNode
        '''

        self.index = index
        self.label = label
        self.height = height
        self.out_set = []
        self.in_set = []
        self.node_set = []


def __compact(t1, t2, graph, k):
    '''
        compact t1 and t2 to @graph and @k
        
        @t1: CateTree
        @t2: CateTree
        @graph: a list of __GraphNode
        @k: a dict whose keys are CateTreeNode and values are __GraphNode
    '''

    L = {}
    traveseQueue = Queue()

    gn = __GraphNode('leaf', 1, len(graph))
    graph.append(gn)
    L['leaf'] = gn

    for leaf_node in t1.leaves_set + t2.leaves_set:
        gn.node_set.append(leaf_node)
        traveseQueue.put(leaf_node)

    while len(traveseQueue)!=0:
        v = traveseQueue.get()
        if 0!=len(v.chd_set):
            pass
            #TODO:
            


def __mapping(t1, t2, graph, k, m12, m21):
    pass

def bottomup_edit_dist_calculator(t1, t2):
    '''
        calculate bottom up distance between t1 and t2

        @t1: one BUEditTree
        @t2: one BUEditTree

        #return: bottom up distance
    '''

    if t1==t2:
        return 0.0

    graph = []
    k = {}
    m12 = {}
    m21 = {}

    __compact(t1, t2, graph, k)
    __mapping(t1, t2, graph, k, m12, m21)
    d = t1.size - len(m12)
    i = t2.size - len(m12)

    si = 0
    for e in m12.keys():
        if e.label != m12[e].label:
            si += 1
    
    return d + i + si
