#coding:utf-8

from covertree.node import Node
from covertree.covertree import CoverTree

class DensityCoverTree(CoverTree) :
    
    def __init__(self, dist_calculator, top_level):
        '''
            init function of density covertree, invoke father's init function

            @dist_calculator: function to calculat distance
            @top_level: level of root
        '''
        super(dist_calculator, top_level)

    def estimate_density(self, node):
        '''
            esitmate density of a node based on PurTreeClust

            @node: node to estimate

            #return: density of @node, long type
        '''
        
        density = 0l

        inf = float('inf')
        level = node.level
        q_i = self.level_stack[self.top_level - level]
        stack_dep = len(self.level_stack)
    
        for i in range(level, self.top_level - stack_dep):
            q = self._get_children_set(q_i)
            alpha = self._filter(node, q, -inf, 2**level-2**(i+1))
            for n in alpha:
                density += n.des_sum
            q_i = self._filter(node, q, 2**level-2**(i+1)+2**(self.top_level-stack_dep-1),
            2**level+2**(i+1)-2**(self.top_level-stack_dep-1))
            density += len(self._subset(q, q_i, node, level))
        density += len(self._filter(node, q_i, -inf, 2**level))

        return density
        

    def _subset(self, q, q_i, node, l):
        '''
            find nodes in q who not in q_i and distance to node in (0.0, 2^l]

            @q:
            @q_i:
            @node:
            @l:

            #return: set satisfies condistions
        '''

        def condition(n):
            dist = self.dist_calculator(node.val, n.val)
            return n not in q_i and dist <= 2**l and dist != 0.0
        return filter(condition, q)
