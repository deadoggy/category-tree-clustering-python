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
        self.root = None

class BUEditTree:

    def __init__(self, tree_name):
        '''
            init function of BUEditTree
            @tree_name: name of this tree
        '''
        self.root = BUEditTreeNode(tree_name, 0, None)
        self.root.root = self.root
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
                    # remove duplicated leaves nodes
                    if next_p in self.leaves_set:
                        self.leaves_set.remove(next_p)
                    break
            if next_p is None:
                next_p = BUEditTreeNode(label, -1, p)
                next_p.root = self.root
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

    traveseQueue = Queue()

    leaf_gn = __GraphNode('leaf', 1, len(graph))
    graph.append(leaf_gn)

    for leaf_node in t1.leaves_set + t2.leaves_set:
        leaf_gn.node_set.append(leaf_node)
        traveseQueue.put(leaf_node)
        k[leaf_node] = leaf_gn
    while not traveseQueue.empty():
        
        v = traveseQueue.get()
        if 0!=len(v.chd_set):
            found = False
            # travese graph reversely to see if there are equal class
            for g_i in xrange(len(graph)-1, -1, -1):
                w = graph[g_i]
                if len(w.out_set)!=len(v.chd_set) or w.label!=v.label or w.height!=v.height:
                    continue
                
                is_same = True
                #get equal class of child nodes
                w_chd_eq_cls = w.out_set
                v_chd_eq_cls = []
                for n in v.chd_set:
                    v_chd_eq_cls.append(k[n])

                #sorted by index of __GraphNode and compare them
                srted_w_chd_eq_cls = sorted(w_chd_eq_cls, cmp=lambda x,y:cmp(x.index, y.index))
                srted_v_chd_eq_cls = sorted(v_chd_eq_cls, cmp=lambda x,y:cmp(x.index, y.index))
                for w_i in xrange(len(srted_w_chd_eq_cls)):
                    w_n = srted_w_chd_eq_cls[w_i]
                    v_n = srted_v_chd_eq_cls[w_i]
                    if 0!=cmp(w_n.index, v_n.index):
                        is_same = False
                        break
                if is_same:
                    if k.has_key(v) and k[v].index!=w.index:
                        raise Exception('error when set K[v]: K[v] has been set')
                    k[v] = w
                    w.node_set.append(v)
                    found = True
                    break
            # if not found, add a new __GraphNode
            if not found:
                new_gn = __GraphNode(v.label, v.height, len(graph))
                k[v] = new_gn
                for chd in v.chd_set:
                    if not k.has_key(chd):
                        raise Exception('not all children of v are in K')
                    k[chd].in_set.append(new_gn)
                    new_gn.out_set.append(k[chd])                
                graph.append(new_gn)
        if v!=t1.root and v!=t2.root:
            v.parent.unprocessed_son_size -= 1
            if 0==v.parent.unprocessed_son_size:
                traveseQueue.put(v.parent)
                v.parent.unprocessed_son_size = len(v.parent.chd_set) # recover unrocessed_son_size to supply next computation
     
def __mapping(t1, t2, graph, k, m12, m21):
    '''
        map nodes between t1 and t2

        @t1: a CateTree
        @t2: a CateTree
        @graph: a list of __GraphNode
        @k: a dict, whose keys are CateTreeNode, whose values are __GraphNode
        @m12: a empty dict, map nodes in t1 to nodes in t2
        @m21: a empty dict, map nodes in t2 to nodes in t1
    '''
    if len(graph)==0 or len(k)==0:
        raise Exception('graph/K empty')
    traverse_queue = Queue()
    traverse_queue.put(t1.root)
    while not traverse_queue.empty():
        # poll a BUEditTreeNode:
        v = traverse_queue.get()
        # leaf node's mapping is delivered to their parent node
        if 0==len(v.chd_set):
            continue
        # chd nodes enqueue
        for n in v.chd_set:
            traverse_queue.put(n)
        # map
        if not m12.has_key(v):
            #unordered tree, there is no need to find the first left equal class
            w = None
            gn = k[v]
            for eqn in gn.node_set:
                if eqn.root==t2.root and not m21.has_key(eqn):
                    w = eqn
                    break
            if w is None:
                continue
            if not k.has_key(w):
                raise Exception('error in mapping: w not in k')
            if k[w] != k[v]:
                raise Exception('graph and K do not consist')

            #using queue to map trees of v and w
            w_queue = Queue()
            v_queue = Queue()
            w_queue.put(w)
            v_queue.put(v)
            while not w_queue.empty():
                n_w_queue = w_queue.get()
                n_v_queue = v_queue.get()
                m12[n_v_queue] = n_w_queue
                m21[n_w_queue] = n_v_queue
                #sort chd_set to ensure responsing
                srted_nw_chd = sorted(n_w_queue.chd_set, cmp=lambda x,y:cmp(k[x].label, k[y].label))
                srted_nv_chd = sorted(n_v_queue.chd_set, cmp=lambda x,y:cmp(k[x].label, k[y].label))
                for i in xrange(len(srted_nw_chd)):
                    if len(srted_nv_chd) != len(srted_nw_chd):
                        print 'stub'
                    w_queue.put(srted_nw_chd[i])
                    v_queue.put(srted_nv_chd[i])



def bottomup_edit_dist_calculator(t1, t2):
    '''
        calculate bottom up distance between t1 and t2

        @t1: one BUEditTree
        @t2: one BUEditTree

        #return: bottom up distance
    '''

    if t1 is t2:
        return 0.0

    graph = []
    k = {}
    m12 = {}
    m21 = {}

    __compact(t1, t2, graph, k)
    __mapping(t1, t2, graph, k, m12, m21)
    d = t1.size - len(m12)
    i = t2.size - len(m12)
    #ignore the root node
    if t1.root.label != t2.root.label:
        d -= 1
        i -= 1

    si = 0
    for e in m12.keys():
        if e.label != m12[e].label:
            si += 1
    return d + i + si


def bottomup_edit_dist_converter(uid, bus_cate_dict, kwargs):
    '''
        convert a user's category data to data a BUEditTree

        @uid: user id
        @bus_cate_dict: a dict whose keys are business ids and values are category paths
        @kwargs: a dict of other parameter, {'pivots':[], 'sigma': val} 

        #return: feature vector
    '''

    t = BUEditTree(uid)
    path_set = []
    for ps in bus_cate_dict.values():
        for p in ps:
            path_set.append(p)
    for path in path_set:
        t.insert(path)
    return t


def printNode(node, level):
    content = ''
    for i in xrange(level-1):
        content += ' | '
    content +=  '-' if 0==level else ' |-'
    content +=  node.label + '\n'
    for chd in node.chd_set:
        content +=  printNode(chd, level+1)
    return content
