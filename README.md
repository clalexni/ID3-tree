# ID3-tree
### Goal 
build ID3 decision tree

### Requirements:
- Python3.6
- data file (path)
- command line: (take two inputs of path to the data file)
  ./id3_tree.py data/test.dat data/train/dat
### Some rule descriptions
1. When building a decision tree, if you reach a leaf node but still have examples that belong to
different classes, then choose the most frequent class (among the instances at the leaf node). 
2. If you reach a leaf node in the decision tree and have no examples left or the examples are equally split
among multiple classes, then choose the class that is most frequent in the entire training set. If two
or more classes are equally frequent in the entire training set, break ties by preferring class 0 to
class 1 and preferring class 1 to class 2. Do not implement pruning.
3. A word on tie breaking: when choosing attributes using information again, if two or more
attributes achieve the highest information gain value, break ties by choosing the earliest one in
the list of attributes (assuming that the attributes in the first line of a training file are read in a
left-to-right manner)

### Terminal Criterias
1. exmaples have same class:
  - Done
2. no example left: (meaning there are unused attribute)
  - select most frequent class of the entire dataset
3. no attribute left:
  - choose the most frequent class of the subset at the leaf node
    - If classes are equally common at subset, select from the entire dataset

Note: If equally common class exists in the entire dataset, break tie class0 > class1 > class2 > ..



