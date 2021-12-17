## **PAGERANK ALGORITHM**

## Description

The goal here is to compute the PageRank score by implementing the PageRank algorithm for the web dataset from the Stanford Large Network Dataset Collection provided by Google in a programming contest in 2002.  
The damping factor considered will be 0.85 (empirically determined).

### Dataset

The [dataset](https://snap.stanford.edu/data/web-Google.html) is in .txt format with the following details: 
*  This dataset contains 875713 page_Ids and 5105039 links.  
*  Rows 1 to 4: Metadata (self-explanatory information of data) 
*  Remaining rows: Each row consists of 2 values representing the link from the web page in the 1st column to the web page in the 2nd column.  

## Code

### Parse file

The function parseFile takes the input file and returns a list (MyList) of Page_Ids and links as inputnodes and outputnodes. 

### Creating the subset of the data

We randomly choose an inputnode index and traverse through its links (range) and add the new nodes to the subset list. 

### Remove dead nodes

To remove dead nodes, we must scan the dataset multiple times because some nodes may become dead nodes after removal of outer dead nodes. We stop scanning when we do not find any dead nodes in one complete traversal.

#### Function:
list remove_deadends(list new_inputs, list new_outputs)
#### Input: 
new_inputs, a list containing the input nodes
new_outputs, a list containing the output nodes
#### Output:
List of input and output nodes after removal of deadnodes

### Transition Matrix

The transition matrix defines the probability of reaching a particular page from a given page (for a random surfer). Transition Matrix M is stochastic, each column adds upto 1. 

#### Function:
list getTransitionMatrix(list inputnodes_fresh, list outputnodes_fresh)
#### Input: 
inputnodes_fresh, a list containing the input nodes with no deadnodes
outputnodes_fresh, a list containing the output nodes with no deadnodes
#### Output:
Transition_matrix, 2 D array
unique_inputs, list of all unique nodes

### Pagerank 

To simulate the path of random surfer, we multiply the transition matrix with its previous position (probability vector). 
Given the stochastic nature of the transition matrix, its principle eigen vector is the limiting position of the random surfer. Simulating the path of random surfer is computationally less expensive than finding the eigen vector of this matrix. Typically it takes 50-75 iterations for convergence.

The final probability vector after convergence signifies the importance of each page. 

#### Function:
2D Array, list pagerank_1(2D array Transition_matrix, list unique_inputs)
#### Input: 
Transition_matrix, a 2D array with probability of visiting a particular page from a particular webpage
unique_inputs, list of all unique nodes
#### Output:
vector, a list containing PageRank scores for all unique nodes

### Dealing with spider traps

A spider trap is a collection of nodes connected among themselves but without any outlinks. This causes the surfer to get stuck in this "trap", as a result the pagerank accumulates within this collection.

#### Function:
2D Array, list pagerank_2(2D array Transition_matrix, list unique_inputs, float damping_factor = 0.85)
#### Input: 
Transition_matrix, a 2 D array with probability of visiting a particular page from a particular webpage
unique_inputs, list of all unique nodes
damping_factor, float (1-damping_factor) is the probability that the surfer can teleport to any other webpage with equal probability at each step
#### Output:
vector, a list containing PageRank scores for all unique nodes 

### Test

To test the pagerank algorithm, a sample transition matrix from [chapter 5](http://infolab.stanford.edu/~ullman/mmds/ch5.pdf) - "Link Analysis" was used. 

Multiple different subsets of the initial dataset were also used to test the algorithm. 

## Results

The csv file named “final_file.csv” cooresponding to the complete dataset, has Page_ID as the first column and corresponding PageRank score as the 2nd column. This will be the final output of the project. 

