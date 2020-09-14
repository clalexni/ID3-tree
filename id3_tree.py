#!/usr/bin/env python3.6
import sys
import math
from itertools import islice

class DataSet:
  """
  dataset fields:
  d.exmaples      An example matrix. It is basically a list of examples, 
                  each example is a list of attribute values + class value
  d.col_indices   A list of indices that is corresponded to a column of the 
                  examples matrix
  d.col_names     A list of name (label) corresponding to the matrix's column
  d.attr_indices  Same as col_indices but without the last column (class)
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

  def most_frequent_class(self):
    """
    return most frequent class,
    if frequency are the same, break tie by choosing class0 > class1 > class2
    """
    dict = {}
    max_frequency, classes = 0, []
    for item in [ex[-1] for ex in self.examples]:
      dict[item] = dict.get(item, 0) + 1
      if dict[item] > max_frequency:
        max_frequency = dict[item]
        classes.clear()
        classes.append(item)
      elif dict[item] == max_frequency:
        classes.append(item)
    return min(classes)
    
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
    return repr(self.result)

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
      return branches_dict[attr_value](exmaple)

  def add(self, attr_value, subtree):
    """add subtree as branch"""
    self.branches_dict[attr_value] = subtree
  
  def __repr__(self):
    return self.attr_name + ': ' self.attr

def id3_tree(dataset):
  


def parse_data(input_file):
  """ 
  return a list of column names and an examples matrix
  """
  with open(input_file, 'r') as file:
    data = file.readlines()
    col_names = data[0].split()
    examples = [line.split() for line in islice(data, 1, len(data))]
    return col_names, examples

if __name__ == '__main__':
  training_file = sys.argv[1]
  test_file = sys.argv[2]

  col_names, examples = parse_data(training_file)
  ds = DataSet(examples, col_names)
  #print(ds.col_values)
  #print(ds.col_names)
  #print(ds.col_indices)
  #print(ds.attr_indices)
  #print(len(ds.examples))
  #print(ds.most_frequent_class())
