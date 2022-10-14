from statistics import mean
import time
import matplotlib.pyplot as plt
from utils import *
from st import *
import numpy as np

def time_naive(fasta, fastq):
    n = []
    t = []
    ps, ps_names = parse_fastq(fastq)
    xs, xs_names = fasta_recs(fasta)
    for i in range(len(ps)):
        for j in range(len(xs)):
            t0 = time.time()
            idx = give_idx(ps[i], xs[j])
            t1 = time.time()
            total = t1 - t0
            n.append(len(xs[j]) * len(ps[i]))
            t.append(total)
    
    return [mean(n)], [mean(t)]

result1 = time_naive("test_data/fasta/genome-100-10.fa", "test_data/fastq/genome-100-10.fa-reads-10-10-0.fq")
result2 = time_naive("test_data/fasta/genome-100-10.fa", "test_data/fastq/genome-100-10.fa-reads-10-50-0.fq")
result3 = time_naive("test_data/fasta/genome-500-10.fa", "test_data/fastq/genome-500-10.fa-reads-10-10-0.fq")
result4 = time_naive("test_data/fasta/genome-500-10.fa", "test_data/fastq/genome-500-10.fa-reads-10-50-0.fq")
result5 = time_naive("test_data/fasta/genome-1000-10.fa", "test_data/fastq/genome-1000-10.fa-reads-10-10-0.fq")
result6 = time_naive("test_data/fasta/genome-1000-10.fa", "test_data/fastq/genome-1000-10.fa-reads-10-50-0.fq")
result7 = time_naive("test_data/fasta/worst-case.fa", "test_data/fastq/worst-case.fq")
result8 = time_naive("test_data/fasta/worst-case1.fa", "test_data/fastq/worst-case.fq")

x = result1[0] + result2[0] + result3[0] + result4[0] + result5[0] + result6[0] + result7[0] + result8[0]
y = result1[1] + result2[1] + result3[1] + result4[1] + result5[1] + result6[1] + result7[1] + result8[1]

fig, ax = plt.subplots()
ax.scatter(x, y)
ax.set_title('Time complexity')
ax.set_ylabel('Time')
ax.set_xlabel('n*m')
plt.savefig('/home/mathilde/Documents/Kandidat/GSA/Project/Project2/project-2-python-team1/src/figs/time.png')