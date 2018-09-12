#coding:utf-8

class Node:
    
    def __init__(self, val=None, parent=None, dist_to_prt=None,
                des_sum=0, level=0, children_set=None, same_val_set=None, index=-1):
        '''
            init function
            
            @val: value of this node
            @parent: parent node of this node
            @dist_to_prt: distance to parent
            @des_sum: number of descendants
            @level: node's level in covertee
            @children_set: set of children of this node
            @same_val_set: nodes which share a same value with this node
            @index: index of the node
        '''
        self.val = val
        self.parent = parent
        self.dist_to_prt = dist_to_prt
        self.des_sum = des_sum
        self.level = level
        self.children_set = children_set if children_set is not None else []
        self.same_val_set = same_val_set if same_val_set is not None else []
        self.self_chd = None
        self.index = index
    
    def generate_chd(self, add_self_chd=False, no=None):
        '''
            generate a new child node

            @add_self_son: True: add the new child node to self son

            #return: the new child
        '''
        chd = Node(val=self.val, parent=self, 
        dist_to_prt=0.0, 
        des_sum=len(self.same_val_set),
        level=self.level-1, children_set=[], 
        same_val_set=self.same_val_set, index=self.index)

        if add_self_chd:
            self.self_chd = chd
            self.children_set.append(self.self_chd)
        
        return chd
    
    def remove_chd(self, chd):
        '''
            remove a child

            @chd: chd node obj
        '''
        if chd not in self.children_set:
            raise Exception('remove_son: not such child')

        if chd == self.self_chd:
            self.self_chd = None

        self.children_set.remove(chd)

