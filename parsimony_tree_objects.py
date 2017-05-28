# Below adapted from code by Lillie Schachter

class Fitch_Node:
	'''A node for an evolutionary tree,
	meant to be built from newick format
	using character states from a chars
	file'''

	def __init__(self,name,state = None):
		'''Node contains character state,
		a name, pointers to left and right
		children, and a leaf_num to correspond
		to a chars matrix when reassigning 
		character states'''
		self.state = state
		self.name = name
		self.right = None
		self.left = None
		self.leaf_num = None

	def is_leaf(self):
		'''Returns true if the node is a leaf'''
		return self.left == None and self.right == None


class Fitch_Tree:

	def __init__(self, newick = None, chars = None, internal = 7):
		'''initializes an empty fitch tree
		with optional "internal" value to 
		name the internal nodes. If no number
		is given, it assumes that the tree will
		have 6 leaves (with internal starting at 7)'''
		self.root = None
		self.newick = newick
		self.chars = chars
		self.internal = internal
		self.leaf_num = 0
		if self.newick:
			self.create_fitch_tree()

	def create_fitch_tree(self,newick = None,chars = None):
		'''populates the tree given a newick string.
		If a list of character states is provided in
		chars, it builds the tree with those states.
		Otherwise, you can add the states in later.'''
		if chars:
			self.chars = chars
		if newick:
			self.newick = newick
		newick = self.newick.split(', ')
		self.root, newick = self.add_fitch_node(newick)

	def add_fitch_node(self, newick):
		'''recursive function that builds an entire
		tree from a newick string. If chars data was
		given, it will also set the leaf character
		states'''
		
		if newick[0][0] == "(":
			#must create an internal node
			node = Fitch_Node(self.internal)
			self.internal += 1
			
			#get rid of the '(' and create the internal node's left child
			newick = [newick[0][1:]]+newick[1:]
			node.left, newick = self.add_fitch_node(newick)
			#get rid of the left child and create the right
			node.right, newick = self.add_fitch_node(newick[1:])
		else:
			node = self.create_leaf_node(newick[0])

		return node, newick


	def create_leaf_node(self, name):
		'''take in the name of the leaf node and build it'''
		clean_name = self.clean_leaf_name(name)
		node = Fitch_Node(clean_name)
		node.leaf_num = self.leaf_num
		self.leaf_num += 1

		if self.chars:
			char_info = self.chars[node.leaf_num]
			node.state = char_info
		return node

	def clean_leaf_name(self,name):
		'''if it's right leaf: get rid of closing brackets etc'''
		closing = name.find(')')
		if closing != -1:
			name = name[:closing]
		return name

	def add_leaf_states(self,chars):
		'''The same tree will need to be scored
		for multiple characters. This method resets
		the leaves' character states from a new 
		set of chars data'''
		self.get_post_order_nodes()
		for node in self.post_order_nodes:
			if node.leaf_num != None:
				node.state = chars[node.leaf_num]
		return self.post_order_nodes

	def get_post_order_nodes(self):
		'''Calls recursive function that returns a list
		of nodes in the tree in post-order traversal'''
		self.post_order_nodes = []
		self.post_order_traversal_2(self.root)
		return self.post_order_nodes

	def post_order_traversal_2(self,current_node):
		'''continues until the current node is null'''
		if current_node:
			self.post_order_traversal_2(current_node.left)
			self.post_order_traversal_2(current_node.right)
			self.post_order_nodes.append(current_node)

