import numpy as np

# order in which the taxa appear in the nexus file
nexus_taxa_order = ['Lungfish', 'Frog', 'Opossum', 'Gecko', 'Ostrich', 'Turtle']

# takes in a nexus file and returns the matrix of data inside
def get_character_matrix(nex_file):
	nex_matrix = []
	for record in nex_file:
		sequence = record.seq
		nex_matrix.append(list(str(sequence)))
	return np.array(nex_matrix)

# takes in a string of newick format tree, an entire matrix
#   of nexus data, and an index 
# uses the two functions below it reorder the data
#   so that the newick matches the nexus data
# returns the nexus data as a correctly ordered list
#   for the tree you're currently looking at
def get_character(newick, matrix, i):
	chars = matrix[:,i]
	newick_taxa = get_taxa_list(newick)
	rearranged = rearrange_chars(newick_taxa, chars)
	return rearranged

# takes in a string of newick format
# returns a list of the taxa names without newick format
def get_taxa_list(newick):
	newick = newick.replace("(", "")
	newick = newick.replace(")", "")
	newick = newick.replace(",", "") 
	newick = newick.replace(";", "")
	return newick.split()

# takes in the taxa names and the current list of characters
# returns a list of the next nexus data in the set
def rearrange_chars(taxa_list, chars):
	# chars is ordered according to the original nexus file
	# taxa_list is ordered according to the newick tree
	d = dict(zip(nexus_taxa_order, chars)) # ex: {Gecko: A, Lungfish: A}
	new_nexus = [d[taxa] for taxa in taxa_list]
	return new_nexus


# Below adapted from code by Lillie Schachter
# takes in two node-states (either strings or lists)
# if the intersection is empty or has more than one item,
#	 returns a list
# if the intersection is 1 item, returns it as a string
def get_intersection(a,b):
	inter = list(set(a).intersection(set(b)))
	if len(inter) == 1:
		return inter[0]
	return inter

# takes in two node-states (either strings or lists)
# returns a list of the incoming node-states combined
def get_union(a,b):
	un = list(set(a).union(set(b)))
	if len(un) == 1:
		return un[0]
	return un