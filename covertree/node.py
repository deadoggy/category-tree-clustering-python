#coding:utf-8

class Node:
    
    def __init__(self, val=None, parent=None, dist_to_prt=None,
                des_sum=0, level=0, children_set=[], same_val_set=[]):
        '''
            init function
            
            @val: value of this node
            @parent: parent node of this node
            @dist_to_prt: distance to parent
            @des_sum: number of descendants
            @level: node's level in covertee
            @children_set: set of children of this node
            @same_val_set: nodes which share a same value with this node
        '''
        self.val = val
        self.parent = parent
        self.dist_to_prt = dist_to_prt
        self.des_sum = des_sum
        self.level = level
        self.children_set = children_set
        self.same_val_set = same_val_set
        self.self_son = None
    
    def generate_son(self, add_self_son=False):
        '''
            generate a new son node

            @add_self_son: True: add the new son node to self son

            @return: the new son
        '''
        son = Node(val=self.val, parent=self.parent, 
        dist_to_prt=0.0, des_sum=len(self.same_val_set),
        level=self.level-1, children_set=[], 
        same_val_set=self.same_val_set)

        if add_self_son:
            self.self_son = son
            self.children_set.append(self.self_son)
        
        return son

    def remove_self_son(self):
        self.children_set.remove(self.self_son)
        self.self_son = None
    


