# ID3-tree
### Goal 
build ID3 decision tree

### Some rules
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
