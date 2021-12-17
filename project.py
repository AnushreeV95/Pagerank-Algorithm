# ***************************************************************************************************************************

import time

#parse file and create a 2D list with from-node to to-node
def parseFile(inFile):
    with open(inFile) as myfile:
        lines = myfile.readlines()
        
    pageId1 = []
    pageId2 = []
    mydata = []
    for line in lines[4:]:
        data = line.strip().split("\t")
        mydata.append(data)
        pageId1.append(data[0])
        pageId2.append(data[1])
    return pageId1, pageId2


#check the total number of unique nodes
def unique(MyList):
    unique_list=list(set(MyList[0]+MyList[1]))
    return unique_list


#access file
f = "../data/web-Google.txt"

MyList = parseFile(f)


############################################ creating subset from the file ####################################################
inputnodes = MyList[0].copy() #from nodes
outputnodes = MyList[1].copy() #to nodes

#initialise new lists to store subset
new_inputs=[]
new_outputs=[]

#pick a random node from the above inputnodes % outputnodes --- here 100th index
new_inputs.append(inputnodes[100])
new_outputs.append(outputnodes[100])


for i in range(0,20):
    add_index=[j for j, x in enumerate(inputnodes) if x == new_outputs[i]]
    #print("indices to look in inputnodes:", add_index)
    for idx in add_index[:10]:
        new_inputs.append(inputnodes[idx])
        new_outputs.append(outputnodes[idx])

#print("Final input-node list length is:", len(new_inputs))
#print("Final output-node list length is:", len(new_outputs))

#print(new_inputs)
#print(new_outputs)

#################################################### Remove deadendds ########################################################

#A node is a dead end if it has no out-link or 
#all of its out-links point to dead ends only


def remove_deadends(new_inputs,new_outputs):
    #list of unique dead end nodes to be removed
    to_be_removed=list(set(new_outputs) - set(new_inputs))
    #print(to_be_removed)
    all_removed=[]
    
    while(len(to_be_removed)>0):
        all_removed=to_be_removed+all_removed
        #print(len(to_be_removed))
        for i in range(0,len(to_be_removed)):
            #list of index values in new_outputs that are to be removed
            remove_index=[j for j, x in enumerate(new_outputs) if x == to_be_removed[i]]

            for idx in remove_index[::-1]:  #reverse the order of removal-- 
                new_inputs.pop(idx)
                new_outputs.pop(idx)

        to_be_removed=list(set(new_outputs) - set(new_inputs))
        
    #print(all_removed)
    return new_inputs, new_outputs


################################################### remove deadnodes using numpy #########################################################
import numpy as np

def remove_deadends_np(new_inputs,new_outputs):
    new_inputs=np.asarray(new_inputs)
    new_outputs=np.asarray(new_outputs)
    to_be_removed=list(set(new_outputs) - set(new_inputs))  #items in outputlist, not in inputlist
    to_be_removed=np.asarray(to_be_removed)

    while len(to_be_removed)>0:
        #print(len(to_be_removed))
        N=np.where(np.isin(new_outputs,to_be_removed))[0]  #index of items to be removed from both lists
        new_inputs=np.delete(new_inputs, N)
        new_outputs=np.delete(new_outputs, N)

        to_be_removed=list(set(new_outputs) - set(inputnodes))  
        to_be_removed=np.asarray(to_be_removed)
        
    return new_inputs, new_outputs
        
# the final nodes are same using both the methods

######################################################## Transition matrix ####################################################


def getTransitionMatrix(inputnodes_fresh, outputnodes_fresh):
    #unique nodes
    unique_inputs = list(set(inputnodes_fresh))  

    #to get the count of each node in order to initialise initial vector
    count_dict = {}

    for i in range(0,len(inputnodes_fresh)):
        if inputnodes_fresh[i] not in count_dict.keys():
            count_dict[inputnodes_fresh[i]] = 1
        else:
            count_dict[inputnodes_fresh[i]] += 1
    #initialise 0 in the transition matrix       
    Transition_matrix = [[0 for x in range(len(unique_inputs))] for y in range(len(unique_inputs))]

    for i in range(0,len(inputnodes_fresh)):
        input_node = inputnodes_fresh[i]
        output_node = outputnodes_fresh[i]
        
        idx_i = unique_inputs.index(input_node)
        idx_j = unique_inputs.index(output_node)
        
        Transition_matrix[idx_j][idx_i] = 1/(count_dict[input_node])
    
    Transition_matrix = np.array(Transition_matrix)
    return Transition_matrix, unique_inputs

##################################### version 1 --- probability without damping factor ########################################

def pagerank_1(Transition_matrix, unique_inputs):
    
    delta = np.ones(len(unique_inputs))
    vector = np.ones(len(unique_inputs))/len(unique_inputs)

    while max(delta) > 0.0001:
        vector_0 = vector
        vector = np.matmul(Transition_matrix, vector_0)
        delta = vector - vector_0
    return vector
    


####################################### version 2 --- probability with damping factor #########################################


def pagerank_2(Transition_matrix, unique_inputs, damping_factor = 0.85):
    
    n = len(Transition_matrix[0])
    delta = np.ones(len(unique_inputs))
    vector = np.ones(len(unique_inputs))/len(unique_inputs)
    e = np.ones(len(unique_inputs))

    while max(delta) > 0.0001:
        vector_0 = vector
        vector = (damping_factor * np.matmul(Transition_matrix, vector_0)) + ((1 - damping_factor)*(e/n))
        delta = vector - vector_0
    return vector


#print(pagerank_1(Transition_matrix))
#print(pagerank_2(Transition_matrix, damping_factor = 0.85))



################################## create final csv file by name --- 'final_file.csv' #########################################

### use new_inputs, new_outputs if using subset data, instead of inputnodes, outputnodes ###

start = time.time()
inputnodes_fresh, outputnodes_fresh = remove_deadends(inputnodes.copy(), outputnodes.copy())
#print(inputnodes_fresh , outputnodes_fresh)
#print('Computational time (deadnodes):', time.time()-start)

#start = time.time()
#inputnodes_fresh_np, outputnodes_fresh_np = remove_deadends_np(inputnodes.copy(), outputnodes.copy())
#print(inputnodes_fresh_np, outputnodes_fresh_np)
#print('Numpy computational time (deadnodes):', time.time()-start)


Transition_matrix, unique_inputs = getTransitionMatrix(inputnodes_fresh, outputnodes_fresh)
PageRank1 = pagerank_1(Transition_matrix, unique_inputs)
PageRank2 = pagerank_2(Transition_matrix, unique_inputs, damping_factor = 0.85)

header = ["Page_ID", "Page _rank_score"]
result = list(zip(unique_inputs, PageRank2))
result.insert(0, header)

f = open('final_file.csv', 'w')
for el in result:
    for i in range(len(el)):
        if i == 0:
            f.write(str(el[i]))
        else:
            f.write(',' + str(el[i]))
    f.write('\n')
f.close()


################################################################## Test code ##################################################

print("*********************** test case ***********************")

test_inputs = ["A", "A", "A", "B", "B", "C", "D", "D", "D"]
test_outputs = ["B", "C", "D", "A", "D", "C", "B", "C", "E"]

test_inputs_fresh, test_outputs_fresh = remove_deadends(test_inputs.copy(), test_outputs.copy())
Transition_matrix_test, unique_inputs_test = getTransitionMatrix(test_inputs_fresh, test_outputs_fresh)
PageRank1_test = pagerank_1(Transition_matrix_test, unique_inputs_test)
PageRank2_test = pagerank_2(Transition_matrix_test, unique_inputs_test, damping_factor = 0.8)

print('Test inputs:', test_inputs)
print('Test outputs:', test_outputs)

print("Unique nodes after deadnodes removal:", unique_inputs_test)
print("Transition matrix:", Transition_matrix_test)

print('PageRank without teleportation:', PageRank1_test)
print('PageRank with teleportation:', PageRank2_test)


#
# *************************************************************************************************************************************

def reverseEntropy(entropy):
    return -entropy

