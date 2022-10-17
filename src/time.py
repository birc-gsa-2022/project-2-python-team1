from statistics import mean
import time
import matplotlib.pyplot as plt
import numpy as np
from suffix_tree import Tree
from random import choice

def time_data(length):
    """Function that generates DNA sequences and takes time on calculation of a Mccreight suffix tree.

    Returns:
        lst: two lists. n is sequence length. t is the calculation time for the sequence.
    """    
    bases = ['a','t','g','c']
    n = []
    t = []
    for i in range(length):
        sequence = [choice(bases) for j in range(i)]
        t0 = time.time()
        s_tree = Tree(sequence)
        t1 = time.time()
        total = t1 - t0
        n.append(i)
        t.append(total) 
        time.sleep(0.01)
    
    return n, t  

n,t = time_data(1000)

fig, ax = plt.subplots()
ax.scatter(n, t)
ax.set_title('Time complexity')
ax.set_ylabel('Time (s)')
ax.set_xlabel('Length of string (n)')
plt.savefig('/home/mathilde/Documents/Kandidat/GSA/Project/Project2/project-2-python-team1/figs/time.png')

