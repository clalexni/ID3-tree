# id3-tree
Please go to my [github](https://github.com/clalexni/id3-tree) repository for formatted README and output file

### Goal 
- build ID3 decision tree
- produce accuracy
- plot learning curve

### Requirements:
- Install Python 3.6
- data file (path) for inputs training and test set
- command line: 
  - run these two lines to ensure the correct python version
  - the first line gives user permission to execute the code using shebang style
  - the second line takes two input of data file path (./data/train.dat for instance)
    the first input is the training set and the second input should be the test set
~~~
chmod u+x id3_tree.py
~~~
~~~
./id3_tree.py [input1] [input2]
~~~

  - for instance: 
~~~
./id3_tree.py data/train.dat data/test.dat
~~~
  - use the following command to redirect output, for example:
~~~
./id3_tree.py data/train.dat data/test.dat > out.txt
~~~
- tested on macos/Linux

### Learning Curve:
![Learning Curve](/outputs/learn.png)

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
    - If equally common class exists in the entire dataset, break tie class0 > class1 > class2 > ..
3. no attribute left:
  - choose the most frequent class of the subset at the leaf node
    - If classes are equally common at subset, select from the entire dataset
      - If equally common class exists in the entire dataset, break tie class0 > class1 > class2 > ..



