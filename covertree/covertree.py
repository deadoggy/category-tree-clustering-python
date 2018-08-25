#coding:utf-8

from node import Node
import math

class CoverTree:

    def __init__(self, dist_calculator, top_level):
        '''
            init function of CoverTree

            @dist_calculator: function to calculate distance
            @top_level: level of root node
        '''
        self.dist_calculator = dist_calculator
        self.level_stack = []
        self.top_level = top_level
        self.root_node = None

    def insert(self, node):
        '''
            insert intreface function

            @node: the node to be inserted

            #return: True=>success; False=>fail;
        '''
        set = self.level_stack[0] if 0 != len(self.level_stack) else []
        self._insert(node, set,  self.top_level)
        
    def _insert(self, node, cover_set, level):
        '''
            the real insert function

            @node: node to be inserted
            @cover_set: possible parent set
            @level: current level

            #return: True=>success; False=>fail;
        '''
        
        #chech if a empty tree
        if None==self.root_node and self.top_level==level and (None==cover_set or 0==len(cover_set)):
            self.root_node = node
            node.level = level
            self.root_node.parent = node
            self.level_stack.append([node])
            return True

        #if level <= current max level, push a new level
        is_new_level = level <= self.top_level-(len(self.level_stack)-1)
        if is_new_level:
            self._push_level_stack()

        #get children set in 2^level range
        chd_set = self._get_children_set(cover_set)
        dist_bound = 2**level
        valid_chd_set = self._filter(node, chd_set, 0.0, dist_bound)
        if 0 == len(valid_chd_set):
            #if a new level, pop it
            if is_new_level:
                self._pop_level_stack();
            return False
        
        parent_info = self._distance_bew_node_set(node, cover_set)
        if 0.0==parent_info[0]:#already has this node
            parent_info[1].same_val_set.append(node)
            self._update_des_sum(parent_info[1])
            if is_new_level:
                self._pop_level_stack()
            return True
        if not self._insert(node, valid_chd_set, level-1):
            #insert fail
            
            #if can not insert to this level(min distance less than 2^level)
            if parent_info[0] > dist_bound:
                if is_new_level:
                    self._pop_level_stack()
                    return False
            #can insert to this level
            parent_node = parent_info[1]
            parent_node.children_set.append(node)
            node.parent = parent_node
            node.dist_to_prt = parent_info[0]
            node.level = level-1
            self.level_stack[self.top_level-node.level].append(node)
            self._update_des_sum(parent_node)
            self._expand_self_chd(node)
            return True
        else:
            return True
            
    def _push_level_stack(self):
        '''
            add a new level to level stack
        '''
        new_level = []
        for n in self.level_stack[-1]:
            new_level.append(n.generate_chd(True))
        self.level_stack.append(new_level)
        
    def _pop_level_stack(self):
        '''
            pop a level from level stack
        '''
        self.level_stack.pop()
        for n in self.level_stack[-1]:
            n.remove_chd(n.self_chd)

    def _get_children_set(self, set):
        '''
            get all children of a set

            @set: the set to retrieve children

            #return: a set whose elements are children of set
        '''

        ret_set = []
        for n in set:
            ret_set += n.children_set
            if None==n.self_chd:
                ret_set.append(n.generate_chd(False))
        return ret_set

    def _filter(self, center_node, node_set, low_bound, high_bound):
        '''
            filter nodes in node_set that d(center_node, node in node_set) in [low_bound, high_bound]

            @node_set: the node set to choose from
            @center_node: center node
            @low_bound: lower bound of distance
            @high_bound: higher bound of distance 
        '''
        d = self.dist_calculator
        return filter(lambda x: d(x, center_node)>=low_bound and d(x, center_node) <= high_bound, node_set)

    def _update_des_sum(self, node):
        '''
            update sum of descendants from root to a node
            notice that sum  of descendants does not include a node itself

            @node: the node to update
        '''
        p = node
        while True:
            p.des_sum += 1
            if p == self.root_node:
                break
            else:
                p = p.parent

    def _expand_self_chd(self, node):
        '''
            expand self children to lower level

            @node: the node to be expanded
        '''
        current_level = node.level
        if self.top_level-current_level > len(self.level_stack)-1:
            raise Exception('wrong level when expand self child')

        #if has been in lowest level, return
        if self.top_level-current_level == len(self.level_stack)-1:
            return
        
        #update to the lowest level
        parent = node
        for i in range(current_level-1, self.top_level-len(self.level_stack), -1):
            son = parent.generate_chd(True)
            self.level_stack[self.top_level-i].append(son)
            parent = son

    def _distance_bew_node_set(self, node, set):
        min_dist = float('inf')
        nearest_node = None
        for n in node:
            dist = self.dist_calculator(n, node)
            if dist < min_dist:
                min_dist = dist
                nearest_node = n
        
        return [min_dist, nearest_node]
