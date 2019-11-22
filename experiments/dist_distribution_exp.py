import sys
sys.path.append(sys.path[0]+'/../')
import numpy as np
import random
import  json
from data_loader.data_loader import *
from dist.vectorized_user_cate_dist import *
import random
from config.load_config import Config
from sklearn.metrics import jaccard_similarity_score
import os





