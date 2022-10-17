import argparse
from suffix_tree import Tree
from utils import *

def give_idx(p, x):
    """Gives indexes where pattern, p, occurs in string, x.

    Args:
        p (str): pattern.
        x (str): string we want to search in.

    Returns:
        lst: list of indexes.
    """    
    s_tree = STree(x)
    return s_tree.find_all(p)

def sam_out(fasta, fastq):
    """Function that prints a simple SAM format in the terminal.

    Args:
        fasta (FASTA-file)
        fastq (FASTQ-file)
    """    
    ps, ps_names = parse_fastq(fastq)
    xs, xs_names = fasta_recs(fasta)

    for i in range(len(ps)):
        for j in range(len(xs)):
            idx = give_idx(ps[i], xs[j])
            for k in idx:
                e = get_edits(ps[i], xs[j][k :(k + len(ps[i])-1)])[2]
                l = edits_to_cigar(e)
            
                print(ps_names[i] + '\t' + xs_names[j] + '\t' + str(k + 1) + '\t' + l + '\t' + ps[i])


def main():
    argparser = argparse.ArgumentParser(
        description="Exact matching using a suffix tree")
    argparser.add_argument("genome", type=argparse.FileType('r'))
    argparser.add_argument("reads", type=argparse.FileType('r'))
    args = argparser.parse_args()
    sam_out(args.genome.name, args.reads.name)


if __name__ == '__main__':
    main()
