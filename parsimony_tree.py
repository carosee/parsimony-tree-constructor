
class Fitch_node:
	def __init__(self, num):
		self.num = num
		self.right = None
		self.left = None
		self.char_state = None


class Fitch_tree:

	def __init__(self, newick = None, chars = None, internal_num = 7):
		# newick: a string in newick format
		# chars: a dictionary of {Turtle: A}
		self.root = None
		self.internal_num = internal_num
		if newick:
			newick = newick.replace(" ","") # remove spaces
			self.root = self.build_tree(list(newick))

	def build_tree(self, newick_list):
		x = newick_list.pop(0)
		if x == '(':
			newick_list.pop() # remove ')' from list

			# add internal node
			print("add internal node", self.internal_num)
			internal_node = Fitch_node(self.internal_num)
			self.internal_num += 1

			# separate left and right lists on either side of comma
			comma_index = self.find_comma_index(newick_list)
			left_list = newick_list[:comma_index]
			right_list = newick_list[comma_index+1:]

			# build trees for left and right children
			internal_node.left = self.build_tree(left_list)
			internal_node.right = self.build_tree(right_list)
			node = internal_node
		else: # character is a leaf taxa (number from 0-5)
			print("add leaf", x)
			node = self.add_leaf(int(x))
		return node

	def find_comma_index(self, newick_list):
		count = 0
		for i in range(len(newick_list)):
			if newick_list[i] == "(":
				count += 1
			elif newick_list[i] == ")":
				count -= 1
			elif newick_list[i] == "," and count == 0:
				return i

	def add_leaf(self,num):
		node = Fitch_node(num)
		return node


newick = "(0, (5, ((1, 4), (2, 3))));"
tree = Fitch_tree(newick)
