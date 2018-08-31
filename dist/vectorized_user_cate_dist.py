#coding: utf-8

from data_loader.data_loader import DataLoader


class CateTreeNode:

    def __init__(self, label, parent):
        '''
            init function of CateTreeNode

            @laebl: label of the node
            @parent: parent node
        '''
        if type(label)!=list:
            raise Exception('label must be a str')
        if parent.__class__!=CateTreeNode:
            raise Exception('parent must be a CateTreeNode')

        self.label = label
        self.parent = parent
        self.bus_cnt = 0 #count of business whose tail category is represented by this node
        self.chd_set = [] #children set
    
    def find_label_in_chd(self, label):
        '''
            find if there exists a node in chd_set whose label is same with @label

            @label: label to find

            #return: None if not exists, else the instance
        '''
        if type(label) != str:
            raise Exception('label must be label')
        
        for n in self.chd_set:
            if n.label == label:
                return n
        return None
    
class CateTree:

    def __init__(self):
        '''
            init function of CateTree
        '''
        self.root = CateTreeNode(label='', parent=None)
    
    def insert(self, cate_path):
        '''
            insert a category path to category tree, if the path has been
            inserted, then add 1 to bus_cnt
            
            @cate_path: a category path 
        '''

        if type(cate_path) != list:
            raise Exception('cate_path must be a list!')

        current_node = self.root
        for i in xrange(len(cate_path)):
            tmp_label = cate_path[i]
            tmp_chd_set = current_node.chd_set
            
            next_node = None
            for n in tmp_chd_set:
                if n.label == tmp_label:
                    next_node = n
                    break
            
            if next_node is None:
                next_node = CateTreeNode(label=tmp_label, parent=current_node)
                current_node.chd_set.append(next_node)
            current_node = next_node
        current_node.bus_cnt += 1
    
    def similarity(self, path_set):
        '''
            calculate similarity between a user and this tree

            @path_set: a set of paths, [ [<path_1>], [<path_2>], ...]

            #return: a float
        '''

        if type(path_set)!=list:
            raise Exception('path_set must be list')

        sum_similarity = 0.0
        for path in path_set:
            similarity = 1.0
            found = False
            p = self.root
            for i in xrange(len(path)-1):
                label = path[i]
                user_cate_node = p.find_label_in_chd(label)
                if user_cate_node is not None:
                    bus_share = 0.0 if user_cate_node.bus_cnt==0 else 1.0
                    similarity *= 1.0/(len(user_cate_node.chd_set) + bus_share)
                    if i == len(path)-2:
                        similarity *= 1.0/user_cate_node.bus_cnt
                    
                    p = user_cate_node
                else:
                    found = False
                    break
            
            if found:
                sum_similarity += similarity
        
        return sum_similarity


def vectorized_convertor(uid, bus_cate_dict, other_para):
    if type(other_para) != list:
        raise Exception('other_para must be a list')
    if type(bus_cate_dict) != dict:
        raise Exception('bus_cate_dict must be a dict')

    pivots = other_para[0]



def generate_category_tree(data_loader):


    