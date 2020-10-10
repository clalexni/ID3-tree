#!/usr/bin/env python3.6
import sys
import math
from itertools import islice
import random

case1 = 0
case2 = 0
case3 = 0

class DataSet:
  """
  dataset fields:
  d.examples      An example matrix. It is basically a list of examples, 
                  each example is a list of attribute values + class value
  d.col_indices   A list of indices that is corresponded to a column of the 
                  examples matrix
  d.col_names     A list of name (label) corresponding to the matrix's column
  d.attr_indices  Same as col_indices but without the last column (class).
                  In another word, each attribute is a column index
  d.col_values    A list of list: each sublist is the set of possible values
                  corresponding to an attribute or class
  """
  def __init__(self, examples=None, col_names=None):
    self.examples = examples
    self.col_names = col_names
    self.col_indices = list(range(len(self.examples[0])))
    self.attr_indices = [i for i in self.col_indices[:-1]]
    self.col_values = list(map(lambda x: set(x), zip(*self.examples)))
    #def unique(numbers):
    #  return set(numbers)



class LeafNode:
  """leaf node holds the result(class)"""
  def __init__(self, result):
    self.result = result

  def __call__(self, example):
    """
    Given an example, return class result.
    use this call function recurrsively with Internal node call function
    """
    return self.result

  def __repr__(self):
    return repr(int(self.result))


class InternalNode:
  """
  fields:
  attr        attribute to test (column number)
  attr_name   attribute's name
  branches    dictionary that hold every value of the attribute
              attribute value is key and subtree(Internal node or leaf node)
              is the value
  """
  def __init__(self, attr, attr_name=None, branches_dict=None):
    self.attr = attr
    self.attr_name = attr_name or attr
    self.branches_dict = branches_dict or {}
  
  def __call__(self, example):
    """
    Given an example, 
    recurrsivly call internal node function to get class result
    """
    attr_value = example[self.attr]
    if attr_value in self.branches_dict:
      return self.branches_dict[attr_value](example)

  def add(self, attr_value, subtree):
    """add subtree as branch"""
    self.branches_dict[attr_value] = subtree
  
  def __repr__(self):
    return self.attr_name


def id3_tree_learner(dataset):
  """
  return id3_tree_learning result
  """
  def id3_tree_learning(examples, attr_indices):
    """id3 decision tree algorithm"""
    if len(examples) == 0:
      global case1
      case1 = case1 + 1 #case1
      return LeafNode(most_frequent_class(dataset.examples)[1]) #mfc of set
    if all_same_class(examples):
      return LeafNode(examples[0][-1])
    if len(attr_indices) == 0:
      classes, class_from_subset = most_frequent_class(examples) #mfc of subset
      if len(classes) == 1:
        global case2
        case2 = case2 + 1 #case2
        return LeafNode(class_from_subset)
      elif len(classes) > 1:
        global case3
        case3 = case3 + 1 #case3
        return LeafNode(most_frequent_class(dataset.examples)[1]) #mfc of set
    #recurrsive case
    A = choose_attribute(attr_indices, examples)
    tree = InternalNode(A, dataset.col_names[A])
    for (attr_value, exs) in split_by(A, examples):
      subtree = id3_tree_learning(exs, trim_item(A, attr_indices))
      tree.add(attr_value, subtree)
    return tree
      
  def most_frequent_class(examples):
    """
    return equally common class and the most frequent class with break tie mechanism
    if frequency are the same, break tie by choosing class0 > class1 > class2
    """
    dict = {}
    max_frequency, classes = 0, []
    for item in [ex[-1] for ex in examples]:
      dict[item] = dict.get(item, 0) + 1
      if dict[item] > max_frequency:
        max_frequency = dict[item]
        classes.clear()
        classes.append(item)
      elif dict[item] == max_frequency:
        classes.append(item)
    return classes, min(classes)

  def all_same_class(examples):
    """are all examples having the same class value?"""
    class0 = examples[0][-1]
    return all(ex[-1] == class0 for ex in examples)

  def split_by(attr_index, examples):
    """ 
    split examples by a specific attribute
    return a list of (attr_value, examples) pairs
    the examples in each pair have the same attribute value
    given an attribute index
    """
    return [(v, [ex for ex in examples if ex[attr_index] == v])
            for v in dataset.col_values[attr_index]]

  def trim_item(item, List):
    """return the List but all the occurance of item are trimmed"""
    return [i for i in List if i != item]

  def choose_attribute(attr_indices, examples):
    """ 
    return attribute that yield highest information gain
    break tie by choosing the left-most attribute index
    """
    max_ig, indices = 0, []
    for index in attr_indices:
      ig = entropy(examples) - remainder_entropy(index, examples) #information gain
      if ig > max_ig:
        max_ig = ig
        indices.clear()
        indices.append(index)
      elif ig == max_ig:
        indices.append(index)
    return min(indices)

  def entropy(examples):
    """return entropy value of examples"""
    dict = {}
    for item in [ex[-1] for ex in examples]:
      dict[item] = dict.get(item, 0) + 1
    entropy = sum(-(val/len(examples))*math.log2(val/len(examples))
                  for val in dict.values())
    return entropy

  def remainder_entropy(attr_index, examples):
    """ 
    conditional entropy
    return children's average entropy based on a split by a specific attribute
    """
    remainder_entropy = 0
    for (v, exs) in split_by(attr_index, examples):
      remainder_entropy = remainder_entropy + (len(exs)/len(examples)) * entropy(exs)
    return remainder_entropy

  return id3_tree_learning(dataset.examples, dataset.attr_indices) # id3 algorithm input


def parse_data(input_file):
  """ 
  return a list of column names and an examples matrix
  """
  with open(input_file, 'r') as file:
    data = file.readlines()
    col_names = data[0].split()
    examples = [line.split() for line in islice(data, 1, len(data))]
    return col_names, examples

def stdout(tree):
  """print tree recursively"""
  def print_tree(tree, level):
    if isinstance(tree, LeafNode):
      print(' ', tree, end='')
      return 1
    else:
      print()
      for branch in sorted(tree.branches_dict.keys()):
        print('| ' * level, end='')
        print(tree, '= ', int(branch), ':', end='')
        val = print_tree(tree.branches_dict[branch], level + 1)
        if val == 1:
          print()
  print_tree(tree, 0)

def accuracy_test(tree, test_examples):
  """test the accuracy of the tree on the test_examples"""
  count = 0
  for ex in test_examples:
    if tree(ex) == ex[-1]:
      count = count + 1
  return count/len(test_examples)


if __name__ == '__main__':
  training_file = sys.argv[1]
  test_file = sys.argv[2]

  col_names, examples = parse_data(training_file)
  ds_train = DataSet(examples, col_names)
  tree = id3_tree_learner(ds_train)
  
  #print(case1, case2, case3) #TODO debug this ting
  
  stdout(tree)
  print('\nAccuracy on training set (', len(examples), ' instances): ',
        '{:.2%}'.format(accuracy_test(tree, examples)), sep='')


  col_names, test_examples = parse_data(test_file)

  print('Accuracy on test set (', len(test_examples), ' instances): ',
        '{:.2%}'.format(accuracy_test(tree, test_examples)), sep='')

  print('\nLearning Curve: (accuracy on test set)')
  for i in range(50, len(examples)+1, 50):
    sample = random.sample(examples, i)
    ds_sample = DataSet(sample, col_names)
    tree_sample = id3_tree_learner(ds_sample)
    print('Sample size: ', len(sample), '; ', 
          ' Accuracy: ', '{:.2%}'.format(accuracy_test(tree_sample, test_examples)))

