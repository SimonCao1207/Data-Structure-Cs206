from BinaryTree import LinkedBinaryTree


class BinarySearchTree(LinkedBinaryTree):
	
	def __init__(self):
		super().__init__()

	def is_empty(self):
		return self._size == 0

    # ----------------NON PUBLIC CLASS---------------------------
	def _subtree_search(self, p, v):
		"""
		Return position p have value v, or last node searched.
		"""
		if v == p.element():
			return p

		elif v < p.element(): # search left subtree
			if self.left(p) is not None: 
				return self._subtree_search(self.left(p), v)

		else: # search right subtree
			if self.right(p) is not None: 
				return self._subtree_search(self.right(p), v)

		return p # unsuccessful search

	def _subtree_first_position(self, p):
		"""
		Return first node of subtree rooted at root node.
		"""
		walk = p
		while self.left(walk):
			walk = self.left(walk)
		return walk

	def _subtree_last_position(self, p):
		"""
		Return last node of subtree rooted at p.
		"""
		walk = p
		while self.right(walk):
			walk = self.right(walk)
		return walk

	#------------------------PUBLIC CLASS---------------------------------
	def insert(self, v):
		if self.is_empty():
			leaf = self._add_root(v)
		else:
			pos = self._subtree_search(self.root(), v)
			if v < pos.element():
				leaf = self._add_left(pos, v)
			else:
				leaf = self._add_right(pos, v)

		self._rebalance_insert(leaf) # hook for balanced tree subclass

	def delete(self, index):
		"""
		Remove the node at given index in positions list
		"""
		p = self._positions[index]
		self._validiate(p)
		if self.right(p) and self.left(p): # if p has both children
			pos = self._subtree_first_position(p.right)
			self._replace(p, pos.element)
			p = pos
		# now p has at most one child
		parent = self.parent(p) # use for balance the tree
		self._delete(p)
		self._rebalance_delete(parent) # if root deleted, parent is None.

	def first(self):
		p = self._subtree_first_position(self.root())
		return p.element() if len(self) > 0 else None

	def last(self):
		p = self._subtree_last_position(self.root())
		return p.element() if len(self) > 0 else None

	def find(self, v):
		if self.is_empty():
			return None
		p = self._subtree_search(self.root(), v)
		if v == p.element():
			return True
		else:
			return False

	def create_bst_from_array(self, arr):
		for v in arr:
			self.insert(v)

	#..................................................................................
	# hooked used by subclass to balance the tree
	def _rebalance_insert(self, p):
		"""Call to indicate that position p is newly added"""
		pass

	def _rebalance_delete(self, p):
		"""Call to indicate that position p was recently accessed"""
		pass

# TEST

BST = BinarySearchTree()

arr = [4,2,6,1,5,3,10,1,5]

BST.create_bst_from_array(arr)

# BST.print_inorder() # left root right
# BST.print_preorder() #root left right
# BST.print_postorder() #left right root

# BST.delete(6) # delete at index 6 

# BST.print_inorder() # left root right
# BST.print_preorder() #root left right
# BST.print_postorder() #left right root

BST.print2D()


