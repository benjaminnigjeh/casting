from fisher_py.data.business import Scan
from fisher_py import RawFile
from sklearn.metrics.pairwise import cosine_similarity
import re
import numpy as np
import pandas as pd
import pickle 
import sys; sys.setrecursionlimit(3000)

class TreeNode:
    def __init__(self, key, index):
        self.left = None
        self.right = None
        self.val = key
        self.index = index

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, index):
        if self.root is None:
            self.root = TreeNode(key, index)
        else:
            self._insert_recursive(self.root, key, index)

    def _insert_recursive(self, node, key, index):
        if key < node.val:
            if node.left is None:
                node.left = TreeNode(key, index)
            else:
                self._insert_recursive(node.left, key, index)
        elif key > node.val:
            if node.right is None:
                node.right = TreeNode(key, index)
            else:
                self._insert_recursive(node.right, key, index)

    def find_closest(self, key):
        return self._find_closest_recursive(self.root, key, float('inf'), -1)

    def _find_closest_recursive(self, node, key, closest_value, closest_index):
        if node is None:
            return closest_index
        
        # Update the closest if the current node is closer
        if abs(node.val - key) < abs(closest_value - key):
            closest_value = node.val
            closest_index = node.index

        # Traverse left or right based on comparison
        if key < node.val:
            return self._find_closest_recursive(node.left, key, closest_value, closest_index)
        else:
            return self._find_closest_recursive(node.right, key, closest_value, closest_index)


def helper_regex(text):
    match = re.search(rf"{'Full'}\s+(\w+)", text)
    if match:
        return match.group(1)
    return None

def cast_func(scan_number):
    "this is a way to cast spectra"
    scan_masses = []
    scan_intensities = []
    data_masses = []
    data_intensities = [] 

    raw_scan = Scan.from_file(raw._raw_file_access, scan_number=scan_number)
    precursor = float(re.findall(r'[\d]*[.][\d]+', raw_scan.scan_type)[1])
    scan_masses = raw_scan.preferred_masses
    scan_intensities = raw_scan.preferred_intensities

    for i in range(4000, 20000): 
        data_intensities.append(0) 
        data_masses.append(i/10)

    for j in range(0,len(scan_masses)):
        for i in range(0,len(data_masses)):
            if (i+ 4000 + 1)/10 > scan_masses[j] > (i + 4000)/10: 
                data_intensities[i] = data_intensities[i] + scan_intensities[j]

    for i in range(0,16000):
        if (precursor -5) < data_masses[i] < (precursor +5): data_intensities[i] = 0
        
    return(list(data_intensities))

def cast_func_1amu(scan_number):
    scan_masses = []
    scan_intensities = []
    data_masses = []
    data_intensities = [] 
 

    raw_scan = Scan.from_file(raw._raw_file_access, scan_number=scan_number)
    precursor = float(re.findall(r'[\d]*[.][\d]+', raw_scan.scan_type)[1])
  
    scan_masses = raw_scan.preferred_masses
    scan_intensities = raw_scan.preferred_intensities
   
    # for k in range(0, len(scan_intensities)):
    #     if scan_intensities[k] > (5/100)*max(scan_intensities): 
    #         scan_intensities1.append(scan_intensities[k])
    #         scan_masses1.append(scan_masses[k])

    for i in range(400, 2000): 
        data_intensities.append(0) 
        data_masses.append(i)

    for j in range(0,len(scan_masses)):
        for i in range(0,len(data_masses)):
            if (i+ 400 + 1) > scan_masses[j] > (i + 400): 
                data_intensities[i] = data_intensities[i] + scan_intensities[j]

    # for i in range(0,len(data_masses)):
    #     if (precursor -5) < data_masses[i] < (precursor +5): data_intensities[i] = 0
        
    return(list(data_intensities))
def cast_func_1amu_bst(scan_number):
    scan_masses = []
    scan_intensities = []
    data_masses = []
    data_intensities = [] 
 
    raw_scan = Scan.from_file(raw._raw_file_access, scan_number=scan_number)
    precursor = float(re.findall(r'[\d]*[.][\d]+', raw_scan.scan_type)[1])
  
    scan_masses = raw_scan.preferred_masses
    scan_intensities = raw_scan.preferred_intensities
    bst = BST()
    for index, value in enumerate(data_masses):
        bst.insert(value, index)
   
    for i in range(400, 2000): 
        data_intensities.append(0) 
        data_masses.append(i)

    for j in range(0,len(scan_masses)):
        index = bst.find_closest(scan_masses[j])
        data_intensities[index] = data_intensities[index] + scan_intensities[j]
        
    return(list(data_intensities))


