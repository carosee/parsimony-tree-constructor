from Bio import AlignIO
from Bio import Phylo
from Bio.Phylo.TreeConstruction import *
from cStringIO import StringIO
from Bio.Phylo import Consensus


rag1_nex = AlignIO.read(open("RAG1_trimmed.nex"), "nexus")
cytb_nex = AlignIO.read(open("CYTB_trimmed.nex"), "nexus")
morph_nex = AlignIO.read(open("morph_nex.nex"), "nexus")


def score_all_trees(nexus):
	newicks_file = open("105treesOutgroupNamed.txt","r")
	newicks = newicks_file.readlines()
	scores = []
	scorer = ParsimonyScorer()
	for newick in newicks:
		tree = Phylo.read(StringIO(newick), "newick")
		tree.rooted = True
		score = scorer.get_score(tree,nexus)
		scores.append(score)
	best_score = min(scores)
	best_index = scores.index(best_score)
	print(best_index)
	print(newicks[best_index])


def main():
	print("Finding best tree for morphological data...")
	score_all_trees(morph_nex)

	print("Finding best tree for RAG1...")
	score_all_trees(rag1_nex)

	print("Finding best tree for CytB...")
	score_all_trees(cytb_nex)

main()
