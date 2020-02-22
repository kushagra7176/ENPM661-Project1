#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import time
import os


# In[2]:


def initial():
    initial_matrix = np.zeros(9)
    for i in range(9):
        state = int(input("Enter a number between 0-8"))
        if state < 0 or state > 8:
            print("Invalid state")
            exit(0)
        else:
           initial_matrix[i] = np.array(state)
    return np.reshape(initial_matrix,(3,3))


# In[3]:


def check_input(a):
    arr = np.reshape(a,9)
    for i in range(9):
        counter = 0
        q = arr[i]
        for j in range(9):
            if q == arr[j]:
                counter = counter + 1
        if counter >= 2:
            return True


# In[4]:


def check_solvable(b):
    arr =  np.reshape(b,9)
    inv_count = 0
    for i in range(9):
        if not arr[i] == 0:
            check_element = arr[i]
            for j in range (i+1,9):
                if check_element < arr[j] or arr[j] == 0:
                    continue
                else: 
                    inv_count = inv_count+1
    if inv_count%2 == 0 :
        print("Puzzle is solvable")
    else:
        print("Puzzle is not solvable but exploring nodes")


# In[5]:


def find_index(ofPuzzle):
    i,j = np.where(ofPuzzle == 0)
    i = int(i)
    j = int(j)
    return i,j


# In[6]:


def move_left(node_data):
    i,j = find_index(node_data)
    if j == 0:
        return None
    else:
        temp_array = np.copy(node_data)
        temp = temp_array[i,j-1]
        temp_array[i,j] = temp
        temp_array[i,j-1] = 0
        return temp_array


# In[7]:


def move_right(node_data):
    i,j = find_index(node_data)
    if j == 2:
        return None
    else:
        temp_array = np.copy(node_data)
        temp = temp_array[i,j+1]
        temp_array[i,j] = temp
        temp_array[i,j+1] = 0
        return temp_array


# In[8]:


def move_up(node_data):
    i,j = find_index(node_data)
    if i == 0:
        return None
    else:
        temp_array = np.copy(node_data)
        temp = temp_array[i-1,j]
        temp_array[i,j] = temp
        temp_array[i-1,j] = 0
        return temp_array


# In[9]:


def move_down(node_data):
    i,j = find_index(node_data)
    if i == 2:
        return None
    else:
        temp_array = np.copy(node_data)
        temp = temp_array[i+1,j]
        temp_array[i,j] = temp
        temp_array[i+1,j] = 0
        return temp_array


# In[10]:


def move_tile(action, node_data):
    if action == 'up':
        return move_up(node_data)
    if action == 'down':
        return move_down(node_data)
    if action == 'left':
        return move_left(node_data)
    if action == 'right':
        return move_right(node_data)
    else:
        return None


# In[11]:


class node:
    def __init__(self,node_index,node_data,parent,move,cost):
        self.node_index = node_index
        self.node_data = node_data
        self.parent = parent
        self.move = move
        self.cost = cost


# In[12]:


def BFS_implementation(initial_matrix):
    print("Exploring....")
    actions = ["down","up", "left","right"]
    final_ = []
    node_queue = [initial_matrix]
    visited_nodes = []
    goal_node = np.array([[1,2,3],[4,5,6],[7,8,0]])
    final_.append(node_queue[0].node_data.tolist())
    counter = 0
    while node_queue:
        current_node = node_queue.pop(0)
        if current_node.node_data.tolist() == goal_node.tolist():
            print("goal reached")
        for move in actions:
            array = move_tile(move,current_node.node_data)
            if array is not None:
                counter = counter + 1
                child = node(counter,np.array(array),current_node,move,0)
                if child.node_data.tolist() not in final_:       
                    final_.append(child.node_data.tolist())
                    visited_nodes.append(child)
                    node_queue.append(child)
                    #for x in range(len(node_queue)):
                        #print(node_queue[x])
                if child.node_data.tolist() == goal_node.tolist():
                    print("Goal Reached")
                    return child, final_,visited_nodes            
    return None, None, None                                                         


# In[13]:


def path(final_node): 
    print("Generating Path....")
    q = []  
    q.append(final_node)
    parent_node = final_node.parent
    while parent_node is not None:
        q.append(parent_node)
        parent_node = parent_node.parent
    final_path = list(q[::-1])
    for i in final_path:
         print(i.node_data)
    return final_path        


# In[14]:


def write_node_info(node_info):  
    if os.path.exists("NodesInfo.txt"):
        os.remove("NodesInfo.txt")

    f = open("NodesInfo.txt", "a")
    for Node in node_info:
        if Node.parent is not None:
            f.write(str(Node.node_index) + "\t" + str(Node.parent.node_index) + "\t" + str(Node.cost) + "\n")
    f.close()


# In[15]:


def write_nodes_explored(explored):  
    if os.path.exists("Node.txt"):
        os.remove("Node.txt")

    f = open("Node.txt", "a")
    for element in explored:
        f.write('[')
        for i in range(len(element)):
            for j in range(len(element)):
                f.write(str(element[j][i]) + " ")
        f.write(']')
        f.write("\n")
    f.close()


# In[16]:


def write_node_path(paths):  
    if os.path.exists("nodePath.txt"):
        os.remove("nodePath.txt")

    f = open("nodePath.txt", "a")
    u = []  
    u.append(paths)
    parent_node = paths.parent
    while parent_node is not None:
        u.append(parent_node)
        parent_node = parent_node.parent
    paths = list(u[::-1])
    for i in paths:
        final = np.transpose(i.node_data)
        f.write(str(np.reshape(final,9)))
        f.write("\n")
    f.close()


# In[ ]:


w = initial()
check_input(w)
if check_input(w) is True:
    print("Invalid Input")
else:    
    check_solvable(w)
    e = node(0, w, None, None, 0)
    t1 = time.time()
    r, t, y = BFS_implementation(e)
    t2 = time.time()
    Time = t2 - t1 
    print("Time Taken:"  + ' ' + str(Time)  + ' ' + "seconds")
    if r is None and t is None and y is None:
        print("Goal could not be reached")
    else:
        write_node_info(path(r))
        write_nodes_explored(t)
        write_node_path(r)    


# In[ ]:





# In[ ]:




