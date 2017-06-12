from Bio import AlignIO
from parsimony_tree_objects import Fitch_Node, Fitch_Tree
from parsimony_helper_functions import *


def find_best_tree(scores, newick_trees):
	best_score = min(scores)
	best_index = scores.index(best_score)
	print(newick_trees[best_index])

def score_all_trees(nex_file, newick_trees):
	parsimony_scores = []
	for newick in newick_trees:
		score = score_tree(nex_file, newick)
		parsimony_scores.append(score)

	return parsimony_scores


def score_tree(nex_file, newick):
	tree = Fitch_Tree()
	tree.create_fitch_tree(newick)

	nexus_matrix = get_character_matrix(nex_file)
	parsimony_score = 0
	for i in range(len(nexus_matrix[0])):
		char_column = get_character(newick, nexus_matrix, i)
		node_list = tree.add_leaf_states(char_column)
		parsimony_score = parsimony_score + fitch_bottom_up(node_list)
	return parsimony_score


def fitch_bottom_up(node_list):
	possible_character_states = {}
	num_unions = 0
	for node in node_list:
		if node.is_leaf():
			possible_character_states[node.name] = node.state
		else:
			intersection = get_intersection(node.left.state, node.right.state)
			if intersection:
				possible_character_states[node.name] = intersection
				node.state = intersection
			else:
				union = get_union(node.left.state, node.right.state)
				possible_character_states[node.name] = union
				node.state = union
				num_unions += 1
	# print(num_unions)
	return num_unions


def main():
	# morph_nex = AlignIO.read(open("morph_data.nex"), "nexus")
	rag1_nex = AlignIO.read(open("RAG1_trimmed.nex"), "nexus")
	cytb_nex = AlignIO.read(open("CYTB_trimmed.nex"), "nexus")

	newick_file = open('105treesOutgroupNamed.txt','rU')
	newick_trees = newick_file.readlines()

	print("Finding best tree for RAG1...")
	scores = score_all_trees(rag1_nex,newick_trees)
	find_best_tree(scores, newick_trees)

	print("Finding best tree for CytB...")
	scores = score_all_trees(cytb_nex,newick_trees)
	find_best_tree(scores, newick_trees)


main()
